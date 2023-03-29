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
from utils.exception import UserNonExistError, InvalidKeyError
from utils.exception import ProductNotExistError, TagNotExistError


@prod.route('/prod/all', strict_slashes=False, methods=['GET'])
def get_all_product():
    """ Method for obtaining different product """
    info = {}
    info["Login"] = False
    every = db.session.query(Product).all()
    if every:
        logging.info(every)
        info['products'] = {}
        for i in range(len(every)):
            info['products'][i] = {}
            val = info['products'][i]
            instance = every[i]
            val = {
                "description": instance.description, "name": instance.name,
                "price": instance.price, "in_stock": instance.in_stock,
                "image": instance.image, "tags": [j.name for j in instance.tags],
                'id':instance.prod_id
            }
    else:
        info["products"] = "No product has been created"
    logging.debug(info)
    return jsonify(info), 200

@prod.route('/tag/all', strict_slashes=False, methods=['GET'])
def get_all_tags():
    """ Method for obtaining all tags """
    info={}
    info['tags'], info["Login"] = {}, False
    taggit = db.session.query(Tag).all()
    if taggit:
        for i in range(len(taggit)):
            info["tags"][i] = {}
            val = info["tags"][i]
            instance = taggit[i]
            val['name'], val['id'] = instance.name, instance.tag_id
            val['description'] = instance.descriiption
    else:
        info["tags"] = "No tags has been created"
    return jsonify(info), 200


# Section for the multiple method like get, put and delete for both product and tags


@prod.route('/prod/<prod_id>', strict_slashes=False, methods=['GET'])
def single_product_actions(prod_id):
    info = {}
    info["error"], info["product"] = {}, {}
    try:
        single = Product.query.filter_by(prod_id=prod_id).first_or_404()
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
            user = User.query.filter_by(
                merchant_id==single.merchant_id
            ).first_or_404()
            if user:
                use["first_name"], use["last_name"] = user.first_name, user.last_name
                if user.profile_picture:
                    use["profile_picture"] = user.profile_picture
        except Exception as e:
            error_exixt = "It is impossible for a product to exist with a creator"
            info['error']['user existence'] = error_exixt
            del info["product"]
            raise ProductWithoutCreator
        code = 201
    except Exception as e:
        if e == ProductWithoutCreator:
            prod_exist = "Due to the absence of a user, It is impossible for a"
            prod_exist += "product to exist without a creator, in this case User"
            code, info["error"]["Product Existence"] = prod_exist, 403
        info["error"]["Product Error"] = f"{prod_id} does not exist at this time"
    finally:
        logging.debug(f"This is it:{info}")
        return jsonify(info), code

@prod.route('/prod/<user_id>/u/<prod_id>', strict_slashes=False, methods=["PUT"])
def update_product(prod_id, user_id):
    """ Function for updating a product """
    try:
        user = user_has_loggedin(user_id)
        if not user.is_merchant:
            raise TypeError("User is not a merchant")
        single = db.session.query(Product).filter(
            Product.prod_id==prod_id
        ).first_or_404()
        value = info['product']
        keys = ["name", "description", 'id', "price", 'in_stock', 'tags', 'image']
        request_data, new_value = request.get_json(), {}
        for keys, value in request_data.items():
            if not (keys in Product.get_dict().keys()):
                info['error']['Invalid Key Error'] = f"{keys} is not a valid key in product"
                raise InvalidKeyError
            if not (single.get(keys) == value):
                new_value[keys] = value
        single.query.update(new_value)
        db.session.commit()
        info['product']["Update"],code = "Successful", 201
        info['product']["Updated Products"] = new_value.keys()
    except Exception as e:
        info['product']["Update"], code = "Failure", 401
    finally:
        return jsonify(info), code

@prod.route('/prod/<user_id>/d/<prod_id>', strict_slashes=False, methods=['DELETE'])
def delete_product(prod_id, user_id):
    """ Function for deleting a product """
    try:
        user = user_has_loggedin(user_id)
        if not user.is_merchant:
            raise TypeError("User is not a merchant")
        single = db.session.query(Product).filter(
            Product.prod_id==prod_id
        ).first_or_404()
        db.session.remove(single)
        info['product']['Delete'], code = "Successful", 201
    except Exception as e:
        info['product']['Delete'], code = "Failure", 401
    finally:
        return jsonify(info), code



@prod.route('/tag/<tag_id>', strict_slashes=False, methods=['GET', 'PUT', 'DELETE'])
def get_post_with_tag(tag_id):
    """ Function to get a post associated with a tag """
    info = {}
    info["error"], info['tags'] = {}, {}
    try:
        tags = Tag.query.filter(Tag.tag_id==tag_id).first_or_404()
        if tags:
            info[tags.name], t = {}, 0
            for i in tags.products:
                info[tags.name][f"Product {t}"] = {
                    "name": t.name, "description": t.descriiption
                }
        else:
            info['error']['No Tag'] = "Tag doesn't exists at this time"
            raise TagNotExistError
    except Exception as e:
        info['Error'] = "Tag doesn't exists"
    finally:
        return jsonify(info), 200

@prod.route('/tags/<user_id>/u/<tag_id>', strict_slashes=False, methods=['PUT'])
def update_tag(tag_id, user_id):
    """ Function for adding a prod to a tag """
    try:
        user = user_has_loggedin(user_id)
        tags = Tag.query.filter(Tag.tag_id==tag_id).first_or_404()
        if tags:
            request_data, new_value = request.get_json(), {}
            for keys, value in request_data.items():
                if not(keys in ['name', "description"]):
                    info['error']['Invalid Key Error'] = f"{keys} is not a valid key in Tags"
                    raise KeyError
                if not (tags.get(keys) == value):
                    new_value[keys] = value
            tags.query.update(new_value)
            db.session.commit()
            info['tags']['Update'] = "Successful"
            info['tags']['Updated Tags'] = new_value.keys()
        else:
            info['error']['No Tag'] = "Tag doesn't exists at this time"
            raise TagNotExistError
        code = 201
    except Exception as e:
            info['tags']['Update'], code = "Failure", 401
    finally:
        return jsonify(info), code

@prod.route('/tag/<user_id>/d/<tag_id>', strict_slashes=False, methods=['DELETE'])
def delete_tag(tag_id):
    """ Function for deleteing a tag """
    try:
        tags = Tag.query.filter(Tag.tag_id==tag_id).first_or_404()
        if tags:
            tags.delete()
            db.session.commit()
            info['tags']['Delete'] = "Successful"
        else:
            info['error']['No tag'] = "Tag doesn't not exists"
            raise TagNotExistError
        code = 201
    except Exception as e:
        info['tags']['delete'], code = "Failure", 401
    finally:
        return jsonify(info), code

# Section for creating a product and tag


@prod.route('/prod/<user_id>/c', strict_slashes=False, methods=["POST"])
def create_product(user_id):
    """ Function for creating a product """
    info = {}
    info["error"] = {}
    request_data = request.get_json()
    try:
        user = user_has_loggedin(user_id)
        for i in request_data.keys():
            if not(i in Product.get_dict().keys()):
                info['error']['Excess Data'] = f"{i} Not Accepted As An Input"
                raise ExcessProductInput
        for i in ["name", "price"]:
            if not (i in request_data.keys()):
                info['error']['Required Data'] = f"{i} not in requested data"
                raise RequiredDataError
        # if "image" in request_data:
        im = request_data.get("image")
        if im:
            if "image_name" in request_data:
                image_name, im = request_data.get("image_name"), bytes(im, 'utf-8')
                with open(image_name, 'rw') as file_name:
                    file_name.write(base64.b64decode((im)))
                request['image'] = image_name
            else:
                info['error']['image_name'] = "Image name is unavaliable"
                raise UnavaliableImageName
        if not user.is_merchant:
            info['error']['Not merchant'] = "User is not a merchant"
            raise ValueError
        request_data['merchant_id'] = user_id.merchant_id
        new_prod = Product(**request_data)
        db.session.add(new_prod)
        db.session.commit()
        info['Product'], code = {"id": new_prod.prod_id}, 200
        info["Created"], info["error"] = "Successful", None
    except Exception as e:
        info["Created"], code = "Failure", 401
    finally:
        return jsonify(info), code

@prod.route('/tags/<user_id>/c/', strict_slashes=False, methods=['POST'])
def create_tags(user_id):
    """ Function for creating a new tag """
    info = {}
    info['error'] = {}
    try:
        user = user_has_loggedin(user_id)
        request_data = request.get_json()
        for i in request_data.keys():
            if not (i in Tag.get_tags()):
                info["error"]['Key Error'] = f"Key {i} not a Tag attribute"
                raise KeyError
        prod_id = Product.query.filter_by(Product.prod_id==request_data['products']).first_or_404()
        if prod_id:
            new_user = prod_id
            del request_data['products']
        else:
            info['error']['Key Error'] = f"User doesn't exists in the database"
            raise UserNonExistError("User Doesn't exists")
        tags, code = Tag(**request_data), 201
        tags.products.append(new_user)
        db.session.add(tags)
        db.commit()
    except Exception as e:
        info['error']['created'], code = "Failure", 401
    finally:
        return jsonify(info), code


#  Section for adding a tag to a product and removing tags from product
@prod.route('/prod/<user_id>/<prod_id>/<tag_id>', strict_slashes=False, methods=['PUT', "DELETE"])
def actions_for_product_and_tag(prod_id, tag_id):
    """ Function for adding tags to products and for removing
    products from tags """
    info, jam = {}, request.method
    info['Login'], info['product'], info['tags'], info['error'] = False, {}, {}, {}
    try:
        if request.method == "PUT":
            single = Product.query.filter_by(Product.prod_id==prod_id).first_or_404()
            tags = Tag.query.filter_by(Tag.tag_id==tag_id).first_or_404()
            single.tags.append(tags)
            db.session.commit()
            info['tags']['Added Tag'] = "Successful"
            info['product']['New Tag'] = "Successful"
        if request.method == "DELETE":
            single = Product.query.filter_by(Product.prod_id==prod_id).first_or_404()
            tags = Tag.query.filter_by(Tag.tag_id==tag_id).first_or_404()
            if not (tags in single.tags):
                info['error']['No Tag in product'] = "Tag doesn't exist in the product"
                raise TagNotExistError
            single.tags.remove(tags)
            db.session.commit()
            info['product']['Removed Tag'] = "Successful"
            info['tags']['Tag Removed'] = "Successful"
    except Exception as e:
        if jam == "PUT":
            info['product']['New Tag'] = "Failure"
            info['tags']['Added Tag'] = "Failure"
        if jam == "DELETE":
            info['product']['Removed Tag'] = "Failure"
            info['tags']['Tag Removed'] = "Failure"
        info['error'], code = json.loads(e), 401
    finally:
        return jsonify(info), code

def user_has_loggedin(user_id):
    """Function for obtaining a user who login in"""
    logging.info("Testing the decorated function")
    email = redis_cli.get(user_id)
    if not email:
        raise UserNotLoggedIn("User Has Not LoginIn")
    email = email.decode("utf-8")
    user = User.query.filter_by(email_address=email).first_or_404()
    return user
