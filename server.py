from flask import Flask, app, request
import database_helper
import json

app = Flask(__name__)
app.debug = True

#@app.route('/')
#def hello_world():
#    return "Hello World !"

#Authenticates the username by the provided password
@app.route('/signin', methods=['POST'])
def sign_in(email,password):
    email = request.form['email']
    password = request.form['password']