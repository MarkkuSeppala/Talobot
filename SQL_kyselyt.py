from sqlalchemy import text, create_engine
#from db_config import SessionLocal, Toimittajat
from db_config import SessionLocal, Toimitussisallot, Kayttajat, Toimittajat, Ikkunat

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

# if __name__ == "__main__":
#     get_all_tables()
#    print("🔹 Tulostetaan kaikki tietokannan taulut...")




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

# if __name__ == "__main__":
#     get_all_table_structures()
#     print("🔹 Päivitetään `toimitussisallot`-taulua...")





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

# if __name__ == "__main__":
#     update_table()
#     print("🔹 Päivitetään `toimitussisallot`-taulua...")


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
    #tulosta_toimitussisallot()
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

from pathlib import Path

#==================================== hae_toimittaja_uuidlla(uuid)

def hae_toimittaja_uuidlla(uuid: str):
    """Hakee toimitussisällön toimittajan annetulla UUID:lla."""
    try:
        with SessionLocal() as db:
            kysely = text("""
                SELECT toimittaja
                FROM toimitussisallot
                WHERE uuid = :uuid
                LIMIT 1;
            """)
            tulos = db.execute(kysely, {"uuid": uuid}).fetchone()

            if not tulos:
                print(f"❌ Ei löytynyt toimitussisältöä UUID:lla {uuid}")
                return None

            toimittaja = tulos[0]
            print(f"✅ Toimittaja UUID:lla {uuid} on: {toimittaja}")
            return toimittaja

    except Exception as e:
        print(f"❌ Virhe kyselyssä: {str(e)}")
        return None

#==================================== hae_txt_sisalto_uuidlla(uuid)
def hae_toimitussisalto_txt_polku_uuidlla(uuid: str) -> str | None:
    """
    Hakee txt_sisalto-sarakkeen sisällön toimitussisallot-taulusta annetulla UUID:lla.

    Args:
        uuid (str): UUID, jolla etsitään tietue

    Returns:
        str | None: Tekstitieto tietueesta tai None jos ei löydy
    """
    try:
        with SessionLocal() as db:
            kysely = text("""
                SELECT txt_sisalto
                FROM toimitussisallot
                WHERE uuid = :uuid
                LIMIT 1;
            """)
            tulos = db.execute(kysely, {"uuid": uuid}).fetchone()

            if not tulos:
                print(f"❌ Ei löytynyt toimitussisältöä UUID:lla {uuid}")
                return None

            txt_sisalto = tulos[0]
            print(f"✅ Tekstisisältö haettu UUID:lla {uuid}")
            return txt_sisalto

    except Exception as e:
        print(f"❌ Virhe kyselyssä: {str(e)}")
        return None


#==================================== lisaa_ikkunat_kantaan(ikkunat_lista, toimitussisalto_id)

def lisaa_ikkunat_kantaan(ikkunat_lista, toimitussisalto_id: int):
    """
    Lisää ikkunatiedot tietokantaan.

    Args:
        ikkunat_lista: Lista Ikkuna-olioita muunna_raaka_ikkunat_yksittaisiksi-funktiolta
        toimitussisalto_id: Toimitussisällön ID, johon ikkunat liittyvät
    """
    try:
        with SessionLocal() as db:
            for ikkuna in ikkunat_lista:
                # Parsitaan leveys ja korkeus mm_koko-kentästä
                leveys, korkeus = map(int, ikkuna.mm_koko.split('x'))
                
                # Luodaan uusi ikkuna-tietue
                uusi_ikkuna = Ikkunat(
                    leveys=leveys,
                    korkeus=korkeus,
                    turvalasi=ikkuna.turvalasi,
                    valikarmi=ikkuna.välikarmi,
                    salekaihtimet=ikkuna.sälekaihtimet,
                    toimitussisalto_id=toimitussisalto_id
                )
                db.add(uusi_ikkuna)
            
            db.commit()
            print(f"✅ Lisätty {len(ikkunat_lista)} ikkunaa kantaan")
            
    except Exception as e:
        print(f"❌ Virhe ikkunoiden lisäämisessä: {str(e)}")
        db.rollback()

#==================================== hae_kaikki_ikkunat()

def hae_kaikki_ikkunat():
    """
    Hakee kaikki ikkunat tietokannasta.
    Palauttaa listan ikkunoista ja niihin liittyvistä toimitussisällöistä.
    """
    try:
        with SessionLocal() as db:
            kysely = text("""
                SELECT 
                    i.id,
                    i.leveys,
                    i.korkeus,
                    i.turvalasi,
                    i.valikarmi,
                    i.salekaihtimet,
                    i.created_at,
                    i.toimitussisalto_id,
                    t.toimittaja,
                    t.uuid
                FROM ikkunat i
                LEFT JOIN toimitussisallot t ON i.toimitussisalto_id = t.id
                ORDER BY i.toimitussisalto_id, i.leveys;
            """)
            
            tulokset = db.execute(kysely).fetchall()
            
            if not tulokset:
                print("❌ Ei ikkunoita tietokannassa")
                return []
            
            print(f"\n🔹 Löydetty {len(tulokset)} ikkunaa:")
            print("=" * 80)
            
            ikkunat = []
            for tulos in tulokset:
                ikkuna = {
                    "id": tulos[0],
                    "leveys": tulos[1],
                    "korkeus": tulos[2],
                    "turvalasi": tulos[3],
                    "valikarmi": tulos[4],
                    "salekaihtimet": tulos[5],
                    "luotu": tulos[6],
                    "toimitussisalto_id": tulos[7],
                    "toimittaja": tulos[8],
                    "toimitussisalto_uuid": tulos[9]
                }
                ikkunat.append(ikkuna)
                
                # Tulostetaan ikkunan tiedot
                print(f"Ikkuna ID: {ikkuna['id']}")
                print(f"Koko: {ikkuna['leveys']}x{ikkuna['korkeus']} mm")
                print(f"Toimittaja: {ikkuna['toimittaja']}")
                print(f"Turvalasi: {'Kyllä' if ikkuna['turvalasi'] else 'Ei'}")
                print(f"Välikarmi: {'Kyllä' if ikkuna['valikarmi'] else 'Ei'}")
                print(f"Sälekaihtimet: {'Kyllä' if ikkuna['salekaihtimet'] else 'Ei'}")
                print(f"Luotu: {ikkuna['luotu'].strftime('%d.%m.%Y %H:%M:%S') if ikkuna['luotu'] else 'Ei tiedossa'}")
                print("-" * 80)
            
            return ikkunat

    except Exception as e:
        print(f"❌ Virhe ikkunoiden haussa: {str(e)}")
        return []

# Testikäyttö
# if __name__ == "__main__":
#     ikkunat = hae_kaikki_ikkunat()
#     print(f"Yhteensä {len(ikkunat)} ikkunaa haettu")


#==================================== hae_paivan_ikkunat(paivamaara)

def hae_paivan_ikkunat(paivamaara: str):
    """
    Hakee tietyn päivän aikana luodut ikkunat tietokannasta.
    
    Args:
        paivamaara: Päivämäärä suomalaisessa muodossa (pp.mm.vvvv)
    """
    try:
        # Muunnetaan suomalainen päivämäärä datetime-objektiksi
        paiva = datetime.strptime(paivamaara, "%d.%m.%Y")
        
        with SessionLocal() as db:
            kysely = text("""
                SELECT 
                    i.id,
                    i.leveys,
                    i.korkeus,
                    i.turvalasi,
                    i.valikarmi,
                    i.salekaihtimet,
                    i.created_at,
                    i.toimitussisalto_id,
                    t.toimittaja,
                    t.uuid
                FROM ikkunat i
                LEFT JOIN toimitussisallot t ON i.toimitussisalto_id = t.id
                WHERE DATE(i.created_at) = DATE(:paiva)
                ORDER BY i.created_at, i.toimitussisalto_id;
            """)
            
            tulokset = db.execute(kysely, {"paiva": paiva}).fetchall()
            
            if not tulokset:
                print(f"❌ Ei ikkunoita päivämäärällä {paivamaara}")
                return []
            
            print(f"\n🔹 Löydetty {len(tulokset)} ikkunaa päivämäärällä {paivamaara}:")
            print("=" * 80)
            
            ikkunat = []
            for tulos in tulokset:
                ikkuna = {
                    "id": tulos[0],
                    "leveys": tulos[1],
                    "korkeus": tulos[2],
                    "turvalasi": tulos[3],
                    "valikarmi": tulos[4],
                    "salekaihtimet": tulos[5],
                    "luotu": tulos[6],
                    "toimitussisalto_id": tulos[7],
                    "toimittaja": tulos[8],
                    "toimitussisalto_uuid": tulos[9]
                }
                ikkunat.append(ikkuna)
                
                # Tulostetaan ikkunan tiedot
                print(f"Ikkuna ID: {ikkuna['id']}")
                print(f"Koko: {ikkuna['leveys']}x{ikkuna['korkeus']} mm")
                print(f"Toimittaja: {ikkuna['toimittaja']}")
                print(f"Turvalasi: {'Kyllä' if ikkuna['turvalasi'] else 'Ei'}")
                print(f"Välikarmi: {'Kyllä' if ikkuna['valikarmi'] else 'Ei'}")
                print(f"Sälekaihtimet: {'Kyllä' if ikkuna['salekaihtimet'] else 'Ei'}")
                print(f"Luotu: {ikkuna['luotu'].strftime('%d.%m.%Y %H:%M:%S')}")
                print("-" * 80)
            
            return ikkunat

    except ValueError as e:
        print(f"❌ Virheellinen päivämäärän muoto. Käytä muotoa pp.mm.vvvv")
        return []
    except Exception as e:
        print(f"❌ Virhe ikkunoiden haussa: {str(e)}")
        return []

# if __name__ == "__main__":
#     ikkunat = hae_paivan_ikkunat("28.03.2025")
#     print(f"Yhteensä {len(ikkunat)} ikkunaa haettu")



#==================================== hae_toimitussisalto_id_uuidlla(uuid)

def hae_toimitussisalto_id_uuidlla(uuid: str) -> int | None:
    """
    Hakee toimitussisällön ID:n annetulla UUID:lla.

    Args:
        uuid (str): UUID, jolla etsitään tietue

    Returns:
        int | None: Toimitussisällön ID tai None jos ei löydy
    """
    try:
        with SessionLocal() as db:
            kysely = text("""
                SELECT id
                FROM toimitussisallot
                WHERE uuid = :uuid
                LIMIT 1;
            """)
            tulos = db.execute(kysely, {"uuid": uuid}).fetchone()

            if not tulos:
                print(f"❌ Ei löytynyt toimitussisältöä UUID:lla {uuid}")
                return None

            toimitussisalto_id = tulos[0]
            print(f"✅ Toimitussisällön ID haettu: {toimitussisalto_id}")
            return toimitussisalto_id

    except Exception as e:
        print(f"❌ Virhe kyselyssä: {str(e)}")
        return None


#==================================== update_toimitussisallot_table()

def update_toimitussisallot_table():
    """Päivittää `toimitussisallot`-taulun lisäämällä puuttuvat sarakkeet ja muuttamalla asetukset."""
    try:
        with SessionLocal() as db:
            print("🔹 Päivitetään `toimitussisallot`-taulua...")

            # 🔹 Lisätään puuttuvat sarakkeet (jos eivät ole olemassa)
            alter_statements = [
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS uuid VARCHAR(36) UNIQUE NOT NULL",
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS pdf_url TEXT NOT NULL",
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS txt_sisalto TEXT NOT NULL",
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS toimittaja VARCHAR(100) NOT NULL"
            ]

            # 🔹 Muutetaan sarakkeiden `NULL`-asetuksia
            alter_nullable_statements = [
                "ALTER TABLE toimitussisallot ALTER COLUMN kayttaja_id SET NOT NULL",
                "ALTER TABLE toimitussisallot ALTER COLUMN created_at SET NOT NULL",
                "ALTER TABLE toimitussisallot ALTER COLUMN aktiivinen SET NOT NULL"
            ]

            # 🔹 Suoritetaan ALTER TABLE -komennot
            for stmt in alter_statements + alter_nullable_statements:
                try:
                    db.execute(text(stmt))
                except Exception as e:
                    print(f"❌ Virhe suoritettaessa: {stmt}")
                    print(f"   ➝ {e}")

            db.commit()
            print("✅ `toimitussisallot`-taulu päivitetty onnistuneesti!")

    except Exception as e:
        print(f"❌ Virhe tietokantapäivityksessä: {e}")

# if __name__ == "__main__":
#    update_toimitussisallot_table()