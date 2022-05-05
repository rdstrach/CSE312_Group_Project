import flask
from flask import Flask, render_template, request, redirect
import flask_login
import pymongo
from pymongo import MongoClient
from flask_sock import Sock
# import db as database
import loginregister as usermanagement
# import for text messages
import sys
import tm

app = Flask(__name__)
sock = Sock(app)

ws_connections = []

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
    tm_list = tm.returns_tm()
    tm_list.reverse()
    return render_template('index.html', text_messages=tm_list)


# Save Text Messages in Database
@app.route('/text_messages', methods=['POST'])
def text_messages():
    username = "testuser1"
    text = request.form['tm']
    tm.loads_tm(username, text)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def registerPOST():
    username: str = request.form.get("name")
    password: str = request.form.get("password")
    # passwordAgain: str = request.form.get("passwordagain")
    usermanagement.create_user("test","test",username,password,password) #last parameter shld be passwordAgain
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

@app.route('/settings')
def settings():
    return render_template('settings.html')

# Websocket for upvote
@sock.route('/upvote')
def upvote(sock):
    ws_connections.append(sock)
    while True:
        data = sock.receive()
        new_votes = tm.upvotes_tm(data)
        # Send to all websocket connections
        for ws in ws_connections:
            try:
                ws.send('{"messageType": "upvote", "status": "OK", "id": "' + new_votes[0] + '", "votes": "' + new_votes[1] + '"}')
            except: # If ConnectionError, remove inactive ws from list
                ws_connections.remove(ws)
        tm.prints_tm()
        print(ws_connections)
        sys.stdout.flush()
        sys.stderr.flush()

if __name__ == "__main__":
    Flask.run(app, "0.0.0.0", 5000, True)
