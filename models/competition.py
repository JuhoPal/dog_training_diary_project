from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Competition(Base):
	__tablename__ = "competitions"

	id = Column(Integer, primary_key=True, index=True)
	dog_id = Column(Integer, ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False)
	event_name = Column(String(150), nullable=False)
	date = Column(Date, nullable=False)
	location = Column(String(150), nullable=True)
	result = Column(String(120), nullable=True)
	notes = Column(Text, nullable=True)

	dog = relationship("Dog", back_populates="competitions")
