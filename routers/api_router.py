from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import get_db
from schemas.api_schema import (
    DogCreate,
    DogResponse,
    DogUpdate,
    TrainingSessionCreate,
    TrainingSessionResponse,
    TrainingSessionUpdate,
)
from services import core_service


router = APIRouter()


@router.get("/dogs", response_model=list[DogResponse], tags=["Koirat"])
def get_dogs(db: Session = Depends(get_db)):
    return core_service.get_all_dogs(db)


@router.get("/dogs/{dog_id}", response_model=DogResponse, tags=["Koirat"])
def get_dog(dog_id: int, db: Session = Depends(get_db)):
    return core_service.get_dog_by_id(db, dog_id)


@router.post(
    "/dogs",
    response_model=DogResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Koirat"],
)
def create_dog(payload: DogCreate, db: Session = Depends(get_db)):
    return core_service.create_dog(
        db,
        name=payload.name,
        breed=payload.breed,
        birth_date=payload.birth_date,
        notes=payload.notes,
    )


@router.put("/dogs/{dog_id}", response_model=DogResponse, tags=["Koirat"])
def update_dog(dog_id: int, payload: DogUpdate, db: Session = Depends(get_db)):
    return core_service.update_dog(
        db,
        dog_id=dog_id,
        name=payload.name,
        breed=payload.breed,
        birth_date=payload.birth_date,
        notes=payload.notes,
    )


@router.delete("/dogs/{dog_id}", tags=["Koirat"])
def delete_dog(dog_id: int, db: Session = Depends(get_db)):
    core_service.delete_dog(db, dog_id)
    return {"message": "Koira poistettu"}


@router.get(
    "/trainings",
    response_model=list[TrainingSessionResponse],
    tags=["Treenit"],
)
def get_training_sessions(db: Session = Depends(get_db)):
    return core_service.get_all_training_sessions(db)


@router.get(
    "/trainings/{training_id}",
    response_model=TrainingSessionResponse,
    tags=["Treenit"],
)
def get_training_session(training_id: int, db: Session = Depends(get_db)):
    return core_service.get_training_session_by_id(db, training_id)


@router.post(
    "/trainings",
    response_model=TrainingSessionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Treenit"],
)
def create_training_session(
    payload: TrainingSessionCreate, db: Session = Depends(get_db)
):
    return core_service.create_training_session(
        db,
        dog_id=payload.dog_id,
        training_date=payload.date,
        duration_minutes=payload.duration_minutes,
    training_type=payload.training_type,
        location=payload.location,
        notes=payload.notes,
    )


@router.put(
    "/trainings/{training_id}",
    response_model=TrainingSessionResponse,
    tags=["Treenit"],
)
def update_training_session(
    training_id: int,
    payload: TrainingSessionUpdate,
    db: Session = Depends(get_db),
):
    return core_service.update_training_session(
        db,
        training_id=training_id,
        training_date=payload.date,
        duration_minutes=payload.duration_minutes,
    training_type=payload.training_type,
        location=payload.location,
        notes=payload.notes,
    )


@router.delete("/trainings/{training_id}", tags=["Treenit"])
def delete_training_session(training_id: int, db: Session = Depends(get_db)):
    core_service.delete_training_session(db, training_id)
    return {"message": "Treeni poistettu"}


@router.get("/ui/api/trainings", tags=["Kayttoliittyma"])
def get_ui_training_data(db: Session = Depends(get_db)):
    trainings = core_service.get_training_overview_rows(db)
    return {
        "message": "Treenit ja harjoitukset haettu",
        "count": len(trainings),
        "trainings": trainings,
    }


@router.get("/ui", response_class=HTMLResponse, tags=["Kayttoliittyma"])
def training_overview_page(db: Session = Depends(get_db)):
    trainings = core_service.get_training_overview_rows(db)

    cards = []
    for row in trainings:
        workouts = row["workouts"]
        if workouts:
            workout_items = "".join(
                [
                    "<li><strong>{}</strong> ({}) - onnistuminen: {}</li>".format(
                        workout["name"],
                        workout["category"] or "ei luokkaa",
                        workout["success_rating"]
                        if workout["success_rating"] is not None
                        else "ei arvioitu",
                    )
                    for workout in workouts
                ]
            )
        else:
            workout_items = "<li>Ei kirjattuja harjoituksia</li>"

        cards.append(
            """
            <article class='card'>
              <h2>{dog_name} - {date}</h2>
              <p><strong>Rotu:</strong> {dog_breed}</p>
              <p><strong>Kesto:</strong> {duration} min</p>
              <p><strong>Harjoituslaji:</strong> {training_type}</p>
              <p><strong>Paikka:</strong> {location}</p>
              <p><strong>Muistiinpanot:</strong> {notes}</p>
              <p><strong>Harjoituksia:</strong> {workout_count}</p>
              <ul>{workout_items}</ul>
            </article>
            """.format(
                dog_name=row["dog"]["name"],
                date=row["date"],
                dog_breed=row["dog"]["breed"],
                duration=row["duration_minutes"],
                training_type=row["training_type"] or "ei asetettu",
                location=row["location"] or "ei asetettu",
                notes=row["notes"] or "ei muistiinpanoja",
                workout_count=row["workout_count"],
                workout_items=workout_items,
            )
        )

    if not cards:
            cards_markup = "<p class='empty'>Ei treenejä vielä.</p>"
    else:
        cards_markup = "".join(cards)

    html = """
    <!doctype html>
    <html lang='fi'>
    <head>
      <meta charset='utf-8'>
      <meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>Koiran treenipäiväkirja</title>
      <style>
        :root {
          color-scheme: light;
          --bg: #f7f5f0;
          --panel: #fffdf8;
          --text: #1f1b16;
          --muted: #5b534a;
          --accent: #2d6a4f;
          --border: #d9d2c7;
        }
        body {
          margin: 0;
          font-family: "Segoe UI", Tahoma, sans-serif;
          background:
            radial-gradient(circle at 15% 10%, #e9f5ec 0%, transparent 36%),
            radial-gradient(circle at 85% 0%, #f4ece1 0%, transparent 32%),
            var(--bg);
          color: var(--text);
        }
        .container {
          max-width: 900px;
          margin: 0 auto;
          padding: 2rem 1rem 4rem;
        }
        h1 {
          margin: 0 0 0.25rem;
          font-size: 2rem;
          line-height: 1.1;
        }
        .subtitle {
          color: var(--muted);
          margin: 0 0 1.25rem;
        }
        .toolbar {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 1rem;
          color: var(--muted);
        }
        .cards {
          display: grid;
          gap: 1rem;
        }
        .card {
          background: var(--panel);
          border: 1px solid var(--border);
          border-radius: 14px;
          padding: 1rem;
          box-shadow: 0 6px 18px rgba(28, 24, 18, 0.06);
        }
        .card h2 {
          margin-top: 0;
          font-size: 1.2rem;
        }
        ul {
          margin: 0.6rem 0 0;
          padding-left: 1.2rem;
        }
        .empty {
          background: var(--panel);
          border: 1px dashed var(--border);
          border-radius: 12px;
          padding: 1rem;
          color: var(--muted);
        }
        a.api-link {
          color: var(--accent);
          text-decoration: none;
          font-weight: 600;
        }
      </style>
    </head>
    <body>
      <main class='container'>
        <h1>Koiran treenit ja harjoitukset</h1>
        <p class='subtitle'>Listaus koiran treeneistä, kestosta, harjoituslajista ja harjoituksista.</p>
        <div class='toolbar'>
          <span>JSON-näkymä:</span>
          <a class='api-link' href='/ui/api/trainings'>/ui/api/trainings</a>
        </div>
        <section class='cards'>{cards_markup}</section>
      </main>
    </body>
    </html>
    """

    return html.replace("{cards_markup}", cards_markup)


@router.get("/ui/new", response_class=HTMLResponse, tags=["Kayttoliittyma"])
def training_entry_page():
    html = """
    <!doctype html>
    <html lang='fi'>
    <head>
      <meta charset='utf-8'>
      <meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>Lisää koira ja treeni</title>
      <style>
        :root {
          color-scheme: light;
          --bg: #f7f5f0;
          --panel: #fffdf8;
          --text: #1f1b16;
          --muted: #5b534a;
          --accent: #2d6a4f;
          --accent-strong: #1f4c38;
          --border: #d9d2c7;
          --danger: #8a2332;
        }
        * {
          box-sizing: border-box;
        }
        body {
          margin: 0;
          font-family: "Segoe UI", Tahoma, sans-serif;
          background:
            radial-gradient(circle at 12% 10%, #eaf4ee 0%, transparent 35%),
            radial-gradient(circle at 90% 0%, #f3eadf 0%, transparent 30%),
            var(--bg);
          color: var(--text);
        }
        .container {
          max-width: 980px;
          margin: 0 auto;
          padding: 2rem 1rem 3rem;
        }
        h1 {
          margin: 0;
          font-size: 2rem;
          line-height: 1.1;
        }
        .subtitle {
          margin: 0.5rem 0 1.5rem;
          color: var(--muted);
        }
        .top-links {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          margin-bottom: 1.2rem;
        }
        .top-links a {
          color: var(--accent);
          text-decoration: none;
          font-weight: 600;
        }
        .layout {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1rem;
        }
        .panel {
          background: var(--panel);
          border: 1px solid var(--border);
          border-radius: 14px;
          padding: 1rem;
          box-shadow: 0 8px 20px rgba(28, 24, 18, 0.08);
        }
        h2 {
          margin-top: 0;
          margin-bottom: 0.75rem;
          font-size: 1.25rem;
        }
        .field {
          display: grid;
          gap: 0.3rem;
          margin-bottom: 0.8rem;
        }
        label {
          font-size: 0.95rem;
          color: var(--muted);
        }
        input,
        textarea,
        select,
        button {
          font: inherit;
        }
        input,
        textarea,
        select {
          border: 1px solid var(--border);
          border-radius: 10px;
          padding: 0.6rem 0.7rem;
          background: #fff;
          color: var(--text);
        }
        textarea {
          min-height: 90px;
          resize: vertical;
        }
        button {
          border: 0;
          border-radius: 10px;
          padding: 0.7rem 1rem;
          background: var(--accent);
          color: #fff;
          font-weight: 600;
          cursor: pointer;
          transition: transform 120ms ease, background 120ms ease;
        }
        button:hover {
          background: var(--accent-strong);
          transform: translateY(-1px);
        }
        .message {
          margin-top: 0.75rem;
          padding: 0.65rem 0.75rem;
          border-radius: 10px;
          font-size: 0.95rem;
        }
        .message.ok {
          background: #e7f5ec;
          color: #17452f;
        }
        .message.error {
          background: #fdecef;
          color: var(--danger);
        }
        .message.info {
          background: #f1efe9;
          color: #4d463f;
        }
        .notes {
          margin-top: 1rem;
          color: var(--muted);
          font-size: 0.95rem;
        }
        @media (max-width: 860px) {
          .layout {
            grid-template-columns: 1fr;
          }
        }
      </style>
    </head>
    <body>
      <main class='container'>
        <h1>Lisää koira ja treeni</h1>
        <p class='subtitle'>Tällä sivulla voit lisätä uuden koiran ja kirjata treenin suoraan selaimesta.</p>
        <div class='top-links'>
          <a href='/ui'>Avaa treenien listaus</a>
          <a href='/docs'>Avaa Swagger UI</a>
          <a href='/ui/api/trainings'>Avaa UI JSON</a>
        </div>

        <section class='layout'>
          <article class='panel'>
            <h2>1) Lisää koira</h2>
            <form id='dog-form'>
              <div class='field'>
                <label for='dog-name'>Nimi</label>
                <input id='dog-name' name='name' required maxlength='100'>
              </div>
              <div class='field'>
                <label for='dog-breed'>Rotu</label>
                <input id='dog-breed' name='breed' required maxlength='100'>
              </div>
              <div class='field'>
                <label for='dog-birth-date'>Syntymäaika</label>
                <input id='dog-birth-date' name='birth_date' type='date'>
              </div>
              <div class='field'>
                <label for='dog-notes'>Muistiinpanot</label>
                <textarea id='dog-notes' name='notes'></textarea>
              </div>
              <button type='submit'>Tallenna koira</button>
            </form>
            <div id='dog-message' class='message info'>Ei toimenpiteitä vielä.</div>
          </article>

          <article class='panel'>
            <h2>2) Lisää treeni</h2>
            <form id='training-form'>
              <div class='field'>
                <label for='training-dog-id'>Koira</label>
                <select id='training-dog-id' name='dog_id' required>
                  <option value=''>Ladataan koiria...</option>
                </select>
              </div>
              <div class='field'>
                <label for='training-date'>Päivämäärä</label>
                <input id='training-date' name='date' type='date' required>
              </div>
              <div class='field'>
                <label for='training-duration'>Kesto (min)</label>
                <input id='training-duration' name='duration_minutes' type='number' min='1' required>
              </div>
              <div class='field'>
                <label for='training-type'>Harjoituslaji</label>
                <input id='training-type' name='training_type' maxlength='80'>
              </div>
              <div class='field'>
                <label for='training-location'>Paikka</label>
                <input id='training-location' name='location' maxlength='150'>
              </div>
              <div class='field'>
                <label for='training-notes'>Muistiinpanot</label>
                <textarea id='training-notes' name='notes'></textarea>
              </div>
              <button type='submit'>Tallenna treeni</button>
            </form>
            <div id='training-message' class='message info'>Ei toimenpiteitä vielä.</div>
          </article>
        </section>

        <p class='notes'>Vinkki: lisää ensin koira, sitten treeni. Uusi koira päivitetään automaattisesti koiravalintaan.</p>
      </main>

      <script>
        const dogForm = document.getElementById('dog-form');
        const trainingForm = document.getElementById('training-form');
        const dogSelect = document.getElementById('training-dog-id');
        const dogMessage = document.getElementById('dog-message');
        const trainingMessage = document.getElementById('training-message');

        function showMessage(element, type, text) {
          element.className = 'message ' + type;
          element.textContent = text;
        }

        async function loadDogs(selectedId = null) {
          try {
            const response = await fetch('/dogs');
            if (!response.ok) {
              throw new Error('Koirien lataus epäonnistui.');
            }
            const dogs = await response.json();
            dogSelect.innerHTML = "<option value=''>Valitse koira</option>";

            for (const dog of dogs) {
              const option = document.createElement('option');
              option.value = String(dog.id);
              option.textContent = dog.name + ' (' + dog.breed + ')';
              if (selectedId !== null && Number(selectedId) === Number(dog.id)) {
                option.selected = true;
              }
              dogSelect.appendChild(option);
            }

            if (dogs.length === 0) {
              showMessage(trainingMessage, 'info', 'Lisää ensin koira ennen treenin tallennusta.');
            }
          } catch (error) {
            showMessage(trainingMessage, 'error', error.message || 'Koirien lataus epäonnistui.');
          }
        }

        dogForm.addEventListener('submit', async function (event) {
          event.preventDefault();
          const formData = new FormData(dogForm);
          const payload = {
            name: String(formData.get('name') || '').trim(),
            breed: String(formData.get('breed') || '').trim(),
            birth_date: formData.get('birth_date') || null,
            notes: String(formData.get('notes') || '').trim() || null
          };

          try {
            const response = await fetch('/dogs', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (!response.ok) {
              throw new Error(data.detail || 'Koiran tallennus epäonnistui.');
            }

            showMessage(dogMessage, 'ok', 'Koira lisätty: #' + data.id + ' ' + data.name);
            dogForm.reset();
            await loadDogs(data.id);
          } catch (error) {
            showMessage(dogMessage, 'error', error.message || 'Koiran tallennus epäonnistui.');
          }
        });

        trainingForm.addEventListener('submit', async function (event) {
          event.preventDefault();
          const formData = new FormData(trainingForm);
          const payload = {
            dog_id: Number(formData.get('dog_id')),
            date: formData.get('date'),
            duration_minutes: Number(formData.get('duration_minutes')),
            training_type: String(formData.get('training_type') || '').trim() || null,
            location: String(formData.get('location') || '').trim() || null,
            notes: String(formData.get('notes') || '').trim() || null
          };

          try {
            const response = await fetch('/trainings', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (!response.ok) {
              throw new Error(data.detail || 'Treenin tallennus epäonnistui.');
            }

            showMessage(trainingMessage, 'ok', 'Treeni lisätty: #' + data.id + ' päivälle ' + data.date);
            trainingForm.reset();
            if (payload.dog_id) {
              await loadDogs(payload.dog_id);
            } else {
              await loadDogs();
            }
          } catch (error) {
            showMessage(trainingMessage, 'error', error.message || 'Treenin tallennus epäonnistui.');
          }
        });

        loadDogs();
      </script>
    </body>
    </html>
    """

    return html
