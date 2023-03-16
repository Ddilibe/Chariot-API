#!/usr/bin/env python3
""" Script for creating the views for prod blueprint """
import logging
from run import db
from . import prod
from auth.models import User
from flask import jsonify, request
from .models import Product, Tag, ProductImage
from utils.exception import ProductWithoutCreator, ExcessProductInput
from utils.exception import UnavaliableImageName, RequiredDataError
from utils.exception import UserNonExistError


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

@prod.route('/prod/<prod_id>', strict_slashes=False, methods=['GET', 'PUT', 'DELETE'])
def get_single_product(prod_id):
    info = {}
    info["product"], info["error"] = {}, {}
    try:
        single = db.session.query(Product).filter(Product.prod_id==prod_id).first_or_404()
        value = info['product']
        keys = ["name", "description", 'id', "price", 'in_stock', 'tags', 'image']
        for i in keys:
            if i == "tags":
                value[i] = [tag for tag in single.tags]
                continue
            value[i] = single.get(i)
        value['user'] = {}
        use = value['user']
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

@prod.route('/tag/<tag_id>', strict_slashes=False, methods=['GET', 'PUT', 'DELETE'])
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

@prod.route('/prod/c', strict_slashes=False, methods=["POST"])
def create_product():
    info = {}
    info["error"] = {}
    request_data = request.get_json()
    try:
        for i in request_data.keys():
            if not(i in Product.get_dict().keys()):
                info['error']['Excess Data'] = f"{i} Not Accepted As An Input"
                raise ExcessProductInput
        for i in ["name", "price"]:
            if not (i in request_data.keys()):
                info['error']['Required Data'] = f"{i} not in requested data"
                raise RequiredDataError
        # if "image" in request_data:
        if im := request_data.get("image"):
            if "image_name" in request_data:
                image_name, im = request_data.get("image_name"), bytes(im, 'utf-8')
                with open(image_name, 'rw') as file_name:
                    file_name.write(base64.b64decode((im)))
                request['image'] = image_name
            else:
                info['error']['image_name'] = "Image name is unavaliable"
                raise UnavaliableImageName
        new_prod = Product(**request_data)
        db.session.add(new_prod)
        db.session.commit()
        info['Product'], code = {"id": new_prod.prod_id}, 200
        info["Created"], info["error"] = "Successful", None
    except Exception as e:
        info["Created"], code = "Failure", 401
    finally:
        return jsonify(info), code

@prod.route('/tags/c/', strict_slashes=False, methods=['POST'])
def create_tags():
    info = {}
    info['error'] = {}
    try:
        if request_data := request.get_json():
            for i in request_data.keys():
                if not (i in Tag.get_tags()):
                    info["error"]['Key Error'] = f"Key {i} not a Tag attribute"
                    raise KeyError
            if prod_id = Product.query.filter_by(Product.prod_id==request_data['products']).first_or_404():
                new_user = prod_id
                del request_data['products']
            else:
                info['error']['Key Error'] = f"User doesn't exists in the database"
                raise UserNonExistError('User Doesn't exists)
            tags = Tag(**request_data)
            tags.products.append(new_user)
            db.session.add(tags)
            db.commit()
    except Exception as e:
        info['error']['created'] = "Failure"
    finally:
        return jsonify
