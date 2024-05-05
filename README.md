# Tapahtuma sovellus

Sovelluksessa käyttäjät voivat luoda tapahtumia ja osallistua tapahtumiin sekä hakea tapahtumia ja lähettää viestejä tapahtuman järjestävälle.

## sovelluksen ominaisuudet:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee listan tapahtumista ja voi osallistua tapahtumiin.
- Käyttäjä voi hakea tapahtumia hakusanoilla. 
- Käyttäjä voi luoda uusia tapahtumia sekä muokata tai poistaa oman tapahtumansa.
- Tapahtumaa luodessa käyttäjä lisää tapahtumalle nimen, kuvauksen, päivämäärän ja kellonajan sekä tapahtuman kategorian. 
- Käyttäjä näkee listan luomistaan tapahtumista ja näkee kuinka monta osallistujaa tapahtumassa on sekä osallistujien nimet.
- Käyttäjä voi lähettää viestin tapahtuman järjestäjälle ja järjestäjä voi vastata viesteihin.



### Ohjeet sovelluksen käynnistämiseen:

Kloonaa tämä repositorio omalle koneellesi. Siirry sen hakemiston juurikansioon, johon kloonasit tämän repositorion. Luo tähän kansioon oma paikallinen .env-tiedosto jonka sisällön tulee olla seuraava:

SECRET_KEY=oma salainen avain

DATABASE_URI=postgresql:///tietokannan nimi

Seuraavaksi valmistellaan ja aktivoidaan tarvittava virtuaaliympäristö ja asennetaan riippuvuudet ajamalla seuraavat komennot terminaalissa:

$ python3 -m venv venv

$ source venv/bin/activate

(venv) $ pip install -r requirements.txt

(venv) $ psql < schema.sql

sovelluksen saa käyntiin komennolla (venv) $ flask run 


