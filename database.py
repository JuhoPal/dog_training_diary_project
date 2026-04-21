from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./dog_training_diary.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def ensure_training_session_schema():
	with engine.begin() as connection:
		columns = connection.execute(text("PRAGMA table_info(training_sessions)"))
		column_names = {row[1] for row in columns}

		if "training_type" not in column_names:
			connection.execute(
				text(
					"ALTER TABLE training_sessions "
					"ADD COLUMN training_type VARCHAR(80)"
				)
			)
