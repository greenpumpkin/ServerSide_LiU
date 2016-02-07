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
def sign_in():
    email = request.form['email']
    password = request.form['password']
    signIn = database_helper.sign_in_db(email,password)
    if signIn == True:
        token = create_token()
        return json.dumps([{'success': True, 'message': "Login successful!", 'token': token}])
    else:
       return json.dumps([{'success': False, 'message': '''Wrong email or password'''}])

@app.route('/signup', methods=['POST'])
def sign_up():
    email = request.form['email']
    password = request.form['password']
    firstname = request.form['firstname']
    familyname = request.form['familyname']
    gender = request.form['gender']
    city = request.form['city']
    country = request.form['country']
    signUp = database_helper.insert_user(email,password,firstname,familyname,gender, city, country)
    if signUp == True:
        return json.dumps([{"success": True, "message": "Successfully created a new user."}])
    else:
        return json.dumps([{"success": False, "message": "Form data missing or incorrect type."}])

#Creates a random token
def create_token():
    ab = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    token = ''
    for i in range(0, 36):
        token += ab[random.randint(0,len(ab)-1)]
    return token
    
if __name__ == '__main__':
    app.run()
    #database_helper.init_db(app)