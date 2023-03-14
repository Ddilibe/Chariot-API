#!/usr/bin/env python3
""" Script for creating the views for prod blueprint """
import logging
from run import db
from . import prod
from flask import jsonify
from .models import Product, Tag
from auth.models import User
from utils.exception import ProductWithoutCreator

@prod.route('/prod/all', strict_slashes=False, methods=['GET'])
def get_all_product():
    info = {}
    info["Login"] = False
    if every := db.session.query(Product).all():
        logging.info(every)
        info['products'] = {}
        for i in range(len(every)):
            info['products'][i] = {}
            val = info['products'][i]
            instance = every[i]
            val["description"], val["name"] = instance.description, instance.name
            val["price"], val["in_stock"] = instance.price, instance.in_stock
            val["image"], val["tags"] = instance.image, [j.name for j in instance.tags]
            val['id'] = instance.prod_id
    else:
        info["products"] = "No product has been created"
    logging.debug(info)
    return jsonify(info), 200

@prod.route('/tag/all', strict_slashes=False, methods=['GET'])
def get_all_tags():
    info={}
    info['tags'], info["Login"] = {}, False
    if taggit := db.session.query(Tag).all():
        for i in range(len(taggit)):
            info["tags"][i] = {}
            val = info["tags"][i]
            instance = taggit[i]
            val['name'], val['id'] = instance.name, instance.tag_id
            val['description'] = instance.descriiption
    else:
        info["tags"] = "No tags has been created"
    return jsonify(info), 200

@prod.route('/prod/<prod_id>', strict_slashes=False, methods=['GET'])
def get_single_product(prod_id):
    info = {}
    info["product"], info["error"] = {}, {}
    try:
        single = db.session.query(Product).filter(Product.prod_id==prod_id).first_or_404()
        value = info['product']
        value['name'], value['id'] = single.name, single.prod_id
        value['price'], value['in_stock'] = single.price, single.in_stock
        value['description'], value['user'] = single.description, {}
        value['tags'], use = [tag for tag in single.tags], value['user']
        value['image'] = single.image
        try:
            logging.debug(f"Picture exists ")
            if user := User.query.filter(User.merchant_id==single.merchant_id).first_or_404():
                use["first_name"], use["last_name"] = user.first_name, user.last_name
                if user.profile_picture:
                    use["profile_picture"] = user.profile_picture
        except Exception as e:
            error_exixt = "It is impossible for a product to exist with a creator"
            info['error']['user existence'] = error_exixt
            del info["product"]
            raise ProductWithoutCreator
    except Exception as e:
        if e == ProductWithoutCreator:
            prod_exist = "Due to the absence of a user, It is impossible for a"
            prod_exist += "product to exist without a creator, in this case User"
            info["error"]["Product Existence"] = prod_exist
        info["error"]["Product Error"] = f"{prod_id} does not exist at this time"
    finally:
        logging.debug(f"This is it:{info}")
        return jsonify(info), 200

@prod.route('/tag/<tag_id>', strict_slashes=False, methods=['GET'])
def get_post_with_tag(tag_id):
    info = {}
    info["Login"] = False
    try:
        if tags := Tag.query.filter(Tag.tag_id==tag_id).first_or_404():
            info[tags.name], t = {}, 0
            for i in tags.products:
                info[tags.name][f"Product {t}"] = {
                    "name": t.name, "description": t.descrition
                }
    except Exception as e:
        info['Error'] = "Tag doesn't exists"
    finally:
        return jsonify(info), 200

@prod.route('/prod/c', strict_slashes=False, methods=["GET, UPDATE"])
def create_update_post():
    pass
