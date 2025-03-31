from config_data import UPLOAD_FOLDER_DATA
from utils.file_handler import muuta_pdf_tekstiksi, kirjoita_txt_tiedosto, lue_txt_tiedosto
from utils.tietosissallon_kasittely import tunnista_toimittaja
#from utils.file_handler import generate_uuid
import uuid
#from utils.file_handler import kirjoita_txt_tiedosto
from luokat_ikkuna_ulkoovi_valiovi import UlkoOvi
from db_luokat import SessionLocal, Toimitussisalto, Kayttaja, Toimittaja, Ikkuna
from sqlalchemy import text  # Lisää tämä rivi
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
#from db_config import Base, engine, SessionLocal
from datetime import datetime
import hashlib
#from sqlalchemy import create_engine
import json
import io
import logging

logging.basicConfig(level=logging.INFO)



def anna_polku(unique_id: str):
    """Ottaa yksilöllisen ID:n ja palauttaa sen mukaisen tiedostopolkuolion"""
    logging.info("Tehdään tiedostopolku...")
    pdf_filename = f"{unique_id}.pdf"
    logging.info(f"...tiedostopolku: {str(UPLOAD_FOLDER_DATA / pdf_filename)}")
    return UPLOAD_FOLDER_DATA / pdf_filename


#==================================== kirjoita_ensimmainen_toimitussisalto()
def kirjoita_ensimmainen_toimitussisalto(file) -> str:
    logging.info("Kirjoitetaan ensimmäistä toimitussisältöä")

    # Muodostetaan yksilöllinen ID
    unique_id = str(uuid.uuid4())

    # Lue tiedosto muistiin ennen tallennusta
    file_data = file.read()  # Lue sisältö talteen
    
    # Varmista, että kansio on olemassa
    if not UPLOAD_FOLDER_DATA.exists():
        logging.warning("❌ Kansio puuttuu, luodaan...")
        UPLOAD_FOLDER_DATA.mkdir(parents=True, exist_ok=True)

    #pdf_filename = luo_uuid_ja_anna_polku()
    pdf_filepath = anna_polku(unique_id)
    
    # Tallenna tiedosto palvelimelle
    with open(pdf_filepath, "wb") as f:
        f.write(file_data)  # Kirjoitetaan alkuperäinen tiedosto levylle
    
    # Muunna PDF tekstiksi ilman tallennusta
    teksti = muuta_pdf_tekstiksi(io.BytesIO(file_data))  # Luo muistissa oleva tiedosto-objekti
    
    # Tunnista toimittaja
    toimittaja = tunnista_toimittaja(teksti)
    print("toimittaja", toimittaja)
    # Tallennetaan tekstidata tiedostoksi
    txt_filename = f"{unique_id}.txt"
    txt_filepath = UPLOAD_FOLDER_DATA / txt_filename
    kirjoita_txt_tiedosto(teksti, txt_filepath)
    print(f"🔹 Tallennetaan tekstidata tiedostoksi 97")

    db = SessionLocal()
    try:
        uusi_toimitussisalto = Toimitussisalto(
            kayttaja_id=1,
            toimittaja_id=hae_toimittajan_id_nimella(toimittaja),
            uuid=unique_id,
            pdf_url=str(pdf_filepath),
            txt_sisalto=str(txt_filepath),
            toimittaja=toimittaja,
            aktiivinen=True,
        )
        db.add(uusi_toimitussisalto)
        db.flush()  # 🌟 Varmistaa, että ID generoituu ennen commitointia
        db.commit()
        db.refresh(uusi_toimitussisalto)  # 🌟 Päivittää objektin tietokannasta
        print("✅ Uusi toimitussisalto lisätty ID:", uusi_toimitussisalto.id)
    except Exception as e:
        db.rollback()  # 🌟 Jos virhe, kumoa kaikki muutokset
        print(f"❌ Virhe lisättäessä tietoa: {e}")
    finally:
        db.close()  # Sulje istunto aina
    #return hae_toimittaja_uuidlla(unique_id)
    print(f"🔹 Uusi toimitussisalto lisätty ID: {unique_id}")
    return unique_id



#==================================== kirjoita_toinen_toimitussisalto()
def kirjoita_toinen_toimitussisalto(file) -> str:
    print("toinen_toimitussisalto")
    #file = request.files["toinen_toimitussisalto"]            
    # 🔹 Luo UUID-tunniste ja tallenna PDF palvelimelle

    # Muodostetaan yksilöllinen ID
    unique_id = str(uuid.uuid4())    
    pdf_filepath = anna_polku(unique_id)
    
    # 🔹 Lue tiedosto muistiin ennen tallennusta
    file_data = file.read()  # Lue sisältö talteen
    
    # 🔹 Varmista, että kansio on olemassa
    if not UPLOAD_FOLDER_DATA.exists():
        print("❌ Kansio puuttuu, luodaan...")
        UPLOAD_FOLDER_DATA.mkdir(parents=True, exist_ok=True)

    #pdf_filepath = UPLOAD_FOLDER_DATA / pdf_filename  # tämä on Path-objekti
    
    # 🔹 Tallenna tiedosto palvelimelle
    with open(pdf_filepath, "wb") as f:
        f.write(file_data)  # Kirjoitetaan alkuperäinen tiedosto levylle
    
    # Muunna PDF tekstiksi ilman tallennusta
    teksti = muuta_pdf_tekstiksi(io.BytesIO(file_data))  # Luo muistissa oleva tiedosto-objekti
    
    # 🔹 Tunnista toimittaja
    toimittaja = tunnista_toimittaja(teksti)
    
    # 🔹 Tallennetaan tekstidata tiedostoksi
    txt_filename = f"{unique_id}.txt"
    txt_filepath = UPLOAD_FOLDER_DATA / txt_filename
    kirjoita_txt_tiedosto(teksti, txt_filepath)
    print(f"🔹 Tallennetaan tekstidata tiedostoksi 97")
    print(f"🔹 Tunnista toimittaja: {toimittaja}")
    db = SessionLocal()
    try:
        uusi_toimitussisalto = Toimitussisalto(
            kayttaja_id=1,
            toimittaja_id=hae_toimittajan_id_nimella(toimittaja),
            uuid=unique_id,
            pdf_url=str(pdf_filepath),
            txt_sisalto=str(txt_filepath),
            toimittaja=toimittaja,
            aktiivinen=True
        )
        db.add(uusi_toimitussisalto)
        db.flush()  # 🌟 Varmistaa, että ID generoituu ennen commitointia
        db.commit()
        db.refresh(uusi_toimitussisalto)  # 🌟 Päivittää objektin tietokannasta
        print("✅ Uusi toimitussisalto lisätty ID:", uusi_toimitussisalto.id)
    except Exception as e:
        db.rollback()  # 🌟 Jos virhe, kumoa kaikki muutokset
        print(f"❌ Virhe lisättäessä tietoa: {e}")
    finally:
        db.close()  # Sulje istunto aina
    #return hae_toimittaja_uuidlla(unique_id)    
    return unique_id



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
            toimitussisallot = db.query(Toimitussisalto).all()

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
        existing_user = db.query(Kayttaja).filter(Kayttaja.email == email).first()
        if existing_user:
            print(f"❌ Käyttäjä '{email}' on jo olemassa.")
            return
        
        # Hashaa salasana (ei suositeltu oikeassa käytössä, käytä bcrypt tai Argon2)
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Luo uusi käyttäjä
        new_user = Kayttaja(
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
            kayttajat = db.query(Kayttaja).all()

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
            kayttaja = db.query(Kayttaja).filter(Kayttaja.id == kayttaja_id).first()

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
            toimittajat = db.query(Toimittaja).all()

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
            uusi_toimittaja = Toimittaja(nimi=nimi)
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


#==================================== lisaa_ikkunat_kantaan(ikkunat_json, toimitussisalto_id)

def lisaa_ikkunat_kantaan(ikkunat_json_str, toimitussisalto_id: int):
    """
    Lisää ikkunatiedot tietokantaan JSON-merkkijonosta.

    Args:
        ikkunat_json_str: JSON-merkkijono ikkunoista
        toimitussisalto_id: Toimitussisällön ID, johon ikkunat liittyvät
    """
    try:
        # Muunna JSON-merkkijono Python-listaksi
        ikkunat_lista = json.loads(ikkunat_json_str)
        print(f"✅ JSON muunnettu Python-listaksi: {len(ikkunat_lista)} ikkunaa")
        
        with SessionLocal() as db:
            lisatty = 0
            for ikkuna_data in ikkunat_lista:
                # Parsitaan leveys ja korkeus koko-kentästä
                leveys_dm, korkeus_dm = map(int, ikkuna_data["koko"].split('x'))
                
                # Luodaan ikkuna jokaiselle kappaleelle
                for _ in range(ikkuna_data["kpl"]):
                    # Muunnetaan mitat millimetreiksi
                    leveys_mm = leveys_dm * 100
                    korkeus_mm = korkeus_dm * 100
                    
                    # Luodaan uusi ikkuna-tietue
                    uusi_ikkuna = Ikkuna(
                        leveys=leveys_mm,
                        korkeus=korkeus_mm,
                        turvalasi=ikkuna_data["turvalasi"],
                        valikarmi=ikkuna_data["välikarmi"],
                        salekaihtimet=ikkuna_data["sälekaihtimet"],
                        toimitussisalto_id=toimitussisalto_id
                    )
                    db.add(uusi_ikkuna)
                    lisatty += 1
            
            db.commit()
            print(f"✅ Lisätty {lisatty} ikkunaa kantaan")
            
    except json.JSONDecodeError as e:
        print(f"❌ Virheellinen JSON-muoto: {str(e)}")
        print(f"JSON (ensimmäiset 100 merkkiä): {ikkunat_json_str[:100]}...")
    except KeyError as e:
        print(f"❌ Puuttuva kenttä JSON:issa: {str(e)}")
        db.rollback()
    except Exception as e:
        print(f"❌ Virhe ikkunoiden lisäämisessä: {str(e)}")
        print(f"Ensimmäiset 100 merkkiä: {ikkunat_json_str[:100]}...")
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

from sqlalchemy.orm import joinedload
from datetime import datetime
from sqlalchemy import func


from sqlalchemy import func
from datetime import datetime

def hae_paivan_ikkunat(paivamaara: str):
    """
    Hakee tietyn päivän aikana luodut ikkunat tietokannasta.

    Args:
        paivamaara: Päivämäärä suomalaisessa muodossa (pp.mm.vvvv)
    """
    try:
        # Muunna suomalainen päivämäärä datetime-objektiksi
        paiva = datetime.strptime(paivamaara, "%d.%m.%Y")
        
        with SessionLocal() as db:
            # Tee kysely SQLAlchemyn avulla
            tulokset = db.query(Ikkuna, Toimitussisalto).join(Toimitussisalto).filter(
                func.date(Ikkuna.created_at) == paiva.date()
            ).order_by(Ikkuna.created_at, Ikkuna.toimitussisalto_id).all()

            if not tulokset:
                print(f"❌ Ei ikkunoita päivämäärällä {paivamaara}")
                return []

            print(f"\n🔹 Löydetty {len(tulokset)} ikkunaa päivämäärällä {paivamaara}:")
            print("=" * 80)

            ikkunat = []
            for ikkuna, toimitus in tulokset:
                ikkuna_tiedot = {
                    "id": ikkuna.id,
                    "leveys": ikkuna.leveys,
                    "korkeus": ikkuna.korkeus,
                    "turvalasi": ikkuna.turvalasi,
                    "valikarmi": ikkuna.valikarmi,
                    "salekaihtimet": ikkuna.salekaihtimet,
                    "luotu": ikkuna.created_at,
                    "toimitussisalto_id": ikkuna.toimitussisalto_id,
                    "toimittaja": toimitus.toimittaja,
                    "toimitussisalto_uuid": toimitus.uuid
                }
                ikkunat.append(ikkuna_tiedot)

                # Tulostetaan ikkunan tiedot
                print(f"Ikkuna ID: {ikkuna_tiedot['id']}")
                print(f"Leveys: {ikkuna_tiedot['leveys']} mm")
                print(f"Korkeus: {ikkuna_tiedot['korkeus']} mm")
                print(f"Toimittaja: {ikkuna_tiedot['toimittaja']}")
                print(f"Turvalasi: {'Kyllä' if ikkuna_tiedot['turvalasi'] else 'Ei'}")
                print(f"Välikarmi: {'Kyllä' if ikkuna_tiedot['valikarmi'] else 'Ei'}")
                print(f"Sälekaihtimet: {'Kyllä' if ikkuna_tiedot['salekaihtimet'] else 'Ei'}")
                print(f"Luotu: {ikkuna_tiedot['luotu'].strftime('%d.%m.%Y %H:%M:%S')}")
                print("-" * 80)

            return ikkunat

    except ValueError:
        print(f"❌ Virheellinen päivämäärän muoto. Käytä muotoa pp.mm.vvvv")
        return []
    except Exception as e:
        print(f"❌ Virhe ikkunoiden haussa: {str(e)}")
        return []




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

#==================================== paivita_ulko_ovet_taulu()
def paivita_ulko_ovet_taulu():
    """
    Päivittää ulko_ovet-taulun rakenteen vastaamaan UlkoOvet-luokan määrittelyä.
    """
    try:
        with SessionLocal() as db:
            print("🔹 Päivitetään ulko_ovet-taulun rakenne...")
            
            # Lisää puuttuva lukko-sarake ja aseta NOT NULL rajoitteet
            muutokset = [
                # Lisää puuttuva lukko-sarake
                "ALTER TABLE ulko_ovet ADD COLUMN IF NOT EXISTS lukko VARCHAR(255)",
                
                # Aseta väliaikainen arvo lukko-sarakkeeseen
                "UPDATE ulko_ovet SET lukko = 'ei määritelty' WHERE lukko IS NULL",
                
                # Aseta NOT NULL rajoitteet
                "ALTER TABLE ulko_ovet ALTER COLUMN malli SET NOT NULL",
                "ALTER TABLE ulko_ovet ALTER COLUMN lukko SET NOT NULL",
                
                # Päivitä CASCADE delete
                """
                ALTER TABLE ulko_ovet 
                DROP CONSTRAINT IF EXISTS ulko_ovet_toimitussisalto_id_fkey,
                ADD CONSTRAINT ulko_ovet_toimitussisalto_id_fkey 
                    FOREIGN KEY (toimitussisalto_id) 
                    REFERENCES toimitussisallot(id) 
                    ON DELETE CASCADE
                """
            ]

            for muutos in muutokset:
                try:
                    db.execute(text(muutos))
                    print(f"✅ Suoritettu: {muutos}")
                except Exception as e:
                    print(f"❌ Virhe muutoksessa: {muutos}")
                    print(f"Virhe: {str(e)}")

            db.commit()
            print("✅ Ulko_ovet-taulu päivitetty onnistuneesti!")

    except Exception as e:
        print(f"❌ Virhe taulun päivityksessä: {str(e)}")
        db.rollback()


#==================================== lisaa_ulko_ovet_kantaan()

def lisaa_ulko_ovet_kantaan(ovet: list[UlkoOvi], toimitussisalto_id: int):
    """
    Lisää UlkoOvi-oliot tietokantaan.
    
    Args:
        ovet: Lista UlkoOvi-olioita
        toimitussisalto_id: Toimitussisällön ID
    """
    try:
        with SessionLocal() as db:
            lisatty = 0
            for ovi in ovet:
                uusi_ovi = UlkoOvet(
                    malli=ovi.malli,
                    paloluokitus_EI_15=ovi.paloluokitus_EI_15,
                    lukko=ovi.lukko,
                    maara=ovi.maara,
                    toimitussisalto_id=toimitussisalto_id
                )
                db.add(uusi_ovi)
                lisatty += 1
            
            db.commit()
            print(f"✅ Lisätty {lisatty} ovea tietokantaan")
            
    except Exception as e:
        print(f"❌ Virhe ovien lisäämisessä: {str(e)}")
        db.rollback()


#==================================== hae_toimitussiallon ikkunat(toimittaja_id, toimitussisalto_id)

def hae_toimitussisallon_ikkunat(toimittaja_id: int, toimitussisalto_id: int):
    """
    Hakee ja tulostaa toimittajan tietyn toimitussisällön ikkunat käyttäen SQLAlchemy ORM:ää.

    Args:
        toimittaja_id (int): Toimittajan ID
        toimitussisalto_id (int): Toimitussisällön ID
    """
    try:
        with SessionLocal() as db:
            # Haetaan ikkunat käyttäen SQLAlchemy ORM:ää
            ikkunat = (
                db.query(Ikkuna)
                .join(Toimitussisalto)
                .filter(
                    Toimitussisalto.toimittaja_id == toimittaja_id,
                    Toimitussisalto.id == toimitussisalto_id
                )
                .order_by(Ikkuna.id)
                .all()
            )
            
            if not ikkunat:
                print(f"❌ Ei löytynyt ikkunoita toimittajalle ID:{toimittaja_id} ja toimitussisällölle ID:{toimitussisalto_id}")
                return
            
            print(f"\n🔹 Löydetty {len(ikkunat)} ikkunaa:")
            print("=" * 80)
            
            for ikkuna in ikkunat:
                print(f"Ikkuna ID: {ikkuna.id}")
                print(f"Koko: {ikkuna.leveys}x{ikkuna.korkeus} mm")
                print(f"Turvalasi: {'Kyllä' if ikkuna.turvalasi else 'Ei'}")
                print(f"Välikarmi: {'Kyllä' if ikkuna.valikarmi else 'Ei'}")
                print(f"Sälekaihtimet: {'Kyllä' if ikkuna.salekaihtimet else 'Ei'}")
                print(f"Luotu: {ikkuna.created_at.strftime('%d.%m.%Y %H:%M:%S') if ikkuna.created_at else 'Ei tiedossa'}")
                print(f"Toimittaja: {ikkuna.toimitussisalto.toimittaja}")
                print("-" * 80)

    except Exception as e:
        print(f"❌ Virhe ikkunoiden haussa: {str(e)}")

def hae_toimittajan_sisallot(toimittaja_id: int):
    """
    Hakee ja tulostaa kaikki toimittajan toimitussisällöt.

    Args:
        toimittaja_id (int): Toimittajan ID

    Returns:
        list[Toimitussisalto]: Lista toimitussisältö-olioista
    """
    try:
        with SessionLocal() as db:
            # Haetaan toimittajan kaikki toimitussisällöt
            toimitussisallot = (
                db.query(Toimitussisalto)
                .filter(Toimitussisalto.toimittaja_id == toimittaja_id)
                .order_by(Toimitussisalto.created_at)
                .all()
            )

            if not toimitussisallot:
                print(f"❌ Ei löytynyt toimitussisältöjä toimittajalle ID:{toimittaja_id}")
                return []

            print(f"\n🔹 Löydetty {len(toimitussisallot)} toimitussisältöä:")
            print("=" * 80)

            for sisalto in toimitussisallot:
                print(f"Toimitussisältö ID: {sisalto.id}")
                print(f"UUID: {sisalto.uuid}")
                print(f"Toimittaja: {sisalto.toimittaja}")
                print(f"Luotu: {sisalto.created_at.strftime('%d.%m.%Y %H:%M:%S')}")
                print(f"Aktiivinen: {'Kyllä' if sisalto.aktiivinen else 'Ei'}")
                print(f"Ikkunoita: {len(sisalto.ikkunat)}")
                print("-" * 80)

            return toimitussisallot

    except Exception as e:
        print(f"❌ Virhe toimitussisältöjen haussa: {str(e)}")
        return []

#==================================== hae_toimitussisalto(toimitussisalto_id)


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
            print(f"Tekstisisältö: {toimitussisalto.txt_sisalto}")
            print(f"Toimittaja: {toimitussisalto.toimittaja}")
            
            # Tulostetaan myös liittyvät ikkunat
            print("\nLiittyvät ikkunat:")
            for ikkuna in toimitussisalto.ikkunat:
                print(f"- Ikkuna ID: {ikkuna.id}")
                
    except Exception as e:
        print(f"❌ Virhe toimitussisällön haussa: {str(e)}")


#==================================== hae_toimittaja_nimella(toimittaja)

def hae_toimittajan_id_nimella(toimittaja: str) -> int | None:
    """
    Hakee toimittajan ID:n nimen perusteella.
    
    Args:
        toimittaja: Toimittajan nimi
        
    Returns:
        int | None: Toimittajan ID tai None jos ei löydy
    """
    try:
        with SessionLocal() as db:
            kysely = text("""
                SELECT id
                FROM toimittajat
                WHERE nimi = :toimittaja
                LIMIT 1;
            """)
            tulos = db.execute(kysely, {"toimittaja": toimittaja}).fetchone()

            if not tulos:
                print(f"❌ Ei löytynyt toimittajaa nimellä {toimittaja}")
                return None

            toimittaja_id = tulos[0]
            print(f"✅ Toimittajan {toimittaja} ID on: {toimittaja_id}")
            return toimittaja_id

    except Exception as e:
        print(f"❌ Virhe kyselyssä: {str(e)}")
        return None

#==================================== hae_paivan_toimitussisallot(paivamaara)

def hae_paivan_toimitussisallot(paivamaara: str) -> list:
    """
    Hakee tietyn päivän aikana luodut toimitussisällöt tietokannasta.

    Args:
        paivamaara: Päivämäärä suomalaisessa muodossa (pp.mm.vvvv)
        
    Returns:
        list: Lista toimitussisällöistä tai tyhjä lista jos ei löydy
    """
    try:
        # Muunna suomalainen päivämäärä datetime-objektiksi
        paiva = datetime.strptime(paivamaara, "%d.%m.%Y")
        
        with SessionLocal() as db:
            # Hae päivän toimitussisällöt
            toimitussisallot = (
                db.query(Toimitussisalto)
                .filter(func.date(Toimitussisalto.created_at) == paiva.date())
                .order_by(Toimitussisalto.created_at)
                .all()
            )

            if not toimitussisallot:
                print(f"❌ Ei toimitussisältöjä päivämäärällä {paivamaara}")
                return []

            print(f"\n🔹 Löydetty {len(toimitussisallot)} toimitussisältöä päivämäärällä {paivamaara}:")
            print("=" * 80)

            for sisalto in toimitussisallot:
                print(f"Toimitussisältö ID: {sisalto.id}")
                print(f"Toimittaja ID: {sisalto.toimittaja_id}")
                print(f"UUID: {sisalto.uuid}")
                print(f"Toimittaja: {sisalto.toimittaja}")
                print(f"Luotu: {sisalto.created_at.strftime('%d.%m.%Y %H:%M:%S')}")
                print(f"PDF URL: {sisalto.pdf_url}")
                print(f"Aktiivinen: {'Kyllä' if sisalto.aktiivinen else 'Ei'}")
                print("-" * 80)

            return toimitussisallot

    except ValueError:
        print(f"❌ Virheellinen päivämäärän muoto. Käytä muotoa pp.mm.vvvv")
        return []
    except Exception as e:
        print(f"❌ Virhe toimitussisältöjen haussa: {str(e)}")
        return []
