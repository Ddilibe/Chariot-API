#!/usr/bin/env python3
""" Script for the model of product for the ecommerce API """
import json
import uuid
import base64
from . import prod
from os.path import join
from run import db, TEMP_PATH
from sqlalchemy_media import Image, ImageAnalyzer, ImageValidator, ImageProcessor


class ProductImage(Image):
    __pre_processors__ = [
        ImageAnalyzer(),
        ImageValidator(
            minimum=(80, 80),
            maximum=(800, 600),
            content_types=['image/jpeg', 'image/png']
        ),
        ImageProcessor(
            fmt='jpeg',
            width=120
        )
    ]


class Json(db.TypeDecorator):
    impl = db.Unicode

    def process_bind_param(self, value, engine):
        return json.dumps(value)

    def process_result_value(self, value, engine):
        return json.loads(value) if value else None


product_tags = db.Table("product_tag", db.Model.metadata,
    db.Column('Product_id', db.Unicode, db.ForeignKey("product.prod_id")),
    db.Column('Tag_id', db.Unicode, db.ForeignKey("tag.tag_id"))
)

class Product(db.Model):
    __tablename__ = "product"

    prod_id = db.Column(db.Unicode(length=225), primary_key=True, unique=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    in_stock = db.Column(db.Integer, default=0)
    merchant_id = db.Column(db.Integer, db.ForeignKey('User.merchant_id'))
    tags = db.relationship("Tag", secondary=product_tags, back_populates="products")
    image = db.Column(ProductImage.as_mutable(Json))
    # category =

    def __init__(self, *args,  **kwargs):
        super(Product, self). __init__( *args, **kwargs)
        self.prod_id = str(uuid.uuid4())

    @classmethod
    def get_dict(cls):
        # with open(self.)
        # with open(TEMP_PATH, self.image.path) as im:
        # image = self.image.get_thumbnail(ratio=3, auto_generate=True)
        return cls.__dict__

    def get(self, value):
        return self.__dict__.get(value)


class Tag(db.Model):
    __tablename__ = "tag"

    tag_id = db.Column(db.Unicode(length=224), primary_key=True, unique=True)
    name = db.Column(db.String(128), nullable=False)
    products = db.relationship("Product", secondary=product_tags, back_populates="tags")
    descriiption = db.Column(db.Text)

    def __init__(self, *args, **kwargs):
        # super(db.Model, self).__init__(**kwargs)
        super(Tag, self).__init__(*args, **kwargs)
        self.tag_id = str(uuid.uuid4())

    def get_tags_options(self):
        return ["tag_id", "name", "products", "descriiption"]

    def get(self, value):
        return self.__dict__.get(value)
