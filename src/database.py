# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///tasks.db')  # Use an SQLite database file named tasks.db
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)  # Create the tasks table
