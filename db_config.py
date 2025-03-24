from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

import psycopg2

#from database import Base  # Base pitää olla määritelty


# 🔹 Lataa ympäristömuuttujat
#load_dotenv("ymparistomuuttujat.env")

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


class Ikkunat(Base):
    __tablename__ = "ikkunat"
    id = Column(Integer, primary_key=True)
    leveys = Column(Integer)
    korkeus = Column(Integer)
    turvalasi = Column(Boolean)
    valikarmi = Column(Boolean)
    salekaihtimet = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    toimitussisalto_id = Column(Integer, ForeignKey("toimitussisallot.id", ondelete="CASCADE"))


class UlkoOvet(Base):
    __tablename__ = "ulko_ovet"
    id = Column(Integer, primary_key=True)
    malli = Column(String(255), nullable=False)
    paloluokitus_EI_15 = Column(Boolean)
    maara = Column(Integer)
    luotu = Column(DateTime, default=datetime.utcnow)
    toimitussisalto_id = Column(Integer, ForeignKey("toimitussisallot.id", ondelete="CASCADE"))


class Valiovet(Base):
    __tablename__ = "valiovet"
    id = Column(Integer, primary_key=True)
    malli = Column(String(255), nullable=False)
    luotu = Column(DateTime, default=datetime.utcnow)
    toimitussisalto_id = Column(Integer, ForeignKey("toimitussisallot.id", ondelete="CASCADE"))


class Materiaalikategoriat(Base):
    __tablename__ = "materiaalikategoriat"
    id = Column(Integer, primary_key=True)
    nimi = Column(String(100), nullable=False)
    kuvaus = Column(Text)


class MateriaalitJaPalvelut(Base):
    __tablename__ = "materiaalit_ja_palvelut"
    id = Column(Integer, primary_key=True)
    kategoria_id = Column(Integer, ForeignKey("materiaalikategoriat.id", ondelete="SET NULL"))
    nimi = Column(String(100), nullable=False)
    yksikko = Column(String(50), nullable=False)
    hinta = Column(DECIMAL(10,2))


class ToimitussisaltoMateriaalitJaPalvelut(Base):
    __tablename__ = "toimitussisalto_materiaalit_ja_palvelut"
    id = Column(Integer, primary_key=True)
    toimitussisalto_id = Column(Integer, ForeignKey("toimitussisallot.id", ondelete="CASCADE"))
    materiaali_id = Column(Integer, ForeignKey("materiaalit_ja_palvelut.id", ondelete="CASCADE"))
    maara = Column(DECIMAL(10,2), nullable=False)
    hinta_yksikko = Column(DECIMAL(10,2))
    hinta = Column(DECIMAL(10,2))
    luotu = Column(DateTime, default=datetime.utcnow)

