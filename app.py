from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://slxkhaaopgcmqd:980eb134404e00bb48996f5c3d765b0fadb3632aa6b03b7b8571e024c8ca71fd@ec2-3-230-122-20.compute-1.amazonaws.com:5432/d54crk6ts0nj1g"

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), unique= True, nullable=False)
    item = db.Column(db.String(100), unique=False)
    price = db.Column(db.Integer, unique=False)

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
@app.route('/product', methods=['POST'])
def add_product():
    image = request.json['image']
    item = request.json['item']
    price = request.json['price']

    new_product = Product(image, item, price)

    db.session.add(new_product)
    db.session.commit()
    
    product = Product.query.get(new_product.id)

    return product_schema.jsonify(product)

#endpoint to query all products
@app.route("/products", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Endpoint for querying a single product
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Endpoint for deleting a record
@app.route("/product/<id>", methods=["DELETE"])
def product_delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)