"""
    Module works using flask sqlalchemy and its classes are accepted as arguments in the respective functions...   """

# import numpy
from flask import redirect
import flash_errors as fe
from random import choice

class User():
    
    def __init__(self,user_contact, user_name, sno, is_admin = False):
        self.contact = user_contact
        self.is_admin = is_admin
        self.user_name = user_name
        self.user_id = sno
        

    def is_active(self):
        return True

    def get_id(self):
        return {"id":self.user_id , "contact":self.contact, "name":self.user_name}

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
        
    def __str__(self):
        return f'{self.user_id} , {self.contact}, {self.user_name}'


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

def get_public_key(dbase ,db ):
    # return "hp"
    try:
        list =[]
        check_in_datbase = dbase.query.all()
        list.append(check_in_datbase.previous_hash)
        return list
    except :
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

def add_transaction(db, dbase , values, id,currentHash, previousHash, session):
    """If there is  no problem in creating a account..."""
    try:
        enter_values = dbase(current_hash = currentHash , previous_hash = previousHash,no_devotee = values['people'],
            user_id = id , ticket_amount = (values['people'])*(values['price']), date_booking = values['date'], slot_booking = values['slot'])

        db.session.add(enter_values)
        db.session.commit() 
        fe.trans_suc()  
        print("try se")         
        
        return redirect("/")

    except Exception:
        print("error")
        fe.server_contact_error()
        return redirect("/")


def get_key_pair(dbase, user_id):
    try:
        check_in_datbase = dbase.query.filter_by(id = user_id).first()
        if check_in_datbase != None :     
            print("database se")
            return check_in_datbase.public_key, check_in_datbase.private_key
        else:
            fe.user_not_found()
            print("user not found")
            return None, None

    except Exception:
        print("exception")
        fe.some_went_wrong() 
        return None, None