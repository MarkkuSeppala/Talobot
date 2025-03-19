from sqlalchemy import text, create_engine
#from db_config import SessionLocal, Toimittajat
from db_config import SessionLocal, Toimitussisallot, Kayttajat, Toimittajat

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
#from db_config import Base, engine, SessionLocal
from datetime import datetime
import hashlib
#from sqlalchemy import create_engine


#==================================== get_all_tables()

def get_all_tables():
    """Tulostaa kaikki tietokannan taulut."""
    try:
        with SessionLocal() as db:
            query = text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = db.execute(query).fetchall()

            if not tables:
                print("❌ Ei yhtään taulua löydetty tietokannasta!")
                return

            print("\n🔹 **Tietokannan taulut:** 🔹")
            print("=" * 40)
            for table in tables:
                print(f"- {table[0]}")
            print("=" * 40)

    except Exception as e:
        print(f"❌ Virhe tietokantakyselyssä: {e}")

if __name__ == "__main__":
    #get_all_tables()
    print("🔹 Tulostetaan kaikki tietokannan taulut...")




#==================================== get_all_table_structures()

def get_all_table_structures():
    """Hakee ja näyttää kaikkien tietokannan taulujen rakenteet."""
    try:
        with SessionLocal() as db:
            # 🔹 Haetaan kaikki taulut `public`-skeemasta
            tables_query = text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = db.execute(tables_query).fetchall()

            if not tables:
                print("❌ Ei yhtään taulua löydetty tietokannasta!")
                return

            # 🔹 Käydään jokainen taulu läpi ja haetaan sen sarakkeet
            for table in tables:
                table_name = table[0]
                print(f"\n🔹 **Rakenne: {table_name}** 🔹")

                structure_query = text("""
                    SELECT column_name, data_type, character_maximum_length, is_nullable
                    FROM information_schema.columns
                    WHERE table_name = :table_name
                    ORDER BY ordinal_position;
                """)
                result = db.execute(structure_query, {"table_name": table_name}).fetchall()

                if not result:
                    print("❌ Ei yhtään saraketta tässä taulussa!")
                    continue

                print(f"{'Sarakkeen nimi':<25} {'Tietotyyppi':<25} {'Pituus':<10} {'NULL?':<10}")
                print("=" * 70)

                for row in result:
                    column_name, data_type, char_length, is_nullable = row
                    char_length = char_length if char_length else "-"
                    print(f"{column_name:<25} {data_type:<25} {char_length:<10} {is_nullable:<10}")

    except Exception as e:
        print(f"❌ Virhe tietokantakyselyssä: {e}")

if __name__ == "__main__":
    #get_all_table_structures()
    print("🔹 Päivitetään `toimitussisallot`-taulua...")





# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import ProgrammingError
# from db_config import Base, engine, SessionLocal
# from datetime import datetime

# ✅ Määritetään uusi taulurakenne
# class Toimitussisallot(Base):
#     __tablename__ = "toimitussisallot"

#     id = Column(Integer, primary_key=True)
#     kayttaja_id = Column(Integer, ForeignKey("kayttajat.id", ondelete="SET NULL"), nullable=False)
#     toimittaja_id = Column(Integer, ForeignKey("toimittajat.id", ondelete="SET NULL"), nullable=True)
#     uuid = Column(String(36), unique=True, nullable=False)
#     pdf_url = Column(Text, nullable=False)
#     txt_sisalto = Column(Text, nullable=False)
#     toimittaja = Column(String(100), nullable=False)  # Uusi sarake toimittajalle
#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
#     aktiivinen = Column(Boolean, default=True, nullable=False)
#     jarjestysnro = Column(Integer, nullable=True)

# ✅ Funktio, joka lisää puuttuvat sarakkeet ja muuttaa asetukset


#==================================== update_table()

def update_table():
    with SessionLocal() as db:
        try:
            print("🔹 Päivitetään `toimitussisallot`-taulua...")

            # 🔹 Lisätään puuttuvat sarakkeet (jos eivät ole olemassa)
            alter_statements = [
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS uuid VARCHAR(36) UNIQUE NOT NULL",
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS pdf_url TEXT NOT NULL",
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS txt_sisalto TEXT NOT NULL",
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS toimittaja VARCHAR(100) NOT NULL"
            ]

            # 🔹 Muutetaan sarakkeiden `NULL`-asetukset, jotta ne eivät voi olla tyhjiä
            alter_nullable_statements = [
                "ALTER TABLE toimitussisallot ALTER COLUMN kayttaja_id SET NOT NULL",
                "ALTER TABLE toimitussisallot ALTER COLUMN created_at SET NOT NULL",
                "ALTER TABLE toimitussisallot ALTER COLUMN aktiivinen SET NOT NULL"
            ]

            # 🔹 Suoritetaan kaikki ALTER TABLE -komennot
            for stmt in alter_statements + alter_nullable_statements:
                db.execute(text(stmt))

            db.commit()
            print("✅ `toimitussisallot`-taulu päivitetty onnistuneesti!")

        except ProgrammingError as e:
            db.rollback()
            print(f"❌ Virhe tietokantapäivityksessä: {e}")

if __name__ == "__main__":
    #update_table()
    print("🔹 Päivitetään `toimitussisallot`-taulua...")


#==================================== tulosta_toimitussisallot()

def tulosta_toimitussisallot():
    """Hakee ja tulostaa `toimitussisallot`-taulun sisällön."""
    try:
        with SessionLocal() as db:
            # 🔹 Hae kaikki tietueet
            toimitussisallot = db.query(Toimitussisallot).all()

            if not toimitussisallot:
                print("❌ Tietokanta on tyhjä! Ei toimitussisältöjä.")
                return

            print("\n🔹 **Toimitussisällöt tietokannassa:** 🔹")
            print("=" * 80)
            for sisalto in toimitussisallot:
                print(f"🔹 ID: {sisalto.id}")
                print(f"🔹 UUID: {sisalto.uuid}")
                print(f"🔹 PDF URL: {sisalto.pdf_url}")
                print(f"🔹 TXT URL: {sisalto.txt_sisalto}")
                print(f"🔹 Toimittaja: {sisalto.toimittaja}")
                print(f"🔹 Luotu: {sisalto.created_at}")
                print("-" * 80)

    except Exception as e:
        print(f"❌ Virhe tietokantakyselyssä: {str(e)}")

# 🔹 Aja funktio
if __name__ == "__main__":
    tulosta_toimitussisallot()
    print("🔹 Tulostetaan `toimitussisallot`-taulun sisältö...")



#==================================== add_user(email, password)


# ✅ Luo uusi istunto tietokantaa varten
def add_user(email, password):
    """Lisää uusi käyttäjä kayttajat-tauluun."""
    with SessionLocal() as db:
        # Tarkista, onko käyttäjä jo olemassa
        existing_user = db.query(Kayttajat).filter(Kayttajat.email == email).first()
        if existing_user:
            print(f"❌ Käyttäjä '{email}' on jo olemassa.")
            return
        
        # Hashaa salasana (ei suositeltu oikeassa käytössä, käytä bcrypt tai Argon2)
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Luo uusi käyttäjä
        new_user = Kayttajat(
            email="testi@testi.com",
            salasana_hash="testi",
            created_at=datetime.utcnow(),
            viimeksi_kirjautunut=None,
            aktiivinen=True
        )

        # Lisää tietokantaan ja tallenna muutokset
        db.add(new_user)
        db.commit()
        print(f"✅ Käyttäjä '{email}' lisätty onnistuneesti!")

# ✅ Suorita, jos skripti ajetaan suoraan
if __name__ == "__main__":
    #email = input("Anna käyttäjän sähköposti: ")
    #password = input("Anna käyttäjän salasana: ")
    
    #add_user(email, password)
    print("🔹 Lisätään käyttäjä...")

#from db_config import SessionLocal, Kayttajat

#==================================== tulosta_kayttajat()

def tulosta_kayttajat():
    """Hakee ja tulostaa `kayttajat`-taulun sisällön."""
    try:
        with SessionLocal() as db:
            # 🔹 Hae kaikki käyttäjät
            kayttajat = db.query(Kayttajat).all()

            if not kayttajat:
                print("❌ Tietokanta on tyhjä! Ei käyttäjiä.")
                return

            print("\n🔹 **Käyttäjät tietokannassa:** 🔹")
            print("=" * 80)
            for kayttaja in kayttajat:
                print(f"🔹 ID: {kayttaja.id}")
                print(f"🔹 Email: {kayttaja.email}")
                print(f"🔹 Salasana Hash: {kayttaja.salasana_hash}")
                print(f"🔹 Luotu: {kayttaja.created_at}")
                print(f"🔹 Viimeksi kirjautunut: {kayttaja.viimeksi_kirjautunut}")
                print(f"🔹 Aktiivinen: {'Kyllä' if kayttaja.aktiivinen else 'Ei'}")
                print("-" * 80)

    except Exception as e:
        print(f"❌ Virhe tietokantakyselyssä: {str(e)}")

# 🔹 Aja funktio
if __name__ == "__main__":
    #tulosta_kayttajat()
    print("🔹 Tulostetaan `kayttajat`-taulun sisältö...")

#from db_config import SessionLocal, Kayttajat



#==================================== aktivoi_kayttaja(kayttaja_id)

def aktivoi_kayttaja(kayttaja_id):
    """Asettaa käyttäjän aktiiviseksi `Kayttajat`-taulussa."""
    try:
        with SessionLocal() as db:
            # 🔹 Etsi käyttäjä ID:n perusteella
            kayttaja = db.query(Kayttajat).filter(Kayttajat.id == kayttaja_id).first()

            if not kayttaja:
                print(f"❌ Käyttäjää ID:llä {kayttaja_id} ei löytynyt.")
                return

            # 🔹 Päivitä aktiivisuus
            kayttaja.aktiivinen = True
            db.commit()
            print(f"✅ Käyttäjä ID:llä {kayttaja_id} on nyt aktiivinen!")

    except Exception as e:
        print(f"❌ Virhe käyttäjän aktivoinnissa: {str(e)}")

# 🔹 Aja funktio
if __name__ == "__main__":
    #kayttaja_id = int(input("Syötä käyttäjän ID, jonka haluat aktivoida: "))
    #aktivoi_kayttaja(kayttaja_id)
    print("🔹 Aktivoidaan käyttäjä...")


#from db_config import SessionLocal, Toimittajat


#==================================== tulosta_toimittajat()

def tulosta_toimittajat():
    """Hakee ja tulostaa `toimittajat`-taulun sisällön."""
    try:
        with SessionLocal() as db:
            # 🔹 Hae kaikki tietueet
            toimittajat = db.query(Toimittajat).all()

            if not toimittajat:
                print("❌ Toimittajat-taulu on tyhjä!")
                return

            print("\n🔹 **Toimittajat tietokannassa:** 🔹")
            print("=" * 60)
            for toimittaja in toimittajat:
                print(f"🔹 ID: {toimittaja.id}")
                print(f"🔹 Nimi: {toimittaja.nimi}")
                print("=" * 60)

    except Exception as e:
        print(f"❌ Virhe tietokantakyselyssä: {str(e)}")

# 🔹 Aja funktio
if __name__ == "__main__":
    #tulosta_toimittajat()
    print("🔹 Tulostetaan `toimittajat`-taulun sisältö...")

#from db_config import SessionLocal, Toimittajat

#==================================== lisaa_toimittaja(nimi)

def lisaa_toimittaja(nimi):
    """Lisää uuden toimittajan tietokantaan."""
    try:
        with SessionLocal() as db:
            uusi_toimittaja = Toimittajat(nimi=nimi)
            db.add(uusi_toimittaja)
            db.commit()
            db.refresh(uusi_toimittaja)

            print(f"✅ Lisätty toimittaja: {uusi_toimittaja.nimi} (ID: {uusi_toimittaja.id})")

    except Exception as e:
        print(f"❌ Virhe lisättäessä toimittajaa: {str(e)}")

# 🔹 Käyttö
if __name__ == "__main__":
    #toimittaja_nimi = input("Syötä lisättävän toimittajan nimi: ")
    #lisaa_toimittaja(toimittaja_nimi)
    print("🔹 Lisätään toimittaja...")
