from flask import Flask, app, request
import database_helper
import json

app = Flask(__name__)
app.debug = True

#@app.route('/')
#def hello_world():
#    return "Hello World !"

@app.before_request
def before_request():
    database_helper.connect_db()

@app.teardown_request
def teardown_request(exception):
    database_helper.close_db()

#Authenticates the username by the provided password
@app.route('/signin', methods=['POST'])
def sign_in(email,password):
    email = request.form['email']
    password = request.form['password']