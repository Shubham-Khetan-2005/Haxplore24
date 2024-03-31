from flask import flash , redirect 

def get_values(request , *args):

    return_values = []
    
    for item in args :
        return_values.append(request.form.get(item))
    
    return return_values

def add_account(db, dbase , user_name , user_contact  , passwordHash , privateKey, publicKey ,session, path):
    """If there is  no problem in creating a account..."""
    try:
        enter_values = dbase(name = user_name , contact = user_contact,
            password_hash = passwordHash ,
            public_key = publicKey, private_key = privateKey)

        db.session.add(enter_values)
        db.session.commit() 

        # fs.acc_created()           
        
        return None

    except Exception:

        # fe.server_contact_error()

        return redirect(path)


def check_in_t_db(name , contact , email , path ,session_var , dbase , db , params,session):
    try:
        check_in_datbase = dbase.query.filter_by(user_email = contact).first()

        if check_in_datbase != None :
            values = {"name":name, "contact": contact}
            session[session_var] = values        
            return redirect(path)
        else:
            return None

    except Exception:
        # fe.server_contact_error()
        values = {"name":name,"contact": contact}
        session[session_var] = values  
        return redirect(path) 