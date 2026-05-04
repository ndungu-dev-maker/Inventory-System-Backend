from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize database

db = SQLAlchemy()

# USER TABLE

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    # Relationship with products

    products = db.relationship(
        "Product",
        backref="user",
        lazy=True
    )


# PRODUCT TABLE

class Product(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    min_quantity = db.Column(
        db.Integer,
        nullable=False
    )

    date_added = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Link product to user

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
