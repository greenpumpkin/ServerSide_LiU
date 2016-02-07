import sqlite3
from flask import g, app


DATABASE = 'database.db'

#Connection to a database
def connect_db():
    return sqlite3.connect(DATABASE)

#Opens a connect_db() if there is None in the current context
def get_db():
    db = getattr(g, '_database', None)
    #If there is no database in g, database value is None
    if db is None:
        db = g._database = connect_db()
    return db

#Close a database
def close_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Inserts a user in the database when signing up
def insert_user(email,password,firstname,familyname,gender,city,country):
     db = get_db()
     user = (email,password,firstname,familyname,gender,city,country)
     try:
      db.execute('INSERT INTO users (email,password,firstname,familyname,gender,city,country) VALUES (?, ?, ?, ?, ?, ?, ?)', user)
     except:
         return False
     db.commit()
     return True

#Inserts a user in the database when signing in
def sign_in_db(email,password):
    db = get_db()
    user = (email,password)
    request = db.execute('SELECT * FROM users WHERE email=(?) AND password=(?)', user)
    try:
        #Retrieving a single matching row,
        request.fetchone()
    except:
        return False
    db.commit()
    return True

#Creates the database based on database.schema
def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource('database.schema', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()