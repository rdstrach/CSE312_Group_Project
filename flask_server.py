import flask
from flask import Flask, render_template, request, redirect
import pymongo
from pymongo import MongoClient
import sys
import tm

app = Flask(__name__)


# Method to set up and return MongoDB database
def db():
    client = MongoClient('mongo', 27017)
    db = client['server']
    return db


@app.route('/')
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


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


if __name__ == "__main__":
    Flask.run(app, "0.0.0.0", 5000, True)
