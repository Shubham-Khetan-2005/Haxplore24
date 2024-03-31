from flask import flash

def user_beta_msti_nhi():
    return flash("error", "Something went wrong")
def some_went_wrong():
    return flash("error", "Something went wrong")
def login_success():
    return flash("success", "Loggen in successfully")
def acc_created():
    return flash("success", "Account created successfully")

def server_contact_error():
    return flash("error", "Problem in conecting to the server")
def acc_al_pres():
    return flash("error", "Account already present at the server")
def wrng_pass():
    return flash("error", "Either contact no. or passward is wrong")
def user_not_found():
    return flash("error", "User not found")