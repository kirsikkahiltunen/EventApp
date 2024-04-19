from db import db
import os
from flask import request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import re

def login(username, password):
    sql = text("SELECT* FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})

    user = result.fetchone()

    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user.id
            return True
        else:
            return False

def logout():
    del session["username"]
    del session["user_id"]

def register(username, password1):
    password_hash = generate_password_hash(password1)
    sql = text("""INSERT INTO users (username, password) 
                    VALUES (:username, :password)""")
    db.session.execute(sql, {"username":username, "password":password_hash})
    db.session.commit()
        
    return login(username, password1)

def valid_password(password):
    special_characters= """!@#$%&*/()[]-_=+}?';,:.<>\``~^{"""
    lower=0
    upper=0
    digit=0
    special=0
    for i in password:

        if (i.islower()):
            lower+=1
        
        if (i.isupper()):
            upper+=1

        if (i.isdigit()):
            digit+=1

        if (i in special_characters):
            special+=1
    
    print (f"lower={lower}, upper={upper}, digit={digit}, special={special}")

    if (lower>=1 and upper>=1 and digit>=1 and special>=1):
        return True
    
    return False
   



def user_id():
    return session.get("user_id", 0)




        
    
        
