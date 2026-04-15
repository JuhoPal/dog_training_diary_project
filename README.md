# Koiran treenipäiväkirja API

Koiran treenipäiväkirja on FastAPI- ja SQLAlchemy-pohjainen sovellus, jolla hallitaan koiria, treenejä ja treeneihin liittyviä harjoituksia.

## Mitä projekti sisältää

- Koirien CRUD-toiminnot
- Treenien CRUD-toiminnot
- UI API treenien ja harjoitusten listaukseen
- Selainnäkymä treenien selaamiseen

## Kieli- ja nimeämissäännöt

- Koodi, funktioiden nimet, tiedostonimet ja rakenne: englanti
- Käyttäjälle näkyvät viestit: suomi

## Teknologiat

- Python 3.12
- FastAPI
- SQLAlchemy 2.x
- SQLite
- Pytest

## Projektin rakenne

```text
.
|- main.py
|- database.py
|- requirements.txt
|- README.md
|- instructors.md
|- dog_training_diary.db
|- models/
|  |- dog.py
|  |- training_session.py
|  |- exercise.py
|  |- competition.py
|  '- __init__.py
|- schemas/
|  |- api_schema.py
|  '- __init__.py
|- services/
|  |- core_service.py
|  '- __init__.py
|- routers/
|  |- api_router.py
|  '- __init__.py
'- tests/
   '- test_api.py
```

## Asennus

1) Luo virtuaaliympäristö

```powershell
python -m venv venv
```

2) Aktivoi ympäristö (PowerShell)

```powershell
.\venv\Scripts\activate
```

3) Asenna riippuvuudet

```powershell
pip install -r requirements.txt
```

## Sovelluksen käynnistys

```powershell
uvicorn main:app --reload
```

Hyödylliset osoitteet:

- API juuri: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Testien ajo

```powershell
python -m pytest -q
```

## Tietokanta

- Tietokanta: SQLite
- Tietokantatiedosto luodaan projektin juureen nimellä dog_training_diary.db
- Taulut luodaan käynnistyksessä komennolla Base.metadata.create_all(bind=engine)

## API-pääreitit

### Perusreitti

- GET /

Palauttaa:

```json
{"message": "Koiran treenipäiväkirjan API"}
```

### Koirat

- GET /dogs
- GET /dogs/{dog_id}
- POST /dogs
- PUT /dogs/{dog_id}
- DELETE /dogs/{dog_id}

Esimerkkirunko (POST /dogs):

```json
{
  "name": "Rekku",
  "breed": "Labradorinnoutaja",
  "birth_date": "2021-05-12",
  "notes": "Rauhallinen ja motivoitunut"
}
```

### Treenit

- GET /trainings
- GET /trainings/{training_id}
- POST /trainings
- PUT /trainings/{training_id}
- DELETE /trainings/{training_id}

Esimerkkirunko (POST /trainings):

```json
{
  "dog_id": 1,
  "date": "2026-03-10",
  "duration_minutes": 45,
  "location": "Koulutuskenttä",
  "notes": "Kontaktiharjoituksia"
}
```

### UI API ja selainnäkymä

- GET /ui/api/trainings
  - palauttaa treenit, koiran perustiedot, harjoitusten määrän ja harjoituslistan
- GET /ui
  - palauttaa HTML-sivun treenien selaamiseen

## Validointi

Koirat:

- name: pakollinen, 1-100 merkkiä
- breed: pakollinen, 1-100 merkkiä
- birth_date: valinnainen (ISO-päivämäärä)
- notes: valinnainen

Treenit:

- dog_id: pakollinen, kokonaisluku > 0
- date: pakollinen (ISO-päivämäärä)
- duration_minutes: pakollinen, kokonaisluku > 0
- location: valinnainen, max 150 merkkiä
- notes: valinnainen

## Virhetilanteet

Esimerkkiviestejä:

- Koiraa ei löytynyt
- Treeniä ei löytynyt

## Kehitysohjeet

- Pidä reitit ohuina: liiketoimintalogiikka kuuluu services-kansioon.
- Laajenna testit aina, kun lisäät uusia endpointteja tai muutat vanhoja.
- Säilytä rakenne selkeänä: schema, service ja router ovat omissa kansioissaan.

## Seuraavat kehitysaskeleet

1. Harjoitusten CRUD-endpointit
2. Kilpailujen CRUD-endpointit
3. Hakutoiminto koiran nimellä ja päivämäärävälillä
4. Alembic-migraatiot tuotantokelpoiseen skeemanhallintaan
