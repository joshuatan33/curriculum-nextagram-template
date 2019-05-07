from models.base_model import BaseModel
import peewee as pw
import datetime
from flask import render_template, request, flash
import re
from werkzeug.security import generate_password_hash


class User(BaseModel):
    name = pw.CharField(unique=False, null=False)
    password = pw.CharField(unique=False, null=False)
    email = pw.CharField(unique=True, null=False)

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_email:
            self.errors.append('Email already used')

        def password_validate(password):
            print(password)
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

        res = password_validate(self.password)
        if res == True:
            self.password = generate_password_hash(self.password)
        else:
            self.errors.append(res)
