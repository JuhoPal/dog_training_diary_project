from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class TrainingSession(Base):
	__tablename__ = "training_sessions"

	id = Column(Integer, primary_key=True, index=True)
	dog_id = Column(Integer, ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False)
	date = Column(Date, nullable=False)
	duration_minutes = Column(Integer, nullable=False)
	location = Column(String(150), nullable=True)
	notes = Column(Text, nullable=True)

	dog = relationship("Dog", back_populates="training_sessions")
	exercises = relationship(
		"Exercise", back_populates="training_session", cascade="all, delete-orphan"
	)
