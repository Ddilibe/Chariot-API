#!/usr/bin/env python3
""" Script for the models for the cart """
import uuid
from . import cart
from run import db
from auth.models import User
from prod.models import Product
from utils.exception import NotProductInstance


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Unicode, primary_key=True)
    user_id = db.Model.mapped_column(db.ForeignKey("User.id"))
    user = db.relationship('User', back_populates='cart')
    products = []

    def __init__(self, *args, **kwargs):
        super(Cart, self).__init__(*args, **kwargs)
        self.id = str(uuid.uuid4())

    def add_item(self, value):
        if isinstance(Product, value['name']):
            if not (value in self.product):
                new_value = value['name']
                setattr(new_value, "number", value['number'])
                self.products.append(value)
            else:
                prod = [i for i in self.products if i['name'].prod_id == value['name'].prod_id][0]
                prod.number += value['number']
            return
        raise NotProductInstance

    def remove_item(self, value):
        if isinstance(Product, value):
            self.product.remove(value)
            return
        raise NotProductInstance

    def display_item(self):
        info, y = {"Products": {}}, 0
        for prod in self.products:
            y += 1
            info['Products'][y] = {}
            for value in ['name', "description", "price", "image"]:
                info['Products'][y][value] = prod['name'].get(value)
        return info

    def get_item(self, value):
        return [i for i in self.products if i['name'].prod_id == value['name'].prod_id][0]
