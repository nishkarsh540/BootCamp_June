from flask import Flask, jsonify, make_response
from flask_restful import Api,Resource,reqparse
from flask_jwt_extended import JWTManager,create_access_token,jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash
from model import db,User,Category,Product
from Management.category import category_bp
from celery_config import celery
from flask_caching import Cache
import redis
app = Flask(__name__)
redis_client = redis.Redis(host='localhost',port=6379,db=0)
cache = Cache(app,config={'CACHE_TYPE':'redis','CACHE_REDIS':redis_client})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'grocery'
celery.conf.update(app.config)


db.init_app(app)
CORS(app,origins='*')
jwt = JWTManager(app)
api = Api(app)

app.register_blueprint(category_bp, url_prefix='/api')

class SignupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help='Username is required')
        parser.add_argument('email',type=str,required=True,help='email is required')
        parser.add_argument('password',type=str,required=True,help='Password is required')
        parser.add_argument('role',type=str,default='user')
        args= parser.parse_args()

        if User.query.filter_by(username=args['username']).first():
            return {"message":"username already exists"}, 400
        if User.query.filter_by(email=args['email']).first():
            return {'message':"email already exists"}, 400
        
        hashed_password = generate_password_hash(args['password'])

        new_user = User(username=args['username'],email=args['email'],password=hashed_password,role=args['role'])

        db.session.add(new_user)
        db.session.commit()

        return {"message":'user created succesfully'},200

class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True)
        parser.add_argument('password',type=str,required=True)
        args= parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()
        if user and check_password_hash(user.password,args['password']):
            access_token = create_access_token(identity=user.role)
            user_info={
                "id":user.id,
                "username":user.username
            }
            return {'access_token':access_token,"user": user_info},200
        else:
            return {'message':"Invalid Username or password"}, 401

class UserInfo(Resource):
    @cache.cached(timeout=2)
    def get(self):
        users = User.query.all()
        user_info = [{
                "id":user.id,
                "username":user.username,
                "role":user.role
        } for user in users]

        return user_info

class ExportResource(Resource):
    @jwt_required()
    def post(self,user_id):
        user_role = get_jwt_identity()
        if user_role !='admin':
            return jsonify({'message':'access denied'})
        
        try:
            from tasks import export_product_details_as_csv

            csv_data = export_product_details_as_csv(user_id)
            response = make_response(csv_data)
            response.headers['Content-Disposition'] = 'attachment; filename=product_report.csv'

            response.headers['Content-type'] = "text/csv"
            return response
        except Exception as e:
            return jsonify(e),500



api.add_resource(ExportResource,'/exportcsv/<int:user_id>')
api.add_resource(UserInfo,'/api/user_info')
api.add_resource(SignupResource,'/api/signup')
api.add_resource(LoginResource,'/api/login')
if __name__ =="__main__":
    app.run(debug=True)