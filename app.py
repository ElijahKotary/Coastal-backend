from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from flask_cors import CORS


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://claizgaivvgtdp:c40cf15a9bc9fdd14ba5ea5afb85e01f2fbe93fadf64491d2a16a80b998558d5@ec2-54-173-77-184.compute-1.amazonaws.com:5432/d3hpp1nj0upg0"

db = SQLAlchemy(app)
ma = Marshmallow(app)
# CORS(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, nullable=False)
    item = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, image, item, price):
        self.image = image
        self.item = item
        self.price = price
    
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'image', 'item', 'price')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#end point to create new product
@app.route("/product", methods=['POST'])
def add_product():
    post_data = request.get_json()
    image = post_data.get['image']
    item = post_data.get['item']
    price = post_data.get['price']

    new_record = Product(image, item, price)
    db.session.add(new_record)
    db.session.commit()

    return jsonify("Product Added")

#endpoint to query all products
@app.route("/products", methods=["GET"])
def get_all_products():
    all_products = Product.query.all()
    return jsonify(products_schema.dump(all_products))

# # Endpoint for querying a single product
# @app.route("/product/<id>", methods=["GET"])
# def get_product(id):
#     pro = Product.query.get(id)
#     return_data = (products_schema.dump(get_product))
#     return product_schema.jsonify(product)

# Endpoint for deleting a record
@app.route("/product/delete/<id>", methods=["DELETE"])
def product_delete(id):
    record = db.session.query(Product).filter(Product.id == id).first()
    db.session.delete(record)
    db.session.commit()
    return jsonify("Product Deleted")


if __name__ == '__main__':
    app.run(debug=True)