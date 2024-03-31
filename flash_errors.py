from flask import flash

def user_beta_msti_nhi():
    return flash("error", "Something went wrong")
def login_success():
    return flash("success", "Loggen in successfully")