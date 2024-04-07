from db import db
from sqlalchemy.sql import text

def get_all():
    sql = "SELECT id, event_name, event_date, event_time, organizer, event_description From events ORDER BY event_date, event_time"

