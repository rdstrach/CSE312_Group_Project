import sys
import os
import flask
from flask import Flask, render_template, request
import flask_login
import pymongo
from pymongo import MongoClient
import db as database
import loginregister
import loginregister as usermanagement

app = Flask(__name__)

app.secret_key = "0000" #os.environ['SECRET_KEY'] but not working with this value
login_manager = flask_login.LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# mongo_client=None
# version=-1
# account_db=None
# users_id_collection=None
# account_info=None
# id_query={}


# Method to set up and return MongoDB database
def db():
    client = MongoClient('mongo', 27017)
    db = client['server']
    return db

@app.route('/')
@flask_login.login_required
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    print("user a exists: " + str(loginregister.user_exist("a")))
    sys.stdout.flush()
    sys.stderr.flush()
    return render_template('login.html')
#comment

@app.route('/register', methods=['POST'])
def registerPOST():
    username: str = request.form.get("name")
    password: str = request.form.get("password")
    usermanagement.create_user("test","test",username,password,password)
    user = load_user(username)
    flask_login.login_user(user, remember=True)
    return flask.redirect(flask.url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html')

class User(flask_login.UserMixin):
    def __init__(self, username, active=True):
        self.username = username
        self.active = active

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


@login_manager.user_loader
def load_user(username):
    return User(username, True)


def startup():
    return
    # mongo_client = MongoClient('mongo', 27017)
    # version = 1
    # account_db = mongo_client["account_db"+str(version)]
    # users_id_collection = account_db["id_counter"]
    # account_info = account_db["account_info"]
    # id_query = {"field": "key"}
    # global mongo_client
    # mongo_client = MongoClient('mongo', 27017)
    # global version
    # version = 1
    # global account_db
    # account_db = mongo_client["account_db"+str(version)]
    # global users_id_collection
    # users_id_collection = account_db["id_counter"]
    # global account_info
    # account_info = account_db["account_info"]
    # global id_query
    # id_query = {"field": "key"}

if __name__ == "__main__":
    Flask.run(app, "0.0.0.0", 5000, True)
    # database.startDb()
    # startup()



