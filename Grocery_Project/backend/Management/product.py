from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from model import db, Product, Category, User
from datetime import datetime

class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        product_list = [{
            'id': product.id,
            'name': product.name,
            'category': product.category.name,
            'category_id': product.category_id,
            'expiry_date': product.expiry_date.strftime('%Y-%m-%d') if product.expiry_date else None,
            'manufacture_date': product.manufacture_date.strftime('%Y-%m-%d') if product.manufacture_date else None,
            'price': product.price,
            'unit': product.unit,
            'quantity': product.quantity,
            'created_at': product.created_at.strftime('%Y-%m-%dT%H:%M:%S') if product.created_at else None,
            'created_user_id': product.created_user_id,
            'sold_quantity': product.sold_quantity
        } for product in products]
        return {"products": product_list}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('category_id', type=int, required=True, help='Category ID is required')
        parser.add_argument('expiry_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=False)
        parser.add_argument('manufacture_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=False)
        parser.add_argument('price', type=float, required=True, help='Price is required')
        parser.add_argument('unit', type=str, required=True, help='Unit is required')
        parser.add_argument('quantity', type=float, required=True, help='Quantity is required')
        parser.add_argument('created_user_id', type=int, required=True, help='Created User ID is required')
        parser.add_argument('sold_quantity', type=float, required=False, default=0.0)
        args = parser.parse_args()

        if not Category.query.get(args['category_id']):
            return {'message': 'Category not found'}, 404
        if not User.query.get(args['created_user_id']):
            return {'message': 'User not found'}, 404

        new_product = Product(
            name=args['name'],
            category_id=args['category_id'],
            expiry_date=args['expiry_date'],
            manufacture_date=args['manufacture_date'],
            price=args['price'],
            unit=args['unit'],
            quantity=args['quantity'],
            created_user_id=args['created_user_id'],
            sold_quantity=args['sold_quantity']
        )

        db.session.add(new_product)
        db.session.commit()

        return {"message": "Product created successfully", "product": {
            'id': new_product.id,
            'name': new_product.name,
            'category': new_product.category.name,
            'category_id': new_product.category_id,
            'expiry_date': new_product.expiry_date,
            'manufacture_date': new_product.manufacture_date,
            'price': new_product.price,
            'unit': new_product.unit,
            'quantity': new_product.quantity,
            'created_at': new_product.created_at,
            'created_user_id': new_product.created_user_id,
            'sold_quantity': new_product.sold_quantity
        }}, 201

class ProductResource(Resource):
    def get(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404
        return {
            'id': product.id,
            'name': product.name,
            'category': product.category.name,
            'category_id': product.category_id,
            'expiry_date': product.expiry_date,
            'manufacture_date': product.manufacture_date,
            'price': product.price,
            'unit': product.unit,
            'quantity': product.quantity,
            'created_at': product.created_at,
            'created_user_id': product.created_user_id,
            'sold_quantity': product.sold_quantity
        }, 200

    def put(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=False)
        parser.add_argument('category_id', type=int, required=False)
        parser.add_argument('expiry_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=False)
        parser.add_argument('manufacture_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=False)
        parser.add_argument('price', type=float, required=False)
        parser.add_argument('unit', type=str, required=False)
        parser.add_argument('quantity', type=float, required=False)
        parser.add_argument('created_user_id', type=int, required=False)
        parser.add_argument('sold_quantity', type=float, required=False)
        args = parser.parse_args()

        if args['category_id'] and not Category.query.get(args['category_id']):
            return {'message': 'Category not found'}, 404
        if args['created_user_id'] and not User.query.get(args['created_user_id']):
            return {'message': 'User not found'}, 404

        if args['name']:
            product.name = args['name']
        if args['category_id']:
            product.category_id = args['category_id']
        if args['expiry_date']:
            product.expiry_date = args['expiry_date']
        if args['manufacture_date']:
            product.manufacture_date = args['manufacture_date']
        if args['price']:
            product.price = args['price']
        if args['unit']:
            product.unit = args['unit']
        if args['quantity']:
            product.quantity = args['quantity']
        if args['created_user_id']:
            product.created_user_id = args['created_user_id']
        if args['sold_quantity'] is not None:
            product.sold_quantity = args['sold_quantity']

        db.session.commit()

        return {"message": "Product updated successfully"}, 200

    def delete(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted successfully"}, 200
