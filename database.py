import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from sqlalchemy import DECIMAL
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Text

DATABASE_URL = "postgresql://eka_tietokanta_user:Ipi86uNZg0FCRXcCSzGODzIteTVqUcyS@dpg-cvbac9jtq21c73dt8ho0-a.oregon-postgres.render.com/eka_tietokanta"

from sqlalchemy import create_engine, text

Base = declarative_base()

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("✅ Yhteys PostgreSQL-tietokantaan on muodostettu!")

        # Käytä text()-funktiota SQL-kyselyissä
        result = connection.execute(text("SELECT current_database();"))
        for row in result:
            print("🔹 Yhdistetty tietokantaan:", row[0])

except Exception as e:
    print("❌ Yhteyden muodostaminen epäonnistui:", e)


# 🔹 Taulujen määrittely
class Toimittajat(Base):
    __tablename__ = "toimittajat"
    id = Column(Integer, primary_key=True)
    nimi = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Kayttajat(Base):
    __tablename__ = "kayttajat"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    salasana_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    viimeksi_kirjautunut = Column(DateTime)
    aktiivinen = Column(Boolean, default=True)

class Toimitussisallot(Base):
    __tablename__ = "toimitussisallot"
    id = Column(Integer, primary_key=True)
    kayttaja_id = Column(Integer, ForeignKey("kayttajat.id", ondelete="CASCADE"))
    toimittaja_id = Column(Integer, ForeignKey("toimittajat.id", ondelete="SET NULL"))
    alkuperainen_tiedosto_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    aktiivinen = Column(Boolean, default=True)
    jarjestysnro = Column(Integer)

class Ikkunat(Base):
    __tablename__ = "ikkunat"
    id = Column(Integer, primary_key=True)
    leveys = Column(Integer)
    korkeus = Column(Integer)
    turvalasi = Column(Boolean)
    valikarmi = Column(Boolean)
    salekaihtimet = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now(datetime.UTC))
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

# 🔹 Luo kaikki taulut tietokantaan
Base.metadata.create_all(engine)

print("✅ Kaikki taulut on luotu onnistuneesti!")