from flask import flash , redirect 
import flash_errors as fe

def get_values(request , *args):

    return_values = []
    
    for item in args :
        return_values.append(request.form.get(item))
    
    return return_values

def add_account(db, dbase , user_name , user_contact  , passwordHash , privateKey, publicKey ,session, session_var, path):
    """If there is  no problem in creating a account..."""
    try:
        print(user_contact)
        enter_values = dbase(name = user_name , contact = user_contact,
            password_hash = passwordHash ,
            public_key = publicKey, private_key = privateKey)

        db.session.add(enter_values)
        db.session.commit() 
        print(user_contact)

        fe.acc_created()           
        
        return None

    except Exception:

        fe.server_contact_error()
        values = {"name":user_name,"contact": user_contact}
        session[session_var] = values 
        return redirect(path)


def check_in_t_db(name , user_contact , path ,session_var , dbase , db ,session):
    check_in_datbase = dbase.query.filter_by(contact = user_contact).first()
    print(check_in_datbase)
    try:
        if check_in_datbase != None :
            values = {"name":name, "contact": user_contact}
            session[session_var] = values   
            fe.acc_al_pres()     
            return redirect(path)
        else:
            return None

    except Exception:
        fe.server_contact_error()
        values = {"name":name,"contact": user_contact}
        session[session_var] = values  
        return redirect(path) 