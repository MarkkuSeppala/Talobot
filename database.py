from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  # Base pitää olla määritelty


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



class Toimitussisalto(Base):
    __tablename__ = "toimitussisallot"

    id = Column(Integer, primary_key=True)
    kayttaja_id = Column(Integer, ForeignKey("kayttajat.id", ondelete="CASCADE"))
    toimittaja_id = Column(Integer, ForeignKey("toimittajat.id", ondelete="SET NULL"))
    uuid = Column(String, unique=True, nullable=False)
    pdf_url = Column(String, nullable=False)
    txt_sisalto = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    aktiivinen = Column(Boolean, default=True)