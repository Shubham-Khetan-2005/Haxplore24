from flask import Flask, render_template, request, redirect , url_for, session, jsonify , Response , send_file
from flask_login import LoginManager , login_required , login_user , logout_user  , current_user
from flask_sqlalchemy import SQLAlchemy
import login_system as ls
from ecdsa import SigningKey
from argon2 import PasswordHasher
from Blockchain.blockChain import BlockChain
from Blockchain.transaction import Transaction

ph=PasswordHasher()
mychain=BlockChain()
MAX_TRANSACTIONS=1 
app =Flask(__name__)
# db = SQLAlchemy(app)

app.secret_key = "super-secret-key"
app.config['SECRET_KEY'] = '12345'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
publicKeys=set()
# Fetch all publicKey from dataset and store in publicKey

# Binding both the databses to the sqlalchemy uri...
# SQLALCHEMY_BINDS = {
#     'haxplore':        'mysql://root:@localhost/haxplore',
# }
# app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS

# defining model
# class Users(db.Model):
    
#     # Students information table class...
#     __tablename__ = 'users'

#     """
#     Data base (users) rows structure -
#     private_key , id  , name , contact , password_hash, public_key
#     """

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(), nullable=False)
#     contact = db.Column(db.String(), nullable=False)
#     password_hash = db.Column(db.String(), nullable=False)
#     private_key = db.Column(db.String(), nullable=False)
#     public_key = db.Column(db.String(), nullable=False)



def to_string(key,isPublic):
    if isPublic:
        return key.to_pem()[len(b"-----BEGIN PUBLIC KEY-----\n"):-len(b"\n-----END PUBLIC KEY-----\n")].decode()
    return key.to_pem()[len(b"-----BEGIN EC PRIVATE KEY-----\n"):-len(b"\n-----END EC PRIVATE KEY-----\n")].decode()

def to_pem(key_str,isPublic):
    if isPublic:
        return b"-----BEGIN PUBLIC KEY-----\n"+key_str.encode()+b"\n-----END PUBLIC KEY-----\n"
    return b"-----BEGIN EC PRIVATE KEY-----\n"+key_str.encode()+b"\n-----END EC PRIVATE KEY-----\n"

def remove_escapeChar(word):
    res=""
    for i in word:
        if i not in ['\n','\t','\r','\b']:
            res+=i

    return res
def generateKeypair():
    print("Generating Key")
    n=len(publicKeys)
    privateKey=publicKey=None
    while n==len(publicKeys):
        privateKey=SigningKey.generate()
        publicKey=privateKey.verifying_key
        publicKeys.add(to_string(publicKey,True))
    return privateKey,publicKey

@login_manager.user_loader
def load_user(details):
    
    user_id = details["user"]
    user_role = details["role"]
    dict = {'user_id' : user_id, 'user_role':user_role}
    return 


@app.errorhandler(404) 
def not_found(e): 
    return render_template("404.html")


@app.route("/", methods = ['GET'])
def index():
    return "index"

@app.route("/login", methods = ['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("contact")
        password = request.form.get("password")

        user_name = ""
        user_email = ""
        user_id = ""

        # login_user(user_to_log)
        # fs.login_success()

        return redirect(url_for("index"))

    return "index"

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return "signup"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
