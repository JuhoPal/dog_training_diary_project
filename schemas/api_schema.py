from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class DogBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    breed: str = Field(min_length=1, max_length=100)
    birth_date: date | None = None
    notes: str | None = None


class DogCreate(DogBase):
    pass


class DogUpdate(DogBase):
    pass


class DogResponse(DogBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TrainingSessionBase(BaseModel):
    date: date
    duration_minutes: int = Field(gt=0)
    location: str | None = Field(default=None, max_length=150)
    notes: str | None = None


class TrainingSessionCreate(TrainingSessionBase):
    dog_id: int = Field(gt=0)


class TrainingSessionUpdate(TrainingSessionBase):
    pass


class TrainingSessionResponse(TrainingSessionBase):
    id: int
    dog_id: int

    model_config = ConfigDict(from_attributes=True)
