#!/bin/env python3
from auth.error import UserDoesNotExists, VariableNotInUserModel
from auth.models import User, GenderEnum, CreditCard
from config import config, basedir
from typing import Dict, Union
import sqlalchemy as DataBase
from run import config_name
from flask import Flask
from uuid import uuid4
import os


class DataLayer:
    
    def __init__(self, db: DataBase, app: Flask) -> None:
        self.db, self.app, self.config = db, app, config[config_name]
        self.user_1 = {
            'first_name': "Emeka", 'user_name': 'Emike', "last_name": "Eze", "user_id": str(uuid4()),
            'profile_picture': f"{os.getenv('MEDIASTORAGE')}/Emike/trerieeorieferf.jpeg",
            "password" : "Passwording", "country": "Nigeria", "phone_number": 2343455346,
            "gender": GenderEnum.male, "email_address": "emeka.ere@gmail.com"
        }
        self.update_user = {
            'first_name': "Chuks", 'user_name': 'Chiemzie', "last_name": "Mike",
            'profile_picture': f"{os.getenv('MEDIASTORAGE')}/Chiemezie/trerieeorieferf.jpeg",
            "country": "Nigeria", "phone_number": 23434553436,
            "gender": GenderEnum.male, "email_address": "chukschiemeze@gmail.com"
        }
        self.credit_card = {
            "number": 439898230783298, "exp_month": 9, "exp_year": 2024, "cvc": 438, "credit_card_id": str(uuid4())
        }
        
    
    def create_user(self, user_details: Dict[str, str|int]) -> None:
        new_user = User(**user_details)
        self.db.session.add(new_user)
        self.db.session.commit()
        self.app.logger.info("New User created")
        self.userid = User.query.filter_by(email_address=user_details['email_address']).first_or_404()
        
    def edit_user(self, user_id: str, name: str, value: str) -> None:
        if user := self.db.session.query(User).filter_by(user_id=user_id).one_or_none():
            if var := user.to_dict().get(name):
                setattr(user, name, value)
                self.db.session.commit()
                return
            raise VariableNotInUserModel
        raise UserDoesNotExists
    
    def delete_user(self, user_id: str) -> None:
        if user := self.db.session.query(User).filter_by(user_id=user_id).one_or_none():
            self.db.session.delete(user)
            self.db.session.commit()
            return 
        raise UserDoesNotExists
    
    def get_user(self, user_id: str)-> Union[User | None]:
        if user := self.db.session.query(User).filter(user_id==user_id).one_or_none():
            return user
        return None
    
    def rollover(self) -> None:
        self.db.session.close_all()
        
    def clean(self) -> None:
        os.remove(f"{basedir}/{self.config.DATABASENAME}")
        
    def create_credit_card(self, card_details: Dict[str, str|int], user: User) -> None:
        new_credit_card = CreditCard(**card_details)
        new_credit_card.user_id = user.user_id
        self.db.session.add(new_credit_card)
        self.db.session.commit()
        
    def get_credit_card(self, credit_card_id: str)-> Union[CreditCard | None]:
        if card := self.db.session.query(CreditCard).filter_by(credit_card_id=credit_card_id).one_or_none():
            return card
        return None