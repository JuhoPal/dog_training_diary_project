# Koiran treenipäiväkirja - kehitysohje

Tämä dokumentti määrittää projektin rakenteen, vastuut ja kehityssäännöt.

## 1. Kielisääntö

- Koodi, nimet ja rakenne: englanti
- Käyttäjälle näkyvät viestit: suomi

Esimerkki:

```python
return {"message": "Koira poistettu"}
```

## 2. Vastuunjako kansioittain

- models: tietokantamallit ja relaatiot
- schemas: pyyntö- ja vastausmallit (Pydantic)
- services: liiketoimintalogiikka ja tietokantaoperaatiot
- routers: HTTP-endpointit ja reititys
- tests: automaattiset testit

## 3. Nykyinen rakenne

```text
.
|- main.py
|- database.py
|- README.md
|- instructors.md
|- models/
|  |- dog.py
|  |- training_session.py
|  |- exercise.py
|  '- competition.py
|- schemas/
|  '- api_schema.py
|- services/
|  '- core_service.py
|- routers/
|  '- api_router.py
'- tests/
   '- test_api.py
```

## 4. Tiedostokohtaiset vastuut

### main.py

- luo FastAPI-sovelluksen
- rekisteröi reitit
- sisältää juurireitin

### database.py

- määrittää SQLite-yhteyden
- luo SQLAlchemy engine/session/base
- tarjoaa get_db-riippuvuuden

### routers/api_router.py

- määrittää endpointit:
  - /dogs
  - /trainings
  - /ui
  - /ui/api/trainings
- delegoi liiketoimintalogiikan services-kerrokseen

### services/core_service.py

- sisältää koirien ja treenien CRUD-logiikan
- sisältää UI-listauksen koostelogiikan
- käsittelee palvelutason virheet

### schemas/api_schema.py

- sisältää kaikki pyyntö- ja vastausmallit
- keskittää validointisäännöt

### tests/test_api.py

- testaa perusreitin
- testaa koira- ja treenitoiminnallisuudet
- testaa UI API- ja HTML-näkymät

## 5. Kehityssäännöt

1. Tee muutokset kerroksittain: schema -> service -> router -> tests.
2. Päivitä testit aina ominaisuusmuutosten yhteydessä.
3. Pidä käyttäjälle näkyvä teksti suomeksi.
4. Pidä importit ajan tasalla, kun tiedostoja yhdistetään tai siirretään.
5. Päivitä README ja instructors samassa muutoksessa, jos rakenne muuttuu.

## 6. Tarkistuslista ennen mergeä

1. Testit menevät läpi komennolla python -m pytest -q.
2. README vastaa todellista rakennetta ja endpointteja.
3. Virheviestit ovat suomeksi.
4. Dokumentaatio ei viittaa poistettuihin tiedostoihin.
