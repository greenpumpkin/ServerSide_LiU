import sqlite3
from flask import g


DATABASE = 'database.db'

#Connection to a database
def connect_db():
    return sqlite3.connect(DATABASE)

#Opens a connect_db() if there is None in the current context
def get_db():
    db = getattr(g,'database',None)
    #If there is no database in g, database value is None
    if db is None:
        db = g.database = connect_db()
    return db

#Insert a user in the database
def insert_user(email,password,firstname,familyname,gender,city,country):
    conn = connect_db()
    user = (email,password,firstname,familyname,gender,city,country)
    try:
        add_user = "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)"
        conn.execute(add_user,user)
        conn.commit()
    except:
        return False
    return True

#Close a database
def close_db():
    get_db().close()
