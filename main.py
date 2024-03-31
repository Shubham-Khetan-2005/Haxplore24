from flask import Flask, render_template, request, redirect , url_for, session, jsonify , Response , send_file
from flask_login import LoginManager , login_required , login_user , logout_user  , current_user
from flask_sqlalchemy import SQLAlchemy
import login_system as ls
from ecdsa import SigningKey
from argon2 import PasswordHasher
from Blockchain.blockChain import BlockChain,Block
from Blockchain.transaction import Transaction
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import pymysql
pymysql.install_as_MySQLdb()
import signup as si
import re
import flash_errors as fe

ph=PasswordHasher()
MAX_TRANSACTIONS=1 
app =Flask(__name__)
# Binding both the databses to the sqlalchemy uri...

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/haxplore'
db = SQLAlchemy(app)
admin = Admin(app)
app.secret_key = "super-secret-key"
app.config['SECRET_KEY'] = '12345'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
publicKeys=set()
# Fetch all publicKey from dataset and store in publicKey
# defining model
class Users(db.Model):
    
    # Students information table class...
    __tablename__ = 'users'

    """
    Data base (users) rows structure -
    private_key , id  , name , contact , password_hash, public_key
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    contact = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    private_key = db.Column(db.String(), nullable=False)
    public_key = db.Column(db.String(), nullable=False)

class mandir_1(db.Model):
    
    # Students information table class...
    __tablename__ = 'mandir_1'


    current_hash = db.Column(db.String(), primary_key=True)
    previous_hash = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    ticket_amount = db.Column(db.Integer, nullable=False)
    date_booking = db.Column(db.Date(), nullable=False)
    slot_booking = db.Column(db.String(), nullable=False)

class mandir_2(db.Model):
    
    # Students information table class...
    __tablename__ = 'mandir_2'


    current_hash = db.Column(db.String(), primary_key=True)
    previous_hash = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    ticket_amount = db.Column(db.Integer, nullable=False)
    date_booking = db.Column(db.Date(), nullable=False)
    slot_booking = db.Column(db.String(), nullable=False)

class mandir_3(db.Model):
    
    # Students information table class...
    __tablename__ = 'mandir_3'


    current_hash = db.Column(db.String(), primary_key=True)
    previous_hash = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    ticket_amount = db.Column(db.Integer, nullable=False)
    date_booking = db.Column(db.Date(), nullable=False)
    slot_booking = db.Column(db.String(), nullable=False)
mydb={"Ram_Mandir":mandir_1,"Akshardam":mandir_2,"Murdeshwar":mandir_3}

admin.add_view(ModelView(Users,db.session,endpoint='naitik'))


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
    
    user_contact = details["contact"]
    user_id = details["id"]
    user_name = ls.get_details(user_contact, Users)

    if(user_name == None):
        return
    return ls.User(user_contact, user_id, user_name)


@app.errorhandler(404) 
def not_found(e): 
    return render_template("404.html")


@app.route("/", methods = ['GET'])
def index():
    return render_template("transaction.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        

        user_contact, user_password = ls.get_values(request, 'contact', 'password')
        if None in (user_contact,user_password) or "" in (user_contact,user_password) :
            fe.user_beta_msti_nhi()
            return redirect("/login")
        
        if not (bool(re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" , user_password))):
            fe.user_beta_msti_nhi()
            return redirect("/login")

        user_account = ls.check_in_t_db(user_contact, "log-details", Users, db, session)
        
        if(user_account == None):
            redirect(url_for("login"))
        
        if(not ph.verify(user_account.password_hash, user_password)):
            fe.wrng_pass()
            session['log-details'] = user_password
            redirect(url_for("login"))
        
        user_contact = user_account.contact
        user_id = user_account.id
        user_to_log = ls.User(user_contact, user_id)

        login_user(user_to_log)
        fe.login_success()

        return redirect(url_for("index"))

    if "log-details" in session:
        return_contact = session["log-details"]
        session.pop("log-details")
    else:
        return_contact = ""

    return render_template("login.html", values = {'contact' : return_contact})

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == 'POST' :

        name,contact,password = si.get_values(request , 'name' , 'contact' ,'password')

        if None in (name,contact,password) or "" in (name,contact,password) :
            fe.some_went_wrong()
            return redirect("/signup")
        
        if not (bool(re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" , password))):
            fe.some_went_wrong()
            return redirect("/signup")
        
        account_presence = si.check_in_t_db(name , contact ,  request.path , "acc_requested", Users , db  , session)

        if  account_presence != None:
            return account_presence  
        
        passwordHash=ph.hash(password)
        privateKey,publicKey=generateKeypair()

        add_details = si.add_account(db , Users , name , contact , passwordHash, privateKey, publicKey, session, "acc_requested", url_for('signup'))
 
        if add_details != None:
            return add_details  
        else:
            return redirect(url_for('index'))
        
    val = {'name' : "", 'contact':""}

    if "acc_requested" in session:
        val = session['acc_requested']
        session.pop("acc_requested")


    return render_template("sign-up.html", values = val)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
@app.route("/online_darshan")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/transaction/<string:slug>",methods=['GET','POST'])
@login_required
def transaction(slug):
    if current_user.is_authenticated:
        return render_template("transaction.html")
    if request.method=="POST":
        publicKey,privateKey=ls.get_key_pair(Users,current_user.user_id)
        if not (publicKey & privateKey): redirect('/')
        try:
            tx=Transaction(remove_escapeChar(to_string(publicKey,True)),"SYSTEM",int(session["amount"]))   
            tx.sign((privateKey,publicKey))
            difficulty=4;
            block=Block(transactions=[tx],previousHash=mydb[slug].getLatestBlock().hash)
            block.mineBlock(difficulty,"SYSTEM")
            # mydb[slug].add(block) #add block to db
        except Exception as e:
            print(e)
        
        
    


if __name__ == "__main__":
    app.run(debug=True)
