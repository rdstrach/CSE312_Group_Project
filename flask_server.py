import flask
from flask import Flask, render_template, request, redirect
import flask_login
import loginregister as usermanagement
import tm

app = Flask(__name__)

app.secret_key = "0000"  # os.environ['SECRET_KEY'] but not working with this value
login_manager = flask_login.LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


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
    ret = usermanagement.create_user(request.form.get("firstname"), request.form.get("lastname"),
                                     request.form.get("name"), request.form.get("password"),
                                     request.form.get("passwordagain"))
    if ret is None:
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
