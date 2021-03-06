import sys
import os
import flask
from flask import Flask, render_template, request, redirect
import flask_login
from flask_sock import Sock
import loginregister as usermanagement
import tm

app = Flask(__name__)
sock = Sock(app)

ws_connections = []

# app.secret_key = "0000"  # os.environ['SECRET_KEY'] but not working with this value
app.secret_key = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = './static/images/'
login_manager = flask_login.LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
@flask_login.login_required
def index():
    tm_list = tm.returns_tm()
    tm_list.reverse()
    return render_template('index.html', text_messages=tm_list, users=usermanagement.logged_in_user_list())


# Save Text Messages in Database
@app.route('/text_messages', methods=['POST'])
def text_messages():
    tm.loads_tm(flask_login.current_user.username, request.form['tm'])
    return redirect('/')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def loginPOST():
    username: str = request.form.get("name")
    username = username.lower()
    password: str = request.form.get("password")
    if usermanagement.login_validation(username, password) != -1:
        user = load_user(username)

        # add into list of logged in users
        usermanagement.logged_in_users.insert_one({"username": username})

        flask_login.login_user(user, remember=True)
        return flask.redirect(flask.url_for('index'))
    else:
        flask.flash("Incorrect username/password")
        return render_template('login.html')


@app.route('/register', methods=['POST'])
def registerPOST():
    ret = usermanagement.create_user(request.form.get("firstname"), request.form.get("lastname"),
                                     request.form.get("name"), request.form.get("password"),
                                     request.form.get("passwordagain"), request.files['profile'])
    if len(ret) == 0:
        user = load_user(request.form.get("name"))
        flask_login.login_user(user, remember=True)
        return flask.redirect(flask.url_for('index'))
    else:
        for r in ret:
            flask.flash(r)
        return flask.redirect(flask.url_for('register'))


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/logout')
@flask_login.login_required
def logout():
    # remove from list of logged in users
    myquery = {"username": flask_login.current_user.username}
    usermanagement.logged_in_users.delete_many(myquery)
    flask_login.logout_user()

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


@app.route('/settings', methods=['POST'])
def settingsPOST():
    # x= flask_login.current_user.username
    # print(x)
    # sys.stdout.flush()
    # sys.stderr.flush()
    usermanagement.change_password(flask_login.current_user.username, request.form.get("old"), request.form.get("new"),
                                   request.form.get("new2"))
    return flask.redirect(flask.url_for('settings'))


'''
websocket input: {"username":"username sending to","message":"msg being sent"}
websocket sends to specified users thread the json..so recipient receives the following websocket output.. 
websocket output: {"username":"username of sender","message"}


'''
message_receive = dict()


@sock.route('/DM_websocket')
def wsocket(ws):
    listofusers = usermanagement.logged_in_user_list()

    import re, json
    global message_receive
    username = flask_login.current_user.username  # need to know what username is creating websocket
    message_receive.update({username: []})

    while True:
        data = ws.receive()
        print(data)
        if username not in listofusers:
            return
        if len(data) != 0:
            print(data)
            data_parse = json.loads(data)
            if username != data_parse['username'] and data_parse['username'] in listofusers:
                usernameTo = "\"" + data_parse['username'] + "\""
                usernameFrom = "\"" + username + "\""
                print(usernameFrom, usernameTo)
                r_payload = re.sub(usernameTo, usernameFrom, data)
                r_payload = re.sub("&", "&amp", r_payload)
                r_payload = re.sub("<", "&lt", r_payload)
                r_payload = re.sub(">", "&gt", r_payload)
                message_receive[data_parse['username']].append(r_payload)
        else:
            if (len(message_receive[username]) != 0):
                ws.send(message_receive[username].pop(0))


@app.route('/settings')
@flask_login.login_required
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
                ws.send(
                    '{"messageType": "upvote", "status": "OK", "id": "' + new_votes[0] + '", "votes": "' + new_votes[
                        1] + '"}')
            except:  # If ConnectionError due to inactive ws, pass
                pass
        tm.prints_tm()
        print(ws_connections)
        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == "__main__":
    Flask.run(app, "0.0.0.0", 5000, True)
