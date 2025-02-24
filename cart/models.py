#!/usr/bin/env python3
""" Script for the models for the cart """
import uuid
import requests
from . import cart
from run import db
from auth.models import User
from prod.models import Product
from utils.exception import NotProductInstance


class CartItem(db.Model):
    """
    Table for items in the cart

    Class Args:
        __tablename__ = The name of the table
        id = The column for the id of an instance of the table
        product_id = The id for the product in the column
        quantity = The quantity of item the product in the cart
        cart_id = A many_to_one relationship between a cart item and
        a cart
    """

    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.prod_id"),
        nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)


class Cart(db.Model):
    """
    Table for cart

    Class Args:
        __tablename__ = The name of the table
        id = The id of the instance of the table created
        user_id = A one_to_one relationship between a user and a cart
        user = A column complementing the one_to_one relationship
        items = A column representing a one to many relationship between
        a cart and an item in the cart
    """

    __tablename__ = "cart"

    id = db.Column(db.Unicode, primary_key=True)
    user_id = db.Column(db.String(228), db.ForeignKey("User.user_id"), unique=True)
    user = db.relationship("User", back_populates="cart")
    items = db.relationship("CartItem", backref="cart", lazy=True)

    def __init__(self, *args, **kwargs):
        """
        Method for initializing the class instance
        Args:
            :params: *args[list] - List argument
            :params: **kwargs[dict] - Dictionary argument
        Return:
            There is no return value
        """
        super(Cart, self).__init__(*args, **kwargs)
        self.id = str(uuid.uuid4())

    def add_item(self, value):
        """
        Method for adding an item to the cart of a
        particular user
        Args:
            :params: value[Product] - Argument instance of a product
        Return:
            There is no return value
            It just updates the instance in the database
        """
        new_id = value["name"]
        new_product = Product.query.filter_by(prod_id=new_id).first_or_404()
        if not (new_product in self.items):
            curr_from = new_product.get("currency")
            curr_to = self.user.currency
            if curr_to != curr_from:
                setattr(
                    new_product,
                    "price",
                    self.change_currency(
                        curr_from,
                        curr_to,
                        new_product.get("price")
                    ),
                )
            setattr(new_product, "number", value["number"])
            new_cart_item = CartItem(
                product_id=new_product.prod_id,
                quantity=value["number"],
                cart_id=self.id,
            )
            db.session.add(new_cart_item)
        else:
            ci = self.items.query.filter_by(id=new_product.id).first_or_404()
            ci.quantity += value["number"]
        db.session.commit()

    def remove_item(self, value):
        """
        Method to remove an item from the cart of a particular user
        Args:
            :params: value[Product] - argument instance of product
        Return:
            The return is to specify an end to the loop
        """
        for item in self.items:
            if item.product_id == value.prod_id:
                db.session.delete(item)
                db.session.commit()
                return

    def display_item(self):
        """
        Method for displaying all the items in the cart
        Args:
            There is no arguemtent
        Return:
            Returns a dictionary of all products in the cart of a
            particular user
        """
        info, y = {"Products": {}}, 0
        for prod in self.items:
            info["Products"][y] = {}
            prod = Product.query.filter_by(
                prod_id=prod.product_id
            ).first_or_404()
            for value in ["id", "name", "description", "price", "image"]:
                info["Products"][y][value] = prod["name"].get(value)
            y += 1
        return info

    def change_currency(self, curr_from, curr_to, amt):
        """
        Method for changing the currency of the product before
        adding it to cart
        Args:
            :params: curr_from[str] - intial currency for the product
            :params: curr_to[str] - Currency to change it to
            :params: amt[float] - Number the currency is converted to
        Return:
            This method returns converted currenct if it converts
        """
        try:
            currency_api_key = os.environ.get("CURRENCY_API_KEY")
            url = (
                f"https://api.exchangeratesapi.io/latest?access_key="
            )
            url += f"{currency_api_key}"
            url += f"&base={curr_from.upper()}&symbols={curr_to.upper()}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                conversion_rate = data["rates"][curr_to.upper()]
                converted_amount = amt * conversion_rate
            else:
                converted_amount = amt
        except Exception as e:
            converted_amount = amt
        finally:
            return converted_amount
