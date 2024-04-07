CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
);

CREATE TABLE events(
    id SERIAL PRIMARY KEY,
    event_name TEXT,
    event_date DATE,
    event_time TIME,
    organizer INT REFERENCES users(id),
    event_description TEXT
);

CREATE TABLE participants(
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    event_id INT REFERENCES events(id)
);
