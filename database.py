from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Az SQLite adatbázis fájl neve, ami automatikusan létrejön a mappában
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# Létrehozzuk az adatbázis motort
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Létrehozzuk a munkamenet (Session) gyárat
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Az adatbázis modellek alaposztálya
Base = declarative_base()

# Függvény, ami biztosítja az adatbázis kapcsolatot a kérések idejére
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()