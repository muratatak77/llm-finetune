# create_db.py

from models.schema import Base
from utils.db import engine

Base.metadata.create_all(bind=engine)
print("Database tables created.")
