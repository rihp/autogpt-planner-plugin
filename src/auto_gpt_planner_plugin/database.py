from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Task

# Generate a unique identifier
uuid_str = str(uuid.uuid4())

# Use the UUID to create a unique database name
db_name = f"tasks_{uuid_str}.db"

# Create an engine that stores data in the local SQLite file named tasks.db
engine = create_engine(f'sqlite:///{db_name}')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
