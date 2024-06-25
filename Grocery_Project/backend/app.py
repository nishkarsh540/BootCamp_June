from flask import Flask,jsonify
from flask_restful import Api,Resource,reqparse
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,unset_jwt_cookies,get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash
from model import db,User,Category,Product
from Management.category import category_bp
from Management.product import ProductListResource,ProductResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'grocery'

db.init_app(app)
CORS(app,origins='*')
jwt = JWTManager(app)
api = Api(app)

app.register_blueprint(category_bp, url_prefix='/api')
api.add_resource(ProductListResource, '/products')
api.add_resource(ProductResource, '/products/<int:product_id>')

class StoreManagerResource(Resource):
    def get(self):
        store_managers = User.query.filter_by(role='store-manager').all()
        store_manager_list = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active
        } for user in store_managers]
        return {"store_managers": store_manager_list}, 200

    def post(self, user_id, action):
        user = User.query.get(user_id)
        if not user or user.role != 'store-manager':
            return {"message": "User not found or not a store manager"}, 404
        
        if action == 'approve':
            user.is_active = True
            message = "Store manager approved"
        elif action == 'delete':
            db.session.delete(user)
            db.session.commit()
            return {"message": "Store manager deleted"}, 200
        elif action == 'flag':
            user.is_active = False
            message = "Store manager flagged"
        else:
            return {"message": "Invalid action"}, 400
        
        db.session.commit()
        return {"message": message}, 200

# Add these resources to the API
api.add_resource(StoreManagerResource, '/store-managers', '/store-managers/<int:user_id>/<string:action>')



class SignupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help='Username is required')
        parser.add_argument('email',type=str,required=True,help='email is required')
        parser.add_argument('password',type=str,required=True,help='Password is required')
        parser.add_argument('role',type=str,default='user')
        args= parser.parse_args()

        is_active = False if args['role'] == 'store-manager' else True

        if User.query.filter_by(username=args['username']).first():
            return {"message":"username already exists"}, 400
        if User.query.filter_by(email=args['email']).first():
            return {'message':"email already exists"}, 400
        
        hashed_password = generate_password_hash(args['password'])

        new_user = User(username=args['username'],email=args['email'],password=hashed_password,role=args['role'],is_active=is_active)

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
    def get(self):
        users = User.query.all()
        user_info = [{
                "id":user.id,
                "username":user.username,
                "role":user.role
        } for user in users]

        return user_info

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Get the identity of the current user
    current_user = get_jwt_identity()

    # Perform any necessary logout actions here
    # For example, logging the user out, revoking tokens, etc.

    # Return a JSON response indicating successful logout
    return jsonify({'message': 'User logged out successfully'}), 200


api.add_resource(UserInfo,'/api/user_info')
api.add_resource(SignupResource,'/api/signup')
api.add_resource(LoginResource,'/api/login')
if __name__ =="__main__":
    app.run(debug=True)