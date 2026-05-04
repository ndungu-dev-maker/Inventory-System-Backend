from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Product
import os


# Create Flask app

app = Flask(__name__)

# Enable CORS

CORS(app)

# Database configuration

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database

db.init_app(app)

# Create tables

with app.app_context():

    db.create_all()


@app.route("/")
def home():

    return "Inventory Backend Running"

# REGISTER USER

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Check if user exists

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:

        return jsonify({
            "message": "User already exists"
        }), 400

    # Hash password

    hashed_password = generate_password_hash(
        password
    )

    # Create new user

    new_user = User(
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)

    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    })

# LOGIN USER

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    # Find user

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:

        return jsonify({
            "message": "User not found"
        }), 404

    # Check password

    if not check_password_hash(
        user.password,
        password
    ):

        return jsonify({
            "message": "Incorrect password"
        }), 401

    return jsonify({
        "message": "Login successful",
        "user_id": user.id
    })

# ADD PRODUCT

@app.route("/add-product", methods=["POST"])
def add_product():

    data = request.get_json()

    name = data.get("name")
    quantity = data.get("quantity")
    min_quantity = data.get("min_quantity")
    user_id = data.get("user_id")

    # Create new product

    new_product = Product(
        name=name,
        quantity=quantity,
        min_quantity=min_quantity,
        user_id=user_id
    )

    db.session.add(new_product)

    db.session.commit()

    return jsonify({
        "message": "Product added successfully"
    })

# VIEW PRODUCTS

@app.route("/products/<int:user_id>", methods=["GET"])
def get_products(user_id):

    products = Product.query.filter_by(
        user_id=user_id
    ).all()

    product_list = []

    for product in products:

        # Check low stock

        if product.quantity < product.min_quantity:
            status = "LOW STOCK"
        else:
            status = "OK"

        product_list.append({

            "id": product.id,
            "name": product.name,
            "quantity": product.quantity,
            "min_quantity": product.min_quantity,
            "status": status

        })

    return jsonify(product_list)
# UPDATE PRODUCT QUANTITY

@app.route("/update-product/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    data = request.get_json()

    new_quantity = data.get("quantity")

    # Find product

    product = Product.query.get(product_id)

    if not product:

        return jsonify({
            "message": "Product not found"
        }), 404

    # Update quantity

    product.quantity = new_quantity

    db.session.commit()

    return jsonify({
        "message": "Product updated successfully"
    })

# DELETE PRODUCT

@app.route("/delete-product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    # Find product

    product = Product.query.get(product_id)

    if not product:

        return jsonify({
            "message": "Product not found"
        }), 404

    # Delete product

    db.session.delete(product)

    db.session.commit()

    return jsonify({
        "message": "Product deleted successfully"
    })


# Run server


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
