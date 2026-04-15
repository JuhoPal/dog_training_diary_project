from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Exercise(Base):
	__tablename__ = "exercises"

	id = Column(Integer, primary_key=True, index=True)
	training_session_id = Column(
		Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False
	)
	name = Column(String(120), nullable=False)
	category = Column(String(80), nullable=True)
	success_rating = Column(Integer, nullable=True)
	notes = Column(Text, nullable=True)

	training_session = relationship("TrainingSession", back_populates="exercises")
