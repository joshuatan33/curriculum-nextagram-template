from models.base_model import BaseModel
import peewee as pw
import datetime
from flask import render_template, request, flash
import re
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    name = pw.CharField(unique=False, null=False)
    password = pw.CharField(unique=False, null=False)
    email = pw.CharField(unique=True, null=False)

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_email:
            self.errors.append('Email already used')

        res = self.password_validate(self.password)
        if res:
            self.password = generate_password_hash(self.password)
        else:
            self.errors.append(res)

    @classmethod
    def password_validate(self, password):
        if (len(password) < 6) or (len(password) > 12):
            return 'Password must be between 6 and 12 characters!'
        elif not re.search("[a-z]", password):
            return 'Password must contain a lower case characters!'
        elif not re.search("[A-Z]", password):
            return 'Password must contain a UPPER case characters!'
        elif not re.search("[0-9]", password):
            return 'Password must contain a numerical characters!'
        else:
            return True

    def login_validate(self, current_password):
        self.errors = []

        password_to_check = current_password
        hashed_password = self.password

        res = check_password_hash(hashed_password, password_to_check)
        print(res)

        if res == True:
            return True
        else:
            print("errors")
            self.errors.append('Wrong password')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
