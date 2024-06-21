# management/category.py

from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, reqparse
from model import db, Category

category_bp = Blueprint('category_bp', __name__)
api = Api(category_bp)

# Resource for Category CRUD operations
class CategoryResource(Resource):
    # Get all categories
    def get(self):
        categories = Category.query.all()
        return jsonify([{
            'id': category.id,
            'name': category.name
        } for category in categories])

    # Create a new category
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        args = parser.parse_args()

        if Category.query.filter_by(name=args['name']).first():
            return {"message": "Category already exists"}, 400
        
        new_category = Category(name=args['name'])
        db.session.add(new_category)
        db.session.commit()

        return {"message": 'Category created successfully'}, 200

    # Update an existing category
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='Category ID is required')
        parser.add_argument('name', type=str, required=True, help='Name is required')
        args = parser.parse_args()

        category = Category.query.get(args['id'])
        if not category:
            return {"message": "Category not found"}, 404
        
        category.name = args['name']
        db.session.commit()

        return {"message": 'Category updated successfully'}, 200

    # Delete a category
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help='Category ID is required')
        args = parser.parse_args()

        category = Category.query.get(args['id'])
        if not category:
            return {"message": "Category not found"}, 404
        
        db.session.delete(category)
        db.session.commit()

        return {"message": 'Category deleted successfully'}, 200

# Add resource to API
api.add_resource(CategoryResource, '/category')

# Optionally, you can define more routes or resources here


