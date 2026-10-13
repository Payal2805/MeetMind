
from app.database import engine
from app.models import Base
from app import models

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("MeetMind database tables created successfully!")


if __name__ == "__main__":
    create_tables()
    