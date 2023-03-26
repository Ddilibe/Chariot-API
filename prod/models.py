#!/usr/bin/env python3
""" Script for the model of product for the ecommerce API """
import json
import uuid
import base64
import enum
from . import prod
from os.path import join
from run import db, TEMP_PATH
from utils.exception import UnavaliableImageName
from sqlalchemy_media import Image, ImageAnalyzer
from sqlalchemy_media import ImageValidator, ImageProcessor


class ProductImage(Image):
    """
    Class for processing image storage for sqlalchemy
    """

    __pre_processors__ = [
        ImageAnalyzer(),
        ImageValidator(
            minimum=(80, 80),
            maximum=(800, 600),
            content_types=["image/jpeg", "image/png"],
        ),
        ImageProcessor(fmt="jpeg", width=120),
    ]


class Json(db.TypeDecorator):
    """
    Json Type decorator for sqlalchemy
    """

    impl = db.Unicode

    def process_bind_param(self, value, engine):
        return json.dumps(value)

    def process_result_value(self, value, engine):
        return json.loads(value) if value else None


class ProductType(enum.Enum):
    """
    Class for enumerating the type product is created
    """

    dig = "digital"
    phy = "physical"


# Variable connecting product and tag many to many connection
product_tags = db.Table(
    "product_tag",
    db.Model.metadata,
    db.Column("Product_id", db.Unicode, db.ForeignKey("product.prod_id")),
    db.Column("Tag_id", db.Unicode, db.ForeignKey("tag.tag_id")),
)


class Product(db.Model):
    """
    A class for the product table

    __tablename__ = The name of the table
    prod_id = The id of any product instance created
    name = The column for the name of the product created
    sku = The sku for the product created
    description = The column for the description of any product created
    price = The column for the price of any product created
    in_stock = The column for the number of product in stock
    merchant_id = A many to one relationship of many product and one merchant
    tags = A many to many relationship between a user product and many tags
    image = A column for containing the image of the product
    shipable = A column for containing the shipability of a product
    package_dimension = The column containing the package dimension
    time_created = The column containing the time the product was created
    time_updated = The column containing the time the product was updated
    currency = The column containing the currency of the product
    """

    __tablename__ = "product"

    prod_id = db.Column(db.Unicode(length=225), primary_key=True, unique=True)
    name = db.Column(db.String(128), nullable=False)
    sku = db.Column(db.String(128), nullable=True, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    in_stock = db.Column(db.Integer, default=0)
    merchant_id = db.Column(db.Integer, db.ForeignKey("User.merchant_id"))
    tags = db.relationship(
        "Tag",
        secondary=product_tags,
        back_populates="products"
    )
    image = db.Column(ProductImage.as_mutable(Json))
    shipable = db.Column(db.Boolean, nullable=False)
    package_dimension = db.Column(db.String(20), nullable=False)
    time_created = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now()
    )
    time_updated = db.Column(
        db.DateTime(timezone=True),
        onupdate=db.func.now()
    )
    currency = db.Column(db.String(20), default="usd")

    def __init__(self, *args, **kwargs):
        """
        Initializing fucntion for the class
        Args:
            :params: args[list] - List argument of the function
            :params: kwargs[dict] - Dictionary argument of the function
        Return:
            There is no return value for this function

        Kwargs will be in the form:
        {
            "name": "Name of product",
            "description": "Description of the product",
            "price": "Price of the product"
            "package_dimension": []
            "shipable": True
            "in_stock": "Number of product in stock",
            "image": [
                {
                    "Image_type": "Link or converted binary",
                    "image": "string or url"
                },
                {
                    "Image_type": "Link or converted binary(covbin)",
                    "image": "string or url"
                    "image_name"
                },
            ]
        }
        """
        super(Product, self).__init__(*args, **kwargs)
        self.prod_id = str(uuid.uuid4())
        self.sku = kwargs["name"].replace(" ", "-")
        if "image_name" in kwargs.keys():
            self.image = ProductImage.create_from(kwargs['image'])

    @classmethod
    def get_dict(cls):
        # with open(self.)
        # with open(TEMP_PATH, self.image.path) as im:
        # image = self.image.get_thumbnail(ratio=3, auto_generate=True)
        return cls.__dict__

    def get(self, value):
        """
        Method for obtaining a value in the class
        Args:
            :params: Value[str] - Name of the argument to
            be obtained
        Return:
            The method returns the value to be obtained or nothing
        """
        return self.__dict__.get(value)


class Tag(db.Model):
    """
    A class for the tag table
    Class Args:
        tag_id = The id for every instance of the product created
        name = The column for the name of the tag created
        products = The column for a many to many relationship between a
        product and a tag
        decriiption = The column for the description of the tag created
    """

    __tablename__ = "tag"

    tag_id = db.Column(db.Unicode(length=224), primary_key=True, unique=True)
    name = db.Column(db.String(128), nullable=False)
    products = db.relationship(
        "Product",
        secondary=product_tags,
        back_populates="tags"
    )
    descriiption = db.Column(db.Text)

    def __init__(self, *args, **kwargs):
        """
        Initializing fucntion for the class
        Args:
            :params: args[list] - List argument of the function
            :params: kwargs[dict] - Dictionary argument of the function
        Return:
            There is no return value for this function
        """
        super(Tag, self).__init__(*args, **kwargs)
        self.tag_id = str(uuid.uuid4())
        self.descriiption = kwargs.get("description")

    def get_tags_options(self):
        """
        Method for obtaining the keys of a tag
        Args:
            No argument
        Return:
            Returns the keys of tag class
        """
        return ["tag_id", "name", "products", "descriiption"]

    def get(self, value):
        """
        Method for obtaining a value in the class
        Args:
            :params: Value[str] - Name of the argument to
            be obtained
        Return:
            The method returns the value to be obtained or nothing
        """
        return self.__dict__.get(value)
