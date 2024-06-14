from flask import Flask
from flask_restful import Api,Resource,reqparse
from flask_jwt_extended import JWTManager,create_access_token,jwt_required
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash
from model import db,User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'grocerystore'

db.init_app(app)
CORS(app,origins='*')
jwt= JWTManager(app)
api = Api(app)

class SignupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help='username is required')
        parser.add_argument('email',type=str,required=True,help='email is required')
        parser.add_argument('password',type=str,required=True,help='password is required')
        parser.add_argument('role',type=str,default='user')

        args = parser.parse_args()

        if User.query.filter_by(username=args['username']).first():
            return {"message":"Username already Exists"}, 400
        if User.query.filter_by(username=args['email']).first():
            return {"message":"Email already Exists"}, 400

        hashed_password = generate_password_hash(args['password'])

        new_user = User(username=args['username'],email=args['email'],password = hashed_password,role=args['role'])

        db.session.add(new_user)
        db.session.commit()

        return {"message":"User Created Successfully"}, 201

api.add_resource(SignupResource,'/api/signup')

if __name__ =="__main__":
    app.run(debug=True)
