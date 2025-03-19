from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

#from database import Base  # Base pitää olla määritelty


# 🔹 Lataa ympäristömuuttujat
load_dotenv("ymparistomuuttujat.env")

# 🔹 Hae tietokantayhteys
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL ei ole asetettu! Tarkista .env-tiedosto.")

# 🔹 Luo SQLAlchemy-moottori
engine = create_engine(DATABASE_URL)

# 🔹 Luo istunto (Session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 ORM-perusta malleille
Base = declarative_base()



class Toimitussisallot(Base):
    __tablename__ = "toimitussisallot"  # Varmista, että nimi on pienillä kirjaimilla!

    id = Column(Integer, primary_key=True)
    kayttaja_id = Column(Integer, ForeignKey("kayttajat.id", ondelete="SET NULL"), nullable=False)
    toimittaja_id = Column(Integer, ForeignKey("toimittajat.id", ondelete="SET NULL"), nullable=True)
    uuid = Column(String(36), unique=True, nullable=False)
    pdf_url = Column(Text, nullable=False)
    txt_sisalto = Column(Text, nullable=False)
    toimittaja = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    aktiivinen = Column(Boolean, default=True, nullable=False)
    jarjestysnro = Column(Integer, nullable=True)


class Kayttajat(Base):
    __tablename__ = "kayttajat"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    salasana_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    viimeksi_kirjautunut = Column(DateTime)
    aktiivinen = Column(Boolean, default=True)

class Toimittajat(Base):
    __tablename__ = "toimittajat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nimi = Column(String(100), nullable=False, unique=True)  # Pituus 100, kuten tietokannassa
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)  # Vastaamaan tietokannan määrittelyä
