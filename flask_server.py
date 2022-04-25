import flask
from flask import Flask, render_template, request
import flask_login
import pymongo
from pymongo import MongoClient
# import db as database
import loginregister as usermanagement

app = Flask(__name__)

app.secret_key = "0000" #os.environ['SECRET_KEY'] but not working with this value
login_manager = flask_login.LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Method to set up and return MongoDB database
def db():
    client = MongoClient('mongo', 27017)
    db = client['server']
    return db

@app.route('/')
@flask_login.login_required
def index():
    usermanagement.printAll()
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def loginPOST():
    username: str = request.form.get("name")
    password: str = request.form.get("password")
    if usermanagement.login_validation(username, password) != -1:
        user = load_user(username)
        # add into list of logged in users

        flask_login.login_user(user, remember=True)
        return flask.redirect(flask.url_for('index'))
    else:
        #display flask error message "incorrect username/password"
        return render_template('login.html')

@app.route('/register', methods=['POST'])
def registerPOST():
    username: str = request.form.get("name")
    password: str = request.form.get("password")
    firstname: str = request.form.get("firstname")
    lastname: str = request.form.get("lastname")
    # add profile image processing here

    # passwordAgain: str = request.form.get("passwordagain")
    usermanagement.create_user(firstname,lastname,username,password,password) #last parameter shld be passwordAgain
    user = load_user(username)
    # add into list of logged in users

    flask_login.login_user(user, remember=True)
    return flask.redirect(flask.url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    # remove from list of logged in users

    return flask.redirect(flask.url_for('login'))

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

@app.route('/settings')
def settings():
    return render_template('settings.html')


if __name__ == "__main__":
    Flask.run(app, "0.0.0.0", 5000, True)
