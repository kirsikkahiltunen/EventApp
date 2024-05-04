from db import db
from sqlalchemy.sql import text
from datetime import datetime

def get_all():
    sql = text("SELECT id, event_name, event_date_time, event_user, event_description From events ORDER BY event_date_time")
    result = db.session.execute(sql)
    return result.fetchall()

def get_participation(user_id, event_id):
    sql = text("SELECT user_id, event_id From participants WHERE user_id=:user_id AND event_id=:event_id")
    result = db.session.execute(sql, {"user_id":user_id,"event_id":event_id})
    result=result.fetchone()
    if not result:
        return False
    else:
        return True

def get_event_by_id(event_id):
    sql = text("SELECT id, event_name, event_date_time, event_user, event_description From events WHERE id=:event_id")
    result = db.session.execute(sql, {"event_id":event_id})
    return result.fetchone()

def create_event(user_id, username, event_name, event_date_time, event_category, event_description):
    date_time = datetime.strptime(event_date_time, '%Y-%m-%dT%H:%M')
    f_date_time = date_time.strftime('%Y-%m-%d %H:%M:00')
    sql = text("""INSERT INTO events (event_name, event_date_time, event_category, organizer, event_user, event_description) 
                    VALUES (:event_name, :event_date_time, :event_category, :organizer, :event_user, :event_description)""")
    db.session.execute(sql, {"event_name":event_name, "event_date_time":f_date_time, "event_category":event_category, "organizer":user_id, "event_user":username, "event_description":event_description})
    db.session.commit()

def participate_event(user_id, username,  event_id):
    sql = text("""INSERT INTO participants (user_id, event_id, username)
                    VALUES (:user_id, :event_id, :username)""")
    db.session.execute(sql, {"user_id":user_id, "event_id":event_id, "username":username})
    db.session.commit()

def send_message(user_id, event_id, content):
    sql = text("""INSERT INTO messages (user_id, event_id, content) VALUES (:user_id, :event_id, :content)""")
    db.session.execute(sql, {"user_id":user_id, "event_id":event_id,"content":content})
    db.session.commit()

def find(query):
    sql = text("""SELECT id, event_name, event_date_time, event_category, event_user, event_description FROM events WHERE event_name LIKE :query OR event_description LIKE :query""")
    result = db.session.execute(sql, {"query":"%"+ query +"%"})
    results = result.fetchall()
    return results