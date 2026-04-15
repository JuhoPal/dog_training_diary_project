from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from models.dog import Dog
from models.training_session import TrainingSession


def get_all_dogs(db: Session):
    return db.query(Dog).order_by(Dog.id.asc()).all()


def get_dog_by_id(db: Session, dog_id: int):
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Koiraa ei löytynyt")
    return dog


def create_dog(
    db: Session,
    name: str,
    breed: str,
    birth_date: date | None = None,
    notes: str | None = None,
):
    dog = Dog(name=name, breed=breed, birth_date=birth_date, notes=notes)
    db.add(dog)
    db.commit()
    db.refresh(dog)
    return dog


def update_dog(
    db: Session,
    dog_id: int,
    name: str,
    breed: str,
    birth_date: date | None = None,
    notes: str | None = None,
):
    dog = get_dog_by_id(db, dog_id)
    dog.name = name
    dog.breed = breed
    dog.birth_date = birth_date
    dog.notes = notes
    db.commit()
    db.refresh(dog)
    return dog


def delete_dog(db: Session, dog_id: int):
    dog = get_dog_by_id(db, dog_id)
    db.delete(dog)
    db.commit()


def get_all_training_sessions(db: Session):
    return db.query(TrainingSession).order_by(TrainingSession.date.desc()).all()


def get_training_session_by_id(db: Session, training_id: int):
    session = db.query(TrainingSession).filter(TrainingSession.id == training_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Treeniä ei löytynyt")
    return session


def create_training_session(
    db: Session,
    dog_id: int,
    training_date: date,
    duration_minutes: int,
    location: str | None = None,
    notes: str | None = None,
):
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Koiraa ei löytynyt")

    session = TrainingSession(
        dog_id=dog_id,
        date=training_date,
        duration_minutes=duration_minutes,
        location=location,
        notes=notes,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def update_training_session(
    db: Session,
    training_id: int,
    training_date: date,
    duration_minutes: int,
    location: str | None = None,
    notes: str | None = None,
):
    session = get_training_session_by_id(db, training_id)
    session.date = training_date
    session.duration_minutes = duration_minutes
    session.location = location
    session.notes = notes
    db.commit()
    db.refresh(session)
    return session


def delete_training_session(db: Session, training_id: int):
    session = get_training_session_by_id(db, training_id)
    db.delete(session)
    db.commit()


def get_training_overview_rows(db: Session):
    sessions = (
        db.query(TrainingSession)
        .options(
            joinedload(TrainingSession.dog),
            joinedload(TrainingSession.exercises),
        )
        .order_by(TrainingSession.date.desc())
        .all()
    )

    rows = []
    for session in sessions:
        workouts = [
            {
                "id": exercise.id,
                "name": exercise.name,
                "category": exercise.category,
                "success_rating": exercise.success_rating,
                "notes": exercise.notes,
            }
            for exercise in session.exercises
        ]

        rows.append(
            {
                "training_id": session.id,
                "date": str(session.date),
                "duration_minutes": session.duration_minutes,
                "location": session.location,
                "notes": session.notes,
                "dog": {
                    "id": session.dog.id,
                    "name": session.dog.name,
                    "breed": session.dog.breed,
                },
                "workout_count": len(workouts),
                "workouts": workouts,
            }
        )

    return rows
