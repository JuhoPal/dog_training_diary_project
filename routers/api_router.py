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
                location=row["location"] or "ei asetettu",
                notes=row["notes"] or "ei muistiinpanoja",
                workout_count=row["workout_count"],
                workout_items=workout_items,
            )
        )

    if not cards:
        cards_markup = "<p class='empty'>Ei treeneja viela.</p>"
    else:
        cards_markup = "".join(cards)

    html = """
    <!doctype html>
    <html lang='fi'>
    <head>
      <meta charset='utf-8'>
      <meta name='viewport' content='width=device-width, initial-scale=1'>
      <title>Koiran treenipaivakirja</title>
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
        <p class='subtitle'>Listaus koiran treeneista, kestoista ja harjoituksista.</p>
        <div class='toolbar'>
          <span>JSON-nakyma:</span>
          <a class='api-link' href='/ui/api/trainings'>/ui/api/trainings</a>
        </div>
        <section class='cards'>{cards_markup}</section>
      </main>
    </body>
    </html>
    """

    return html.replace("{cards_markup}", cards_markup)
