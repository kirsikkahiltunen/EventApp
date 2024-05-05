from db import db
from sqlalchemy.sql import text
from datetime import datetime

def get_all():
    sql = text(
        """SELECT id, event_name, event_date_time, event_user, event_description From events ORDER BY event_date_time""")
    result = db.session.execute(sql)
    return result.fetchall()

def get_participation(user_id, event_id):
    sql = text(
        """SELECT user_id, event_id From participants WHERE user_id=:user_id AND event_id=:event_id""")
    result = db.session.execute(
        sql, {"user_id": user_id, "event_id": event_id})
    result = result.fetchone()
    if result:
        return True
    else:
        return False

def get_all_participants(event_id):
    sql = text("""SELECT username From participants WHERE event_id=:event_id""")
    result = db.session.execute(sql, {"event_id": event_id})
    return result.fetchall()

def get_messages_by_event(event_id):
    sql = text("""SELECT * From messages WHERE event_id=:event_id""")
    result = db.session.execute(sql, {"event_id": event_id})
    return result.fetchall()

def get_messages_by_user_id(user_id):
    sql = text("""SELECT * From messages WHERE user_id=:user_id""")
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def get_event_by_id(event_id):
    sql = text(
        """SELECT id, event_name, event_date_time, event_user, event_description From events WHERE id=:event_id""")
    result = db.session.execute(sql, {"event_id": event_id})
    return result.fetchone()

def create_event(user_id, username, event_name, event_date_time, event_category, event_description):
    date_time = datetime.strptime(event_date_time, '%Y-%m-%dT%H:%M')
    f_date_time = date_time.strftime('%Y-%m-%d %H:%M:00')
    sql = text("""INSERT INTO events (event_name, event_date_time, event_category, organizer, event_user, event_description) 
                    VALUES (:event_name, :event_date_time, :event_category, :organizer, :event_user, :event_description)""")
    db.session.execute(sql, {"event_name": event_name, "event_date_time": f_date_time, "event_category": event_category,
                       "organizer": user_id, "event_user": username, "event_description": event_description})
    db.session.commit()

def participate_event(user_id, username,  event_id):
    sql = text("""INSERT INTO participants (user_id, event_id, username)
                    VALUES (:user_id, :event_id, :username)""")
    db.session.execute(
        sql, {"user_id": user_id, "event_id": event_id, "username": username})
    db.session.commit()

def send_message(user_id, username, event_id, title, content):
    sql = text("""INSERT INTO messages (user_id, username, event_id, title, content) VALUES (:user_id, :username, :event_id, :title, :content)""")
    db.session.execute(sql, {"user_id": user_id, "username": username,
                       "event_id": event_id, "title": title, "content": content})
    db.session.commit()

def find(query):
    sql = text("""SELECT id, event_name, event_date_time, event_category, event_user, event_description FROM events WHERE event_name LIKE :query OR event_description LIKE :query""")
    result = db.session.execute(sql, {"query": "%" + query + "%"})
    results = result.fetchall()
    return results

def find_past_events():
    now = datetime.now()
    formated_now = now.strftime('%Y-%m-%d %H:%M:00')
    sql = text("""SELECT id, event_name, event_date_time, event_category, organizer, event_user, event_description FROM events WHERE event_date_time < :now""")
    result = db.session.execute(sql, {"now": formated_now})
    results = result.fetchall()
    return results

def past_events():
    events = find_past_events()
    for event in events:
        sql = text("""INSERT INTO past_events (event_name, event_date_time, event_category, organizer, event_user, event_description) 
                    VALUES (:event_name, :event_date_time, :event_category, :organizer, :event_user, :event_description)""")
        db.session.execute(sql, {"event_name": event.event_name, "event_date_time": event.event_date_time, "event_category": event.event_category,
                           "organizer": event.organizer, "event_user": event.event_user, "event_description": event.event_description})
    remove_past_events()
    db.session.commit()

def remove_past_events():
    now = datetime.now()
    formatted_now = now.strftime('%Y-%m-%d %H:%M:00')
    sql_participants = text("""DELETE FROM participants WHERE event_id IN (
                                    SELECT id FROM events WHERE event_date_time < :now
                                        )""")
    db.session.execute(sql_participants, {"now": formatted_now})
    sql_events = text(
        """DELETE FROM events WHERE event_date_time < :now""")
    db.session.execute(sql_events, {"now": formatted_now})

    db.session.commit()

def update_event_info(event_id, user_id, event_name, event_date_time, event_description):
    date_time = datetime.strptime(event_date_time, '%Y-%m-%dT%H:%M')
    f_date_time = date_time.strftime('%Y-%m-%d %H:%M:00')
    sql = text("""UPDATE events SET event_name=:event_name, event_date_time=:event_date_time, event_description=:event_description WHERE id=:id AND organizer=:organizer""")
    db.session.execute(sql, {"id": event_id, "event_name": event_name, "event_date_time": f_date_time,
                       "organizer": user_id, "event_description": event_description})
    db.session.commit()

def delete_event(event_id, user_id):
    sql_participants = text("""DELETE FROM participants WHERE event_id IN (
                                SELECT id FROM events WHERE id=:id
                                        )""")
    db.session.execute(sql_participants, {"id": event_id})
    sql_participants = text("""DELETE FROM messages WHERE event_id IN (
                                SELECT id FROM events WHERE id=:id
                                        )""")
    db.session.execute(sql_participants, {"id": event_id})
    sql_events = text(
        """DELETE FROM events WHERE id=:id AND organizer=:organizer""")
    db.session.execute(sql_events, {"id": event_id, "organizer": user_id})
    db.session.commit()

def delete_participation(event_id, user_id):
    sql = text(
        """DELETE FROM participants WHERE event_id=:event_id AND user_id=:user_id""")
    db.session.execute(sql, {"event_id": event_id, "user_id": user_id})
    db.session.commit()