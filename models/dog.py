from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Dog(Base):
	__tablename__ = "dogs"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(100), nullable=False)
	breed = Column(String(100), nullable=False)
	birth_date = Column(Date, nullable=True)
	notes = Column(Text, nullable=True)

	training_sessions = relationship(
		"TrainingSession", back_populates="dog", cascade="all, delete-orphan"
	)
	competitions = relationship(
		"Competition", back_populates="dog", cascade="all, delete-orphan"
	)
