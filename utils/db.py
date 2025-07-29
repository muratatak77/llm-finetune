from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Veritabanı bağlantı ayarları
DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/ai_vet_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
