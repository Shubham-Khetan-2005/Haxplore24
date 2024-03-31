"""
    Module works using flask sqlalchemy and its classes are accepted as arguments in the respective functions...   """

# import numpy
from flask import redirect
import string
from random import choice

class User():
    
    def __init__(self,user_name,user_email,is_admin,sno, user_contact):
        self.name = user_name
        self.email = user_email
        self.contact = user_contact
        self.is_admin = is_admin
        self.user_id = sno
        

    def is_active(self):
        return True

    def get_id(self):
        return {"user":self.user_id , "role":self.role}

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
        
    def __str__(self):
        return f'{self.name} , {self.email} , {self.role}'


def get_values(request , *args):

    return_values = []
    
    for item in args :
        return_values.append(request.form.get(item))
    
    return return_values

    try:

        user_name = account.user_name
        phone_no = account.user_phone
        email = account.user_email

        if role == "Student":
            enter_values = dbase(user_name = user_name, user_phone = phone_no, user_email = email , user_password = password)

        elif role == "Teacher":
            enter_values = dbase2(user_name = user_name, user_phone = phone_no, user_email = email , user_password = password)

        db.session.add(enter_values)
        db.session.delete(account)
        db.session.commit()
        return None

    except Exception:
        fe.server_contact_error()
        return "Problem In Contacting"