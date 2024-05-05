CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE events(
    id SERIAL PRIMARY KEY,
    event_name TEXT,
    event_date_time TIMESTAMP,
    event_category TEXT[],
    organizer INT REFERENCES users(id),
    event_user TEXT,
    event_description TEXT
);

CREATE TABLE past_events(
    id SERIAL PRIMARY KEY,
    event_name TEXT,
    event_date_time TIMESTAMP,
    event_category TEXT[],
    organizer INT REFERENCES users(id),
    event_user TEXT,
    event_description TEXT
);

CREATE TABLE participants(
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    event_id INT REFERENCES events(id),
    username TEXT
);

CREATE TABLE messages(
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    username TEXT,
    event_id INT REFERENCES events(id),
    title TEXT,
    content TEXT
);

INSERT INTO users (username, password) VALUES ('Testi_kayttaja', '   ');
INSERT INTO events (event_name, event_date_time, event_category, organizer, event_user, event_description) VALUES ('Lukupiiri', '2024-09-04 18:15:00', '{9}', 1, 'Testi_kayttaja', 'Biologia aiheinen lukupiiri aloittaa viikoittaiset tapaamiset 4.9.2024. Mukaan mahtuu kaikki lukemisesta ja biologiasta kiinnostuneet. Ensimmäinen kirja, jota lukupiirissä tullaan käsittelemään on Selja Ahavan "Nainen joka rakasti hyönteisiä". Seuraava kirja päätetään osallistujien kesken. Kirjaehdotuksia ovat esim. Charlotte McConaghyn "Täällä oli susia".');
INSERT INTO events (event_name, event_date_time, event_category, organizer, event_user, event_description) VALUES ('Lautapeli-ilta', '2024-05-14 17:30:00', '{2}', 1, 'Testi_kayttaja', 'Tähän lautapeli-iltaan ovat kaikki tervetulleita. Saavu paikalle pelaamaan tuttuja tai vähemmän tuttuja lautapelejä tai ota oma suosikkilautapelisi mukaan.');