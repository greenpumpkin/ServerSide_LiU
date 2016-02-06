from flask import app, request
from flask import Flask
import database_helper
import random
import json

app = Flask(__name__)
app.debug = True

@app.before_request
def before_request():
    database_helper.connect_db()

@app.teardown_request
def teardown_request(exception):
    database_helper.close_db()

@app.route('/')
def hello_world():
    return "Hello World !"

#Authenticates the username by the provided password
@app.route('/signin', methods=['POST'])
def sign_in(email,password):
    email = request.form['email']
    password = request.form['password']

#Creates a random token
def create_token():
    ab = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    token = ''
    for i in range(0, 36):
        token += ab[random.randint(0,len(ab)-1)]
    return token
    
if __name__ == '__main__':
    app.run()
    database_helper.init_db(app)
    database_helper.insert_user('email','password','firstname','familyname','gender','city','country')