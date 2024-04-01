from flask import Flask, render_template, request, redirect , url_for, session, jsonify , Response, send_file, make_response
from flask_login import LoginManager , login_required , login_user , logout_user  , current_user
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
import login_system as ls
import pdfkit
from ecdsa import SigningKey
from argon2 import PasswordHasher
from Blockchain.blockChain import BlockChain,Block
from Blockchain.transaction import Transaction
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import pymysql
from io import BytesIO
pymysql.install_as_MySQLdb()
import signup as si
import re
import flash_errors as fe
import ecdsa

ph=PasswordHasher()
MAX_TRANSACTIONS=1 
app =Flask(__name__)
QRcode(app)
# Binding both the databses to the sqlalchemy uri...

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/haxplore'
db = SQLAlchemy(app)
admin = Admin(app)
app.secret_key = "super-secret-key"
app.config['SECRET_KEY'] = '12345'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

pk=set()
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
    no_devotee = db.Column(db.Integer, nullable=False)

class mandir_2(db.Model):
    
    # Students information table class...
    __tablename__ = 'mandir_2'


    current_hash = db.Column(db.String(), primary_key=True)
    previous_hash = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    ticket_amount = db.Column(db.Integer, nullable=False)
    date_booking = db.Column(db.String(), nullable=False)
    slot_booking = db.Column(db.String(), nullable=False)
    no_devotee = db.Column(db.Integer, nullable=False)

class mandir_3(db.Model):
    
    # Students information table class...
    __tablename__ = 'mandir_3'


    current_hash = db.Column(db.String(), primary_key=True)
    previous_hash = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    ticket_amount = db.Column(db.Integer, nullable=False)
    date_booking = db.Column(db.Date(), nullable=False)
    slot_booking = db.Column(db.String(), nullable=False)
    no_devotee = db.Column(db.Integer, nullable=False)

mydb={"9999999999":mandir_1,"5555555555":mandir_2,"7777777777":mandir_3}
'''
added admin contact in a dictionary due to lack of time, but will be finally stored in a database for all and any temples added
'''
class TempleView(ModelView):
    can_edit=False
    can_delete=False
    create_modal = True
    can_view_details = True
    column_exclude_list = ['previous_hash'] 
    column_filters = ['user_id']
    can_export = True
    def is_accessible(self):
        '''
        We added all temples to all admins due to lack of time, but we can use this function to restrict an admin to access only his temple tickets
        '''
        return current_user.is_authenticated and current_user.is_admin and 1*(current_user.contact)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'), next=request.url)
class UserView(ModelView):
    can_edit=False
    can_delete=False
    can_view_details = True
    column_exclude_list = ['password_hash','private_key','public_key'] 
    column_filters = ['contact','id']
    can_export = True
    def is_accessible(self):
        '''
        We added all temples to all admins due to lack of time, but we can use this function to restrict an admin to access only his temple tickets
        '''
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'), next=request.url)

# adding all database views
admin.add_view(UserView(Users,db.session,endpoint='user'))
admin.add_view(TempleView(mydb["9999999999"],db.session,endpoint='mandir1'))
admin.add_view(TempleView(mydb["5555555555"],db.session,endpoint='mandir2'))
admin.add_view(TempleView(mydb["7777777777"],db.session,endpoint='mandir3'))

config = pdfkit.configuration(wkhtmltopdf = r"/usr/local/bin/wkhtmltopdf")

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
    n=len(pk)
    privateKey=publicKey=None
    while n==len(pk):
        privateKey=SigningKey.generate(curve = ecdsa.NIST384p)
        publicKey=privateKey.verifying_key
        pk.add(to_string(publicKey,True))

    publicKey = publicKey.to_pem()
    public_string = publicKey.decode()

    # Convert the string back to PEM representation
    private_key = privateKey.to_pem()

    # Convert the PEM representation to a private key object
    private_string = private_key.decode()

    print(type(private_string))

    return (private_string),(public_string)

@login_manager.user_loader
def load_user(details):
    print(details)
    user_contact = details["contact"]
    user_id = details["id"]
    user_name = details["name"]
    is_admin = details["admin"]
    return ls.User(user_contact,  user_name, user_id, is_admin)


@app.errorhandler(404) 
def not_found(e): 
    return render_template("404.html")


@app.route("/", methods = ['GET'])
def index():
    return render_template("index.html")

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
            return redirect("/login/")

        user_account = ls.check_in_t_db(user_contact, "log-details", Users, db, session)
        
        if(user_account == None):
            redirect(url_for("login"))
        try:
            ph.verify(user_account.password_hash, user_password)
        except Exception as e:
            fe.wrng_pass()
            session['log-details'] = {"contact":user_contact}
            return redirect(url_for("login"))
        
        user_contact = user_account.contact
        user_id = user_account.id
        if(str(user_contact) in list(mydb.keys())):
            user_to_log = ls.User(user_contact,user_account.name, user_id, True)
        else:
            user_to_log = ls.User(user_contact,user_account.name, user_id)

        login_user(user_to_log)
            
        fe.login_success()
        return redirect(url_for("index"))

    if "log-details" in session:
        return_contact = session["log-details"]["contact"]
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
            return redirect("/signup/")
        
        if not (bool(re.match(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" , password))):
            fe.some_went_wrong()
            return redirect("/signup/")
        
        account_presence = si.check_in_t_db(name , contact ,  request.path , "acc_requested", Users , db  , session)

        if  account_presence != None:
            return account_presence  
        pk=ls.get_public_key(Users,db)
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
def online_darshan():
    return render_template("online_darshan.html")

@app.route("/rammandir/",methods=['POST'])
@login_required
def rammandir():
    if request.method=="POST":
        slot = request.form.get('inlineRadioOptions')
        price = int(request.form.get('inputGroupSelect01'))
        people = int(request.form.get('devotee'))
        date = request.form.get('datepicker1')

        print("printing")
        print(slot, price, people, date)

        if None in (slot,price,people,date) or "" in (slot,price,people,date) :
            fe.some_went_wrong()
            return redirect("/")
        
        if price not in [100, 300, 500] or slot not in ["option1", "option2"]:
            fe.user_beta_msti_nhi()
            return redirect("/")
        print("printing")
        print(slot, price, people, date)
        if(slot == 'option1'):
            slot = "Slot 1 (7:00 AM to 11:00 AM)"
        else :
            slot = "Slot 2 (2:00 PM to 7:00 PM)"
        session['ticket'] = {'slot':slot, 'price':price, 'date' : date, 'people':people, 'temple' :  "9999999999"}

        return redirect("/transaction/")
    
@app.route("/akshardham/",methods=['POST'])
@login_required
def akshardham():
    if request.method=="POST":
        slot = request.form.get('inlineRadioOptions')
        price = int(request.form.get('inputGroupSelect01'))
        people = int(request.form.get('devotee'))
        date = request.form.get('datepicker2')


        if None in (slot,price,people,date) or "" in (slot,price,people,date) :
            fe.some_went_wrong()
            return redirect("/")
        
        if price not in [50, 100] or slot not in ["option1", "option2"]:
            fe.user_beta_msti_nhi()
            return redirect("/")
        
        if(slot == 'option1'):
            slot = "SSlot 1 (10:00 AM to 1:00 PM)"
        else :
            slot = "Slot 2 (2:30 PM to 6:30 PM)"

        session['ticket'] = {'slot':slot, 'price':price, 'date' : date, 'people':people, 'temple' :  "5555555555"}

        return redirect("/transaction/")
    
@app.route("/murdeshwar/",methods=['POST'])
@login_required
def murdeshwar():
    if request.method=="POST":
        slot = request.form.get('inlineRadioOptions')
        price = int(request.form.get('inputGroupSelect01'))
        people = int(request.form.get('devotee'))
        date = request.form.get('datepicker3')

        print(slot, price, people, date)
        if None in (slot,price,people,date) or "" in (slot,price,people,date) :

            fe.some_went_wrong()
            return redirect("/")
        
        if price not in [25, 50] or slot not in ["option1", "option2"]:
            fe.user_beta_msti_nhi()
            return redirect("/")
        
        if(slot == 'option1'):
            slot = "Slot 1 (6:00 AM to 12:00 AM)"
        else :
            slot = "Slot 2 (3:00 PM to 8:00 PM)"

        session['ticket'] = {'slot':slot, 'price':price, 'date' : date, 'people':people, 'temple' :  "7777777777"}

        return redirect("/transaction/")

'''
DUMMY TRANSACTION PAGE
'''
@app.route("/transaction/",methods=['GET','POST'])
@login_required
def transaction():
    if(current_user.is_admin):
        fe.dnt_ac()
        redirect("/")

    # if 'to_redirect'  in session:
    #     return redirect('/')

    if request.method=="POST":
        if 'ticket' not in session:
            fe.some_went_wrong()
            return redirect('/')
        
        publicKey,privateKey=ls.get_key_pair(Users,current_user.user_id)

        if publicKey == None or privateKey == None:
            return redirect('/')
        pem_public_key = publicKey.encode()
        # Convert the PEM representation to a public key object
        publicKey = ecdsa.VerifyingKey.from_pem(pem_public_key)
        pem_private_key = privateKey.encode()
        # Convert the PEM representation to a private key object
        privateKey = ecdsa.SigningKey.from_pem(pem_private_key)

        tx=Transaction((publicKey),"SYSTEM",int(session['ticket']["price"])*int(session['ticket']['people']))   
        tx.sign((privateKey,publicKey))
        difficulty=4
        block=Block(transactions=[tx],previousHash=(mydb[session['ticket']['temple']].query.all()[-1]).current_hash)
        block.mineBlock(difficulty,publicKey)
        ans =  ls.add_transaction(db, mydb[session['ticket']['temple']], session['ticket'], current_user.user_id, block.hash ,block.previousHash,session) #add block to db
        session["dwn_inf"] = {"id":current_user.user_id, "current_hash":block.hash, "previous_hash":block.previousHash, "inf" : session['ticket'], "name":current_user.user_name, "contact":current_user.contact}
        session.pop('ticket')
        values = session['dwn_inf']
        html = render_template("download.html", value = values)
        pdf = pdfkit.from_string(html, False,  configuration = config)
        return send_file(BytesIO(pdf), download_name="Ticket.pdf" , as_attachment=True)

    if 'ticket' not in session:
        fe.some_went_wrong()
        return redirect('/')
    return render_template("transaction.html")
                    

if __name__ == "__main__":
    app.run(debug=True)
