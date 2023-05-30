# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Create an engine that stores data in the local SQLite file named tasks.db
engine = create_engine('sqlite:///tasks.db')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
