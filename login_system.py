"""
    Module works using flask sqlalchemy and its classes are accepted as arguments in the respective functions...   """

# import numpy
from flask import redirect
import flash_errors as fe
from random import choice

class User():
    
    def __init__(self,user_contact, sno, is_admin = False):
        self.contact = user_contact
        self.is_admin = is_admin
        self.user_id = sno
        

    def is_active(self):
        return True

    def get_id(self):
        return {"id":self.user_id , "contact":self.contact}

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

def get_details(user_contact, dbase):
    try:
        check_in_datbase = dbase.query.filter_by(contact = user_contact).first()
        if check_in_datbase != None :    
            return check_in_datbase
        else:
            return None

    except Exception:
        fe.some_went_wrong() 
        return None

def check_in_t_db(user_contact ,session_var , dbase , db ,session):

    try:
        check_in_datbase = dbase.query.filter_by(contact = user_contact).first()
        if check_in_datbase != None :     
            return check_in_datbase
        else:
            fe.user_not_found()
            return None

    except Exception:
        session[session_var] = {"contact":user_contact}
        fe.some_went_wrong() 
        return None