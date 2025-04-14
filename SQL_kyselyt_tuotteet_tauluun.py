from config_data import UPLOAD_FOLDER_DATA
from sqlalchemy import create_engine, text, inspect, Table, Column, Integer, Boolean, String, DECIMAL, ForeignKey, text
from sqlalchemy.orm import Session
from db_luokat import Base, Tuote, engine, SessionLocal, Toimitussisalto, Kayttaja, Toimittaja, Ikkuna, Ulko_ovi, Valiovi

from decimal import Decimal
from tabulate import tabulate  # Asentaa: pip install tabulate
import os
import pandas as pd
from io import StringIO 
import csv

from datetime import datetime, timedelta
from logger_config import configure_logging
import logging
import json

# Loggerin alustus
configure_logging()
logger = logging.getLogger(__name__)


# Hae tietokantayhteys
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL ei ole asetettu! Tarkista .env-tiedosto.")

# Luo SQLAlchemy-moottori
engine = create_engine(DATABASE_URL)





#==================================== tuo_tuotteet_sheetista(csv_url)
def siisti_arvo(arvo):
    if pd.isna(arvo):
        return None
    if isinstance(arvo, str) and arvo.strip() in ('', '""'):
        return None
    return str(arvo)

def tuo_tuotteet_sheetista(csv_url):
    """
    Tuo tuotteet Google Sheets -taulukosta tietokantaan.
    """
    try:
        print(f"Luetaan dataa osoitteesta: {csv_url}")
        
        # Lue CSV pandas DataFrameen
        df = pd.read_csv(csv_url)
        
        # Poista tyhjät rivit
        df = df.dropna(how='all')
        
        print(f"Luettiin {len(df)} riviä dataa")
        
        current_time = datetime.utcnow()
        future_time = current_time + timedelta(days=365)
        
        session = SessionLocal()
        
        try:
            lisatyt = 0
            virheet = 0
            
            for index, row in df.iterrows():
                try:
                    # Käsittele hinta
                    hinta = Decimal(str(row['hinta']).replace(',', '.')) if pd.notna(row['hinta']) else None

                    # Luo uusi Tuote-objekti, käytä siisti_arvo-funktiota
                    tuote = Tuote(
                        version_number=row.get('version_number', 1),
                        valid_from=pd.to_datetime(row['valid_from']),
                        valid_to=pd.to_datetime(row['valid_to']),
                        prompt_1=bool(row['prompt_1']),
                        prompt_2=bool(row['prompt_2']),
                        prompt_3=bool(row['prompt_3']),
                        tuote=str(row['tuote']),
                        yksikko=siisti_arvo(row['yksikko']),
                        hinta=hinta,
                        absoluuttinen_hinta=bool(row['absoluuttinen_hinta']),
                        tarkenne_yleinen=siisti_arvo(row['tarkenne_yleinen']),
                        tarkenne_sievitalo=siisti_arvo(row['tarkenne_sievitalo']),
                        tarkenne_kastelli=siisti_arvo(row['tarkenne_kastelli']),
                        tarkenne_designtalo=siisti_arvo(row['tarkenne_designtalo']),
                        tarkenne_jopera=siisti_arvo(row['tarkenne_jopera']),
                        tarkenne_kannustalo=siisti_arvo(row['tarkenne_kannustalo']),
                        tarkenne_kylatimpurit=siisti_arvo(row['tarkenne_kylatimpurit']),
                        tarkenne_ainoakoti=siisti_arvo(row['tarkenne_ainoakoti']),
                        viite_tuote_id=None  # Tämä kenttä jää tyhjäksi
                    )
                    
                    session.add(tuote)
                    lisatyt += 1
                    
                    if lisatyt % 10 == 0:
                        print(f"Lisätty {lisatyt} tuotetta...")
                    
                except Exception as e:
                    print(f"Virhe rivillä {index + 2}: {str(e)}")
                    print(f"Rivin data: {row.to_dict()}")
                    virheet += 1
                    continue
            
            session.commit()
            print(f"\nValmis! Lisätty {lisatyt} tuotetta, virheitä {virheet}")
            
            # Suorita laajennettu tarkistus tallennuksen jälkeen
            tarkista_tuotteiden_tallennus()
            
        except Exception as e:
            print(f"Virhe tietojen tallennuksessa: {str(e)}")
            session.rollback()
            
    except Exception as e:
        print(f"Virhe CSV:n lukemisessa: {str(e)}")




#==================================== tarkista_tuotteiden_tallennus()
def tarkista_tuotteiden_tallennus():
    """
    Tarkistaa tuotteiden tallennuksen tietokantaan ja tulostaa yhteenvedon.
    """
    try:
        with SessionLocal() as db:
            # Hae kaikki tuotteet
            tuotteet = db.query(Tuote).all()
            
            # Laske tilastot
            yhteensa = len(tuotteet)
            tyhja_tarkenne_sievitalo = len([t for t in tuotteet if t.tarkenne_sievitalo is None])
            taytetty_tarkenne_sievitalo = len([t for t in tuotteet if t.tarkenne_sievitalo is not None])
            
            print("\nTuotteiden tallennuksen tarkistus:")
            print(f"Tuotteita yhteensä: {yhteensa}")
            print(f"Tarkenne_sievitalo täytetty: {taytetty_tarkenne_sievitalo}")
            print(f"Tarkenne_sievitalo tyhjä: {tyhja_tarkenne_sievitalo}")
            
            # Näytä esimerkki tuotteista joilla on tarkenne_sievitalo
            if taytetty_tarkenne_sievitalo > 0:
                print("\nEsimerkkejä tuotteista joilla on tarkenne_sievitalo:")
                for tuote in db.query(Tuote).filter(Tuote.tarkenne_sievitalo.isnot(None)).limit(5):
                    print(f"- {tuote.tuote}: {tuote.tarkenne_sievitalo}")
            
            # Näytä esimerkki tuotteista joilla ei ole tarkenne_sievitalo
            if tyhja_tarkenne_sievitalo > 0:
                print("\nEsimerkkejä tuotteista joilla ei ole tarkenne_sievitalo:")
                for tuote in db.query(Tuote).filter(Tuote.tarkenne_sievitalo.is_(None)).limit(5):
                    print(f"- {tuote.tuote}")

    except Exception as e:
        print(f"Virhe tarkistuksessa: {str(e)}")




#==================================== tyhjenna_tuotteet_taulu()
def tyhjenna_tuotteet_taulu():
    """
    Tyhjentää tuotteet-taulun kaikista riveistä.
    Kysyy varmistuksen ennen toimenpidettä.
    """
    try:
        session = SessionLocal()
        
        # Tarkista ensin rivien määrä
        rivien_maara = session.query(Tuote).count()
        
        if rivien_maara == 0:
            print("Tuotteet-taulu on jo tyhjä!")
            return True
            
        # Kysy varmistus
        print(f"\nOlet tyhjentämässä tuotteet-taulun.")
        print(f"Taulussa on {rivien_maara} riviä.")
        print("HUOMIO: Tätä toimintoa ei voi peruuttaa!")
        vastaus = input("Haluatko varmasti tyhjentää taulun? (kirjoita 'TYHJENNÄ' jatkaaksesi): ")
        
        if vastaus != "TYHJENNÄ":
            print("Toiminto peruttu.")
            return False
            
        try:
            # Tyhjennä taulu
            session.query(Tuote).delete()
            session.commit()
            
            print(f"Tuotteet-taulu tyhjennetty onnistuneesti!")
            print(f"Poistettu {rivien_maara} riviä.")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Virhe taulun tyhjennyksessä: {str(e)}")
            return False
            
    except Exception as e:
        print(f"Virhe: {str(e)}")
        return False
        
    finally:
        session.close()



#
def luo_tuotteet_taulu_uudelleen():
    """
    Luo tuotteet-taulun uudelleen Tuote-luokan rakenteen mukaisesti
    """
    try:
        # Tyhjennä SQLAlchemy:n metadata välimuisti
        Base.metadata.clear()
        
        with engine.connect() as connection:
            with connection.begin():
                # Pudota vanha taulu
                connection.execute(text("DROP TABLE IF EXISTS tuotteet CASCADE;"))
                
                # Luo taulu eksplisiittisesti SQL:llä
                connection.execute(text("""
                    CREATE TABLE tuotteet (
                        id SERIAL PRIMARY KEY,
                        version_number INTEGER,
                        valid_from TIMESTAMP,
                        valid_to TIMESTAMP,
                        prompt_1 BOOLEAN NOT NULL,
                        prompt_2 BOOLEAN NOT NULL,
                        prompt_3 BOOLEAN NOT NULL,
                        tuote VARCHAR(100) NOT NULL,
                        yksikko VARCHAR(50),
                        hinta DECIMAL(10,2),
                        absoluuttinen_hinta BOOLEAN NOT NULL DEFAULT FALSE,
                        tarkenne_yleinen VARCHAR(100),
                        tarkenne_sievitalo VARCHAR(100),
                        tarkenne_kastelli VARCHAR(100),
                        tarkenne_designtalo VARCHAR(100),
                        tarkenne_jopera VARCHAR(100),
                        tarkenne_kannustalo VARCHAR(100),
                        tarkenne_kylatimpurit VARCHAR(100),
                        tarkenne_ainoakoti VARCHAR(100),
                        viite_tuote_id INTEGER REFERENCES tuotteet(id)
                    );
                """))
                
        print("Tuotteet-taulu luotu uudelleen onnistuneesti!")
        return True
        
    except Exception as e:
        print(f"Virhe taulun luonnissa: {str(e)}")
        return False



#==================================== poista_tuotteet_taulu()
def poista_tuotteet_taulu():
    """
    Poistaa tuotteet-taulun tietokannasta.
    Kysyy varmistuksen ennen poistoa.
    """
    try:
        print("VAROITUS: Tämä toiminto poistaa tuotteet-taulun ja KAIKKI sen tiedot!")
        vastaus = input("Haluatko varmasti poistaa taulun? (kirjoita 'POISTA' jatkaaksesi): ")
        
        if vastaus != "POISTA":
            print("Toiminto peruttu.")
            return False
        
        with engine.connect() as connection:
            with connection.begin():
                # Poista taulu ja siihen liittyvät viittaukset
                connection.execute(text("DROP TABLE IF EXISTS tuotteet CASCADE;"))
                
        print("Tuotteet-taulu poistettu onnistuneesti!")
        return True
        
    except Exception as e:
        print(f"Virhe taulun poistossa: {str(e)}")
        return False





#==================================== hae_tuotteet_prompt_1_tuote_tarkenne_yleinen()
def hae_tuotteet_prompt_1_tuote_tarkenne_yleinen():
    """
    Hakee tuotteet-taulusta kaikki rivit, joissa prompt_1 on True ja palauttaa tuotteen nimen
    ja tarkenne_yleinen -kentän tiedot.

    Returns:
        list: Lista tupleja, joissa (tuote, tarkenne_yleinen)
    """
    try:
        with SessionLocal() as db:
            # Hae vain tuote ja tarkenne_yleinen -kentät riveistä, joissa prompt_1 on True
            tuotteet = db.query(
                Tuote.tuote,
                Tuote.tarkenne_yleinen
            ).filter(
                Tuote.prompt_1.is_(True)
            ).order_by(
                Tuote.tuote
            ).all()

            # Jos haluat tulostaa tulokset konsoliin
            for tuote in tuotteet:
                print(f"{tuote.tuote:<30}{tuote.tarkenne_yleinen if tuote.tarkenne_yleinen else ' '}")

            return tuotteet

    except Exception as e:
        print(f"Virhe tuotteiden haussa: {str(e)}")
        return None



#==================================== hae_tuotteet_prompt_1_tuote_tarkenne_yleinen_tarkenne_sievitalo()
def hae_tuotteet_prompt_1_tuote_tarkenne_yleinen_tarkenne_sievitalo():
    """
    Hakee tuotteet-taulusta kaikki rivit, joissa prompt_1 on True ja palauttaa tuotteen nimen,
    tarkenne_yleinen ja tarkenne_sievitalo -kenttien tiedot.

    Returns:
        list: Lista tupleja, joissa (tuote, tarkenne_yleinen, tarkenne_sievitalo)
    """
    try:
        with SessionLocal() as db:
            # Hae tuote, tarkenne_yleinen ja tarkenne_sievitalo -kentät riveistä, joissa prompt_1 on True
            tuotteet = db.query(
                Tuote.tuote,
                Tuote.tarkenne_yleinen,
                Tuote.tarkenne_sievitalo
            ).filter(
                Tuote.prompt_1.is_(True)
            ).order_by(
                Tuote.tuote
            ).all()

            # Jos haluat tulostaa tulokset konsoliin
            for tuote in tuotteet:
                print(f"{tuote.tuote:<30}"
                      f"{tuote.tarkenne_yleinen if tuote.tarkenne_yleinen else ' ':<30}"
                      f"{tuote.tarkenne_sievitalo if tuote.tarkenne_sievitalo else ' '}")

            return tuotteet

    except Exception as e:
        print(f"Virhe tuotteiden haussa: {str(e)}")
        return None



#==================================== hae_tuotteet_tarkenne_sievitalo()
def hae_tuotteet_tarkenne_sievitalo():
    """
    Hakee tuotteet-taulusta kaikki uniikit tarkenne_sievitalo -kentän arvot.

    Returns:
        list: Lista tarkenne_sievitalo -kentän arvoista
    """
    try:
        with SessionLocal() as db:
            # Hae vain uniikit tarkenne_sievitalo -kentän arvot
            tarkennetiedot = db.query(
                Tuote.tarkenne_sievitalo
            ).filter(
                Tuote.tarkenne_sievitalo.isnot(None)  # Poistetaan null-arvot
            ).distinct(
            ).order_by(
                Tuote.tarkenne_sievitalo
            ).all()

            # Tulostetaan löydetyt arvot
            print("Löydetyt tarkenne_sievitalo arvot:")
            for tarkenne in tarkennetiedot:
                print(f"- {tarkenne.tarkenne_sievitalo}")

            # Palautetaan lista tarkenne_sievitalo arvoista
            return [t.tarkenne_sievitalo for t in tarkennetiedot]

    except Exception as e:
        print(f"Virhe tarkenne_sievitalo -tietojen haussa: {str(e)}")
        return None



def hae_tuotteet_id_prompt_1_tuote_tarkenne_yleinen_tarkenne_sievitalo():
    """
    Hakee tuotteet-taulusta seuraavat kentät: id, prompt_1, tuote, tarkenne_yleinen, tarkenne_sievitalo.
    """
    try:
        with SessionLocal() as db:
            # Suorita kysely
            tulokset = db.query(
                Tuote.id,
                Tuote.prompt_1,
                Tuote.tuote,
                Tuote.tarkenne_yleinen,
                Tuote.tarkenne_sievitalo
            ).all()
            
            # Tulosta tulokset
            for tulos in tulokset:
                print(f"id: {tulos.id}, prompt_1: {tulos.prompt_1}, tuote: {tulos.tuote}, "
                    f"tarkenne_yleinen: {tulos.tarkenne_yleinen}, tarkenne_sievitalo: {tulos.tarkenne_sievitalo}")
            
            return tulokset

    except Exception as e:
        print(f"Virhe kyselyssä: {str(e)}")
        return None


def hae_tuotteet_if_prompt_1_true():
    """
    Hakee tuotteet-taulusta seuraavat kentät: id, prompt_1, tuote, tarkenne_yleinen, tarkenne_sievitalo.
    Suodattaa rivit, joissa prompt_1 on True.
    """
    try:
        with SessionLocal() as db:
            # Suorita kysely, joka suodattaa prompt_1 == True
            tulokset = db.query(
                Tuote.id,
                Tuote.prompt_1,
                Tuote.tuote,
                Tuote.tarkenne_yleinen,
                Tuote.tarkenne_sievitalo
            ).filter(Tuote.prompt_1 == True).all()
            
            # Tulosta tulokset
            for tulos in tulokset:
                tarkenne_yleinen = tulos.tarkenne_yleinen if tulos.tarkenne_yleinen is not None else ' '
                tarkenne_sievitalo = tulos.tarkenne_sievitalo if tulos.tarkenne_sievitalo is not None else ' '
                
                # print(f"id: {tulos.id}, tuote: {tulos.tuote}, "
                #       f"tarkenne_yleinen: {tarkenne_yleinen}, tarkenne_sievitalo: {tarkenne_sievitalo}")
            
            return tulokset

    except Exception as e:
        print(f"Virhe kyselyssä: {str(e)}")
        return None

def tulosta_tuotteet(tulokset):
    """
    Palauttaa listan, jossa jokainen tuote on oma alkionsa ilman otsaketta.
    """
    tulostuslista = []
    for tulos in tulokset:
        tuote = tulos[2]
        tarkenne_yleinen = tulos[3] if tulos[3] is not None else ''
        tarkenne_sievitalo = tulos[4] if tulos[4] is not None else ''
        
        # Luo tulostettava merkkijono
        tulostettava = f"{tuote}"
        if tarkenne_yleinen:
            tulostettava += f" {tarkenne_yleinen}"
        if tarkenne_sievitalo:
            tulostettava += f" {tarkenne_sievitalo}"
        
        # Lisää jokainen tuote omana alkionaan listaan
        tulostuslista.append(tulostettava)
    
    return tulostuslista

def hae_tuotteet_suodatettu_json():
    """
    Hakee tuotteet-taulusta seuraavat kentät: id, prompt_1, tuote, tarkenne_yleinen, tarkenne_sievitalo.
    Suodattaa rivit, joissa prompt_1 on True ja palauttaa tulokset JSON-muodossa.
    """
    try:
        with SessionLocal() as db:
            # Suorita kysely
            tulokset = db.query(
                Tuote.id,
                Tuote.prompt_1,
                Tuote.tuote,
                Tuote.tarkenne_yleinen,
                Tuote.tarkenne_sievitalo
            ).filter(Tuote.prompt_1 == True).all()
            
            # Muunna tulokset JSON-muotoon
            json_tulokset = [
                {
                    "id": tulos.id,
                    "prompt_1": tulos.prompt_1,
                    "tuote": tulos.tuote,
                    "tarkenne_yleinen": tulos.tarkenne_yleinen if tulos.tarkenne_yleinen else "Ei tietoa",
                    "tarkenne_sievitalo": tulos.tarkenne_sievitalo if tulos.tarkenne_sievitalo else "Ei tietoa"
                }
                for tulos in tulokset
            ]
            
            json_data = json.dumps(json_tulokset, ensure_ascii=False, indent=4)
            print(json_data)
            
            return json_data

    except Exception as e:
        print(f"Virhe kyselyssä: {str(e)}")
        return None


