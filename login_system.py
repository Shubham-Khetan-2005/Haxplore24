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

def find_account(email,dbase1 , dbase2):

    try:
        
        st_account = dbase1.query.filter_by(user_email = email).first()
        if st_account == None:
            t_account = dbase2.query.filter_by(user_email = email).first()

            if t_account == None:
                fe.login_err()            
                return None , None

            return (t_account  , "Teacher")
        return (st_account , "Student")

    except Exception:

        # fe.server_contact_error()
        return "Problem in contacting" , None


def get_user_details(dbase,dbase2,role,sno):

    try:
        if role == "Teacher":
            user_account = dbase2.query.filter_by(sno = sno).first()
            if user_account == None :
                return None , None
            return user_account.user_name , user_account.user_email
        elif role == "Student":
            user_account = dbase.query.filter_by(sno = sno).first()
            if user_account == None :
                return None , None
            return user_account.user_name , user_account.user_email
        return None , None
        
    except Exception:

        # fe.server_contact_error()        
        return None , None


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