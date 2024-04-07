# Tapahtuma sovellus

Sovelluksessa käyttäjät voivat luoda tapahtumia ja osallistua tapahtumiin sekä hakea tapahtumia ja lähettää viestejä tapahtuman järjestävälle. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

## sovelluksen ominaisuuksia:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee listan tapahtumista ja voi osallistua tapahtumiin.
- Käyttäjä voi hakea tapahtumia hakusanoilla. 
- Käyttäjä voi suodattaa tapahtumia kategorian tai ajankohdan mukaan.
- Käyttäjä voi luoda uusia tapahtumia sekä muokata tai poistaa oman tapahtumansa.
- Tapahtumaa luodessa käyttäjä lisää tapahtumalle nimen, kuvauksen, päivämäärän ja kellonajan, osoitteen tai muun paikkatiedon sekä tapahtuman kategorian. 
- Tapahtuman voi määrittää julkiseksi tai yksityiseksi.
- Yksityisiin tapahtumiin voivat ilmoittautua vain tapahtuman järjestäjän valitsemat käyttäjät.
- Käyttäjä näkee listan luomistaan tapahtumista ja näkee kuinka monta osallistujaa tapahtumassa on sekä osallistujien nimet.
- Käyttäjä voi lähettää viestin tapahtuman järjestäjälle ja järjestäjä voi vastata viesteihin.
- Ylläpitäjä näkee kaikki tapahtumat ja tapahtumiin ilmoittautuneet. Ylläpitäjä voi poistaa tapahtumia tai perua käyttäjän ilmoittautumisen tapahtumaan.


## Tällä hetkellä toimivat ominaisuudet:

- käyttäjä voi kirjautua sisään ja ulos sekä uoda uudet tunnukset



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

Tällä hetkellä sovelluksessa toimii vain sisään- ja uloskirjautuminen sekä uuden käyttäjän rekisteröiminen. 


