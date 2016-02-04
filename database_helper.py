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

#Insert a user in the database
def insert_user(email,password,firstname,familyname,gender,city,country):
    conn = connect_db()
    cursor = conn.cursor()
    user = (email,password,firstname,familyname,gender,city,country)
    try:
        add_user = "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(add_user,user)
        conn.commit()
    except:
        return False
    return True

#Close a database
def close_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Creates the database based on database.schema
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('database.schema', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
