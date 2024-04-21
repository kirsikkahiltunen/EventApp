from db import db
from sqlalchemy.sql import text
from datetime import datetime

def get_all():
    sql = text("SELECT id, event_name, event_date_time, event_user, event_description From events ORDER BY event_date_time")
    result  = db.session.execute(sql)
    return result.fetchall()

def create_event(user_id, username, event_name, event_date_time, event_category, event_description):
    date_time = datetime.strptime(event_date_time, '%Y-%m-%dT%H:%M')
    f_date_time = date_time.strftime('%Y-%m-%d %H:%M:00')
    sql = text("""INSERT INTO events (event_name, event_date_time, event_category, organizer, event_user, event_description) 
                    VALUES (:event_name, :event_date_time, :event_category, :organizer, :event_user, :event_description)""")
    db.session.execute(sql, {"event_name":event_name, "event_date_time":f_date_time, "event_category":event_category, "organizer":user_id, "event_user":username, "event_description":event_description})
    db.session.commit()

