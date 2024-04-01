from flask import flash

def user_beta_msti_nhi():
    return flash(("error", "Something went wrong"))
def some_went_wrong():
    return flash(("error", "Something went wrong"))
def login_success():
    return flash(("success", "Logged in successfully"))
def acc_created():
    return flash(("success", "Account created successfully"))
def trans_suc():
    return flash(("success", "Your ticket has been genrated successfully"))

def server_contact_error():
    return flash(("error", "Problem in conecting to the server"))
def acc_al_pres():
    return flash(("error", "Account already exists"))
def wrng_pass():
    return flash(("error", "Either contact no. or passward is wrong"))
def user_not_found():
    return flash(("error", "User not found"))
def dnt_ac():
    return flash(("error", "You do not have access to this page"))