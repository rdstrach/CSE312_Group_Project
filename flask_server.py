import flask
from flask import Flask, render_template, request, redirect, url_for
import pymongo
from pymongo import MongoClient
import sys

app = Flask(__name__)


# Method to set up and return MongoDB database
def db():
    client = MongoClient('mongo', 27017)
    db = client['server']
    return db


@app.route('/')
def index():
    return render_template('index.html')

# Save Text Messages in Database
@app.route('/text_messages', methods=['POST'])
def my_form_post():
    text = request.form['tm']
    print(text)
    print(request.form)
    sys.stdout.flush()
    return redirect('/')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


if __name__ == "__main__":
    Flask.run(app, "0.0.0.0", 5000, True)
