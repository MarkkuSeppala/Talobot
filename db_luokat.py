from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy.sql import func


import psycopg2

#from database import Base  # Base pitää olla määritelty


# 🔹 Lataa ympäristömuuttujat
#load_dotenv("ymparistomuuttujat.env")

# 🔹 Hae tietokantayhteys
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL ei ole asetettu! Tarkista .env-tiedosto.")

def create_robust_engine(url):
    """
    Luo vakaan tietokantayhteyden, joka kestää yhteysongelmia.
    
    Args:
        url (str): Tietokantayhteyden URL
        
    Returns:
        Engine: SQLAlchemy engine-objekti
    """
    return create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5
        }
    )

# 🔹 Luo SQLAlchemy-moottori
engine = create_robust_engine(DATABASE_URL)

# 🔹 Luo istunto (Session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 ORM-perusta malleille
Base = declarative_base()





class Toimitussisalto(Base):
    __tablename__ = "toimitussisallot"
    id = Column(Integer, primary_key=True)
    kayttaja_id = Column(Integer, nullable=False)
    toimittaja_id = Column(Integer, nullable=True)
    alkuperainen_tiedosto_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    aktiivinen = Column(Boolean, nullable=False)
    jarjestysnro = Column(Integer, nullable=True)
    uuid = Column(String(36), nullable=False)
    pdf_url = Column(Text, nullable=False)
    txt_url = Column(Text, nullable=False)
    toimittaja = Column(String(100), nullable=False)

    ikkunat = relationship("Ikkuna", back_populates="toimitussisalto", cascade="all, delete-orphan")


class Kayttaja(Base):
    __tablename__ = "kayttajat"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    salasana_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    viimeksi_kirjautunut = Column(DateTime)
    aktiivinen = Column(Boolean, default=True)


class Toimittaja(Base):
    __tablename__ = "toimittajat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nimi = Column(String(100), nullable=False, unique=True)  # Pituus 100, kuten tietokannassa
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)  # Vastaamaan tietokannan määrittelyä


class Ikkuna(Base):
    __tablename__ = "ikkunat"
    id = Column(Integer, primary_key=True)
    leveys = Column(Integer)
    korkeus = Column(Integer)
    turvalasi = Column(Boolean)
    valikarmi = Column(Boolean)
    salekaihtimet = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    toimitussisalto_id = Column(Integer, ForeignKey("toimitussisallot.id", ondelete="CASCADE"))

    toimitussisalto = relationship("Toimitussisalto", back_populates="ikkunat")



class Ulko_ovi(Base):
    __tablename__ = "ulko_ovet"
    id = Column(Integer, primary_key=True)
    malli = Column(String(255), nullable=False)
    paloluokitus_EI_15 = Column(Boolean)
    lukko = Column(String(255), nullable=False)
    maara = Column(Integer)
    luotu = Column(DateTime, default=datetime.utcnow, nullable=True)
    toimitussisalto_id = Column(Integer, ForeignKey("toimitussisallot.id", ondelete="CASCADE"))


class Valiovi(Base):
    __tablename__ = "valiovet"
    id = Column(Integer, primary_key=True)
    malli = Column(String(255), nullable=False)
    luotu = Column(DateTime, default=datetime.utcnow)
    toimitussisalto_id = Column(Integer, ForeignKey("toimitussisallot.id", ondelete="CASCADE"))


class Materiaalikategoria(Base):
    __tablename__ = "materiaalikategoriat"
    id = Column(Integer, primary_key=True)
    nimi = Column(String(100), nullable=False)
    kuvaus = Column(Text)


class Materiaali_ja_palvelu(Base):
    __tablename__ = "materiaalit_ja_palvelut"
    id = Column(Integer, primary_key=True)
    kategoria_id = Column(Integer, ForeignKey("materiaalikategoriat.id", ondelete="SET NULL"))
    nimi = Column(String(100), nullable=False)
    yksikko = Column(String(50), nullable=False)
    hinta = Column(DECIMAL(10,2))


class Tuote(Base):
    __tablename__ = "tuotteet"
    id = Column(Integer, primary_key=True)
    version_number = Column(Integer, nullable=True)
    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)
    prompt_1 = Column(Boolean, nullable=False)
    prompt_2 = Column(Boolean, nullable=False)
    prompt_3 = Column(Boolean, nullable=False)
    tuote = Column(String(100), nullable=False)
    yksikko = Column(String(50), nullable=True)
    hinta = Column(DECIMAL(10, 2), nullable=True)
    absoluuttinen_hinta = Column(Boolean, nullable=False, default=False)
    tarkenne_yleinen = Column(String(100), nullable=True)
    tarkenne_sievitalo = Column(String(100), nullable=True)
    tarkenne_kastelli = Column(String(100), nullable=True)
    tarkenne_designtalo = Column(String(100), nullable=True)
    tarkenne_jopera = Column(String(100), nullable=True)
    tarkenne_kannustalo = Column(String(100), nullable=True)
    tarkenne_kylatimpurit = Column(String(100), nullable=True)
    tarkenne_ainoakoti = Column(String(100), nullable=True)
        
    viite_tuote_id = Column(Integer, ForeignKey("tuotteet.id"), nullable=True)

    # Suhde: viittaa toiseen tuotteeseen, jos hinta ei ole absoluuttinen
    viite_tuote = relationship("Tuote", remote_side=[id], backref="suhteelliset_hinnat")


class Toimitussisalto_tuotteet(Base):
    __tablename__ = "toimitussisalto_tuotteet"
    id = Column(Integer, primary_key=True)
    toimitussisalto_id = Column(Integer, ForeignKey("toimitussisallot.id", ondelete="CASCADE"))
    tuote_id = Column(Integer, ForeignKey("tuotteet.id", ondelete="CASCADE"))
    tuote_nimi_toimitussisallossa = Column(String(50), nullable=False)
    maara = Column(DECIMAL(10,2), nullable=False)
    luotu = Column(DateTime, default=datetime.utcnow)


def hae_toimitussisalto(toimitussisalto_id: int) -> None:
    """
    Hakee ja tulostaa toimitussisällön tiedot ID:n perusteella.
    
    Args:
        toimitussisalto_id: Haettavan toimitussisällön ID
    """
    try:
        with SessionLocal() as db:
            toimitussisalto = db.query(Toimitussisalto).filter(Toimitussisalto.id == toimitussisalto_id).first()
            
            if not toimitussisalto:
                print(f"Toimitussisältöä ID:llä {toimitussisalto_id} ei löytynyt.")
                return
            
            print(f"Toimitussisällön tiedot (ID: {toimitussisalto_id}):")
            print("-" * 50)
            print(f"Käyttäjä ID: {toimitussisalto.kayttaja_id}")
            print(f"Toimittaja ID: {toimitussisalto.toimittaja_id}")
            print(f"Alkuperäinen tiedosto: {toimitussisalto.alkuperainen_tiedosto_url}")
            print(f"Luotu: {toimitussisalto.created_at}")
            print(f"Aktiivinen: {toimitussisalto.aktiivinen}")
            print(f"Järjestysnumero: {toimitussisalto.jarjestysnro}")
            print(f"UUID: {toimitussisalto.uuid}")
            print(f"PDF URL: {toimitussisalto.pdf_url}")
            print(f"TXT URL: {toimitussisalto.txt_url}")
            print(f"Toimittaja: {toimitussisalto.toimittaja}")
            
            # Tulostetaan myös liittyvät ikkunat
            print("\nLiittyvät ikkunat:")
            for ikkuna in toimitussisalto.ikkunat:
                print(f"- Ikkuna ID: {ikkuna.id}")
                
    except Exception as e:
        print(f"❌ Virhe toimitussisällön haussa: {str(e)}")


class Vertailut(Base):
    __tablename__ = 'vertailut'

    id = Column(Integer, primary_key=True)
    toimitussisalto_1_id = Column(Integer, ForeignKey('toimitussisallot.id', ondelete='CASCADE'), nullable=False)
    toimitussisalto_2_id = Column(Integer, ForeignKey('toimitussisallot.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Vertailu(id={self.id}, toimitussisalto_1_id={self.toimitussisalto_1_id}, toimitussisalto_2_id={self.toimitussisalto_2_id})>"
