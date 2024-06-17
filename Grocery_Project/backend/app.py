from flask import Flask
from flask_restful import Api,Resource,reqparse
from flask_jwt_extended import JWTManager,create_access_token,jwt_required
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash
from model import db,User
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACT_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'grocery'

db.init_app(app)
CORS(app,origins='*')
jwt = JWTManager(app)
api = Api(app)


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
            access_token = create_access_token(identity=user.username)
            user_info ={
                "id":user.id,
                "username":user.username,
                "role":user.role
            }
            return {'access_token':access_token,"user":user_info}, 200
        else:
            return {'message':"invalid username or password"}, 401
        
class UserInfo(Resource):
    def get(self):
        user = User.query.all()
        user_info=[ {
            "id":u.id,
            "username":u.username
        } for u in user]
        return ("user",user_info),200


api.add_resource(SignupResource,'/api/signup')
api.add_resource(LoginResource,'/api/login')
api.add_resource(UserInfo,'/info')
if __name__ =="__main__":
    app.run(debug=True)