from fastapi import FastAPI

from database import Base, engine, ensure_training_session_schema
from routers.api_router import router as api_router

import models.competition
import models.dog
import models.exercise
import models.training_session


Base.metadata.create_all(bind=engine)
ensure_training_session_schema()

app = FastAPI(title="Dog Training Diary API")

app.include_router(api_router)


@app.get("/")
def root():
	return {"message": "Koiran treenipäiväkirjan API"}
