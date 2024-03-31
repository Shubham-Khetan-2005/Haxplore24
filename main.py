from flask import Flask, render_template, request, redirect , url_for, session, jsonify , Response , send_file
from flask_login import LoginManager , login_required , login_user , logout_user  , current_user
from flask_sqlalchemy import SQLAlchemy
import login_system as ls

app =Flask(__name__)
db = SQLAlchemy(app)

app.secret_key = "super-secret-key"
app.config['SECRET_KEY'] = '12345'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Binding both the databses to the sqlalchemy uri...
SQLALCHEMY_BINDS = {
    'haxplore':        'mysql://root:@localhost/haxplore',
}
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS

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
