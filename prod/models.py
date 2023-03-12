#!/usr/bin/env python3
""" Script for the model of product for the ecommerce API """
from . import prod
from run import db
from sqlalchemy_media import Image, ImageAnalyzer, ImageValidator, ImageProcessor


class ProductImage(Image):
    __pre_processors__ = [
        ImageAnalyzer(),
        ImageValidator(
            minimum=(80, 80),
            maximum=(800, 600),
            content_types=['image/jpeg', 'image/png']
        ),
        ImageProcessor
    ]


product_tags = db.Table("product_tags", db.Model.metadata,
    db.Column('tags_id', db.Unicode, db.ForeignKey("Tags.id")),
    db.Column('Product_id', db.Unicode, db.ForeignKey("Product.id")),
)

class Product(db.Model):
    __tablename__ = "Product"

    product_id = db.Column(db.Unicode(length=225), primary_key=True, unique=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    in_stock = db.Column(db.Integer, default=0)
    merchant_id = db.Column(db.Integer, db.ForeignKey('User.merchant_id'))
    tags = db.relationship("Tags", secondary=table, back_populates="Product")
    # image =
    # category =

class Tags(db.Model):
    __tablename__ = "Tags"

    tag_id = db.Column(db.Unicode(length=224), primary_key=True, unique=True)
    name = db.Column(db.String(128), nullable=False)
    product = db.relationship("Product", secondary=table, back_populates="Tags")
    descriiption = db.Column(db.Text)
