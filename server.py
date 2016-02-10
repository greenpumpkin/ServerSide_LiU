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


@app.route('/signup', methods=['POST'])
def sign_up():
    #if request.method == 'POST':
    email = request.form['emailSign']
    password = request.form['passwordSign']
    firstname = request.form['firstName']
    familyname = request.form['familyName']
    gender = request.form['gender']
    city = request.form['city']
    country = request.form['country']
    signUp = database_helper.insert_user(email,password,firstname,familyname,gender,city,country)
    if signUp:
        return json.dumps({"success": True, "message": "Successfully created a new user."})
    else:
        return json.dumps({"success": False, "message": "Form data missing or incorrect type."})

#Authenticates the username by the provided password
@app.route('/signin', methods=['POST'])
def sign_in():
    email = request.form['emailLog']
    password = request.form['passwordLog']
    signIn = database_helper.sign_in_db(email,password)

    if signIn:
        token = create_token()
        database_helper.add_logged_in(token,email)
        return json.dumps({'success': True, 'message': "Login successful!", 'token': token})
    else:
       return json.dumps({'success': False, 'message': '''Wrong email or password'''})

#Creates a random token
def create_token():
    ab = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    token = ''
    for i in range(0, 36):
        token += ab[random.randint(0,len(ab)-1)]
    return token

#Signs out a user from the system
@app.route('/signout', methods=['POST'])
def sign_out():
    token = request.form['token']
    if (database_helper.get_logged_in(token)):
        database_helper.remove_logged_in(token)
        return json.dumps({"success": True, "message": "Successfully signed out."})
    else:
        return json.dumps({"success": False, "message": "You are not signed in"})

#Changes the password from the current user to a new one
@app.route('/changepassword', methods=['POST'])
def change_password():
    token = request.form['token']
    pwd = request.form['pwd']
    chgPwd = request.form['chgPwd']
    if not database_helper.get_logged_in(token):
        return json.dumps({'success': False, 'message': "You are not logged in."})
    else:
        if len(chgPwd) < 6:
            return json.dumps({"success": False, "message": "Error: password must be at least 6 characters long"})
        email = database_helper.get_email(token)
        validLog = database_helper.check_pwd(email,pwd)
        if validLog == False:
            return json.dumps({'success': False, 'message': "Wrong password."})
        database_helper.modify_pwd(email[0],pwd,chgPwd)
        return json.dumps({'success': True, 'message': "Password changed."})

#Retrieves the stored data for the user whom the passed token is issued for.
#The currently signed-in user case use this method to retrieve all its own info from the server
@app.route('/getuserdatabytoken/<token>', methods=['GET'])
def get_user_data_by_token(token):
    if (database_helper.get_logged_in(token)):
        data = database_helper.get_user_data_by_token(token)
        if data is not None:
            return json.dumps({"success": True, "message": "User data retrieved.", "data": data})
        return json.dumps({"success": False, "message": "No such user."})
    return json.dumps({"success": False, "message": "You are not signed in."})

#Retrieves the stored data for the user specified by the email address
@app.route('/getuserdatabyemail/<token>/<email>', methods=['GET'])
def get_user_data_by_email(token,email):
    if (database_helper.get_logged_in(token)):
        data = database_helper.get_user_data_by_email(email)
        if data is not None:
            return json.dumps({"success": True, "message": "User data retrieved.", "data": data})
        else:
            return json.dumps({"success": False, "message": "No such user."})
    else:
        return json.dumps({"success": False, "message": "You are not signed in."})

if __name__ == '__main__':
    app.run(debug=True)
    #database_helper.init_db(app)