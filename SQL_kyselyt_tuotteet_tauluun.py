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

from datetime import datetime
from logger_config import configure_logging
import logging

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
def tuo_tuotteet_sheetista(csv_url):
    """
    Tuo tuotteet Google Sheets -taulukosta tietokantaan.
    """
    try:
        print(f"Luetaan dataa osoitteesta: {csv_url}")
        
        # Lue CSV pandas DataFrameen
        df = pd.read_csv(csv_url, skiprows=1)  # Ohita tyhjä rivi
        
        # Poista tyhjät rivit
        df = df.dropna(how='all')
        
        print(f"Luettiin {len(df)} riviä dataa")
        
        session = SessionLocal()
        
        try:
            lisatyt = 0
            virheet = 0
            
            for index, row in df.iterrows():
                try:
                    # Paranna hinnan käsittelyä
                    if pd.notna(row['hinta']):
                        # Käsittele hinta-arvo
                        hinta_str = str(row['hinta']).strip()
                        # Korvaa eri miinusmerkit standardilla
                        hinta_str = hinta_str.replace('−', '-')  # Unicode miinus
                        hinta_str = hinta_str.replace(',', '.')  # Pilkku pisteeksi
                        try:
                            hinta = Decimal(hinta_str)
                        except:
                            print(f"Virheellinen hinta rivillä {index + 2}: '{hinta_str}'")
                            print(f"Rivin data: {row.to_dict()}")
                            virheet += 1
                            continue
                    else:
                        hinta = None  # Jos hinta on tyhjä
                    
                    # Luo uusi Tuote-objekti
                    tuote = Tuote(
                        prompt_1=bool(row['prompt_1']),
                        prompt_2=bool(row['prompt_2']),
                        tuote=str(row['tuote']),
                        tuote_tarkennus=str(row['tuote_tarkenne']) if pd.notna(row['tuote_tarkenne']) else None,
                        yksikko=str(row['yksikko']) if pd.notna(row['yksikko']) else None,
                        hinta=hinta,
                        onko_hinta_absoluuttinen=bool(row['onko_hinta_absoluuttinen'])
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
            
        except Exception as e:
            print(f"Virhe tietojen tallennuksessa: {str(e)}")
            session.rollback()
        
        finally:
            session.close()
            
    except Exception as e:
        print(f"Virhe tietojen tuonnissa: {str(e)}")




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


#==================================== muuta_tuotteet_taulun_hinta_sarake_nullable()
def muuta_tuotteet_taulun_hinta_sarake_nullable():
    """
    Muuttaa tuotteet-taulun hinta-sarakkeen nullable-arvoksi True.
    """
    try:
        # Suorita ALTER TABLE -komento
        with engine.connect() as connection:
            with connection.begin():
                # Muuta sarakkeen nullable-arvo
                connection.execute(text("""
                    ALTER TABLE tuotteet 
                    ALTER COLUMN hinta DROP NOT NULL;
                """))
                
        print("Hinta-sarakkeen nullable-arvo muutettu onnistuneesti!")
        return True
        
    except Exception as e:
        print(f"Virhe sarakkeen muokkauksessa: {str(e)}")
        return False


#==================================== muuta_sarakkeen_nimi()
def muuta_tuotteet_taulun_sarakkeen_nimi():
    """
    Muuttaa sarakkeen nimen 'hinta_lisahinta_johonkin' -> 'onko_hinta_absoluuttinen'
    """
    try:
        # Luo yhteys tietokantaan
        with engine.connect() as connection:
            with connection.begin():
                # Suorita ALTER TABLE -komento
                connection.execute(text("""
                    ALTER TABLE tuotteet 
                    RENAME COLUMN hinta_lisahinta_johonkin TO onko_hinta_absoluuttinen;
                """))
                
        print("Sarakkeen nimi muutettu onnistuneesti!")
        return True
        
    except Exception as e:
        print(f"Virhe sarakkeen nimen muutoksessa: {str(e)}")
        return False


#==================================== lisaa_viite_tuote_id_sarake()
def lisaa_tuotteet_taulun_viite_tuote_id_sarake():  
    """
    Lisää viite_tuote_id-sarakkeen tuotteet-tauluun
    """
    try:
        # Luo yhteys tietokantaan
        with engine.connect() as connection:
            with connection.begin():
                # Lisää sarake ja foreign key -viittaus
                connection.execute(text("""
                    ALTER TABLE tuotteet 
                    ADD COLUMN viite_tuote_id INTEGER;
                """))
                
                # Lisää foreign key -viittaus
                connection.execute(text("""
                    ALTER TABLE tuotteet
                    ADD CONSTRAINT fk_viite_tuote
                    FOREIGN KEY (viite_tuote_id) 
                    REFERENCES tuotteet(id);
                """))
                
        print("viite_tuote_id-sarake lisätty onnistuneesti!")
        return True
        
    except Exception as e:
        print(f"Virhe sarakkeen lisäyksessä: {str(e)}")
        return False


#==================================== korjaa_tuotteet_taulun_null_arvot()
def korjaa_tuotteet_taulun_null_arvot():
    """
    Korjaa tuotteet-taulun sarakkeiden NULL-arvot vastaamaan luokan määrittelyä
    """
    try:
        with engine.connect() as connection:
            with connection.begin():
                # Muuta tuote_tarkennus nullable
                connection.execute(text("""
                    ALTER TABLE tuotteet 
                    ALTER COLUMN tuote_tarkennus DROP NOT NULL;
                """))
                
                # Muuta yksikko nullable
                connection.execute(text("""
                    ALTER TABLE tuotteet 
                    ALTER COLUMN yksikko DROP NOT NULL;
                """))
                
        print("Sarakkeiden NULL-arvot korjattu onnistuneesti!")
        return True
        
    except Exception as e:
        print(f"Virhe NULL-arvojen korjauksessa: {str(e)}")
        return False

#
def luo_tuotteet_taulu_uudelleen():
    """
    Luo tuotteet-taulun uudelleen oikealla rakenteella
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
                        prompt_1 BOOLEAN NOT NULL,
                        prompt_2 BOOLEAN NOT NULL,
                        tuote VARCHAR(100) NOT NULL,
                        tuote_tarkennus VARCHAR(100),
                        yksikko VARCHAR(50),
                        hinta DECIMAL(10,2),
                        onko_hinta_absoluuttinen BOOLEAN NOT NULL DEFAULT FALSE,
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




#==================================== korjaa_tuotteet_taulu()
def korjaa_tuotteet_taulu():
    """
    Korjaa tuotteet-taulun rakenteen vastaamaan db_luokat.py:n määrittelyä.
    Näyttää rakenteen ennen ja jälkeen muutoksen.
    """
    try:
        # Näytä nykyinen rakenne
        inspector = inspect(engine)
        columns = inspector.get_columns('tuotteet')
        # Tyhjennä SQLAlchemy:n metadata välimuisti
        Base.metadata.clear()
        
        print("Nykyinen taulun rakenne:")
        print("-" * 60)
        print(f"{'Sarake':<25} {'Tyyppi':<15} {'NULL?':<8}")
        print("-" * 60)
        for column in columns:
            nullable = "YES" if column['nullable'] else "NO"
            print(f"{column['name']:<25} {str(column['type']):<15} {nullable:<8}")

        # Varmistus käyttäjältä
        print("\nTaulun rakenne päivitetään vastaamaan db_luokat.py määrittelyä.")
        vastaus = input("Haluatko jatkaa? (k/e): ")
        if vastaus.lower() != 'k':
            print("Toiminto peruttu.")
            return False

        with engine.connect() as connection:
            with connection.begin():
                # Poista vanha taulu
                connection.execute(text("DROP TABLE IF EXISTS tuotteet CASCADE;"))
                
                # Luo taulu uudelleen db_luokat.py:n määrittelyn mukaan
                Base.metadata.create_all(engine)

        # Näytä uusi rakenne
        inspector = inspect(engine)
        columns = inspector.get_columns('tuotteet')
        
        print("\nUusi taulun rakenne:")
        print("-" * 60)
        print(f"{'Sarake':<25} {'Tyyppi':<15} {'NULL?':<8}")
        print("-" * 60)
        for column in columns:
            nullable = "YES" if column['nullable'] else "NO"
            print(f"{column['name']:<25} {str(column['type']):<15} {nullable:<8}")

        print("\nTaulun rakenne korjattu onnistuneesti!")
        return True

    except Exception as e:
        print(f"Virhe taulun korjauksessa: {str(e)}")
        return False



#==================================== nayta_tuotteet()
def nayta_tuotteet():
    """
    Hakee ja näyttää kaikki tuotteet siistinä taulukkona.
    """
    try:
        session = SessionLocal()
        
        # Hae kaikki tuotteet
        tuotteet = session.query(Tuote).order_by(Tuote.id).all()
        
        if not tuotteet:
            print("Tuotteet-taulu on tyhjä!")
            return
        
        # Muodosta data taulukkoa varten
        headers = ['ID', 'Tuote', 'Tarkenne', 'Yksikkö', 'Hinta', 'Abs.', 'P1', 'P2', 'Viite ID']
        data = []
        
        for t in tuotteet:
            # Muotoile hinta siististi
            hinta = f"{float(t.hinta):.2f}" if t.hinta is not None else "-"
            
            # Lisää rivi dataan
            data.append([
                t.id,
                t.tuote[:40],  # Rajoita tuotteen nimen pituutta
                t.tuote_tarkennus[:20] if t.tuote_tarkennus else "-",
                t.yksikko if t.yksikko else "-",
                hinta,
                "X" if t.onko_hinta_absoluuttinen else "-",
                "X" if t.prompt_1 else "-",
                "X" if t.prompt_2 else "-",
                t.viite_tuote_id if t.viite_tuote_id else "-"
            ])
        
        # Tulosta taulukko
        print("\nTuotteet:")
        print(tabulate(
            data,
            headers=headers,
            tablefmt='grid',
            numalign='right',
            stralign='left'
        ))
        
        # Tulosta yhteenveto
        print(f"\nYhteensä {len(tuotteet)} tuotetta")
        
    except Exception as e:
        print(f"Virhe tuotteiden haussa: {str(e)}")
    
    finally:
        session.close()



#==================================== nayta_tuote(tuote_id)
def nayta_tuote(tuote_id):
    """
    Näyttää yhden tuotteen kaikki tiedot.
    
    Args:
        tuote_id (int): Tuotteen ID
    """
    try:
        session = SessionLocal()
        tuote = session.query(Tuote).filter(Tuote.id == tuote_id).first()
        
        if not tuote:
            print(f"Tuotetta ID:llä {tuote_id} ei löytynyt!")
            return
        
        print("\nTuotteen tiedot:")
        print("-" * 40)
        print(f"ID: {tuote.id}")
        print(f"Tuote: {tuote.tuote}")
        print(f"Tarkenne: {tuote.tuote_tarkennus or '-'}")
        print(f"Yksikkö: {tuote.yksikko or '-'}")
        print(f"Hinta: {float(tuote.hinta):.2f} €" if tuote.hinta else "Hinta: -")
        print(f"Absoluuttinen hinta: {'Kyllä' if tuote.onko_hinta_absoluuttinen else 'Ei'}")
        print(f"Prompt 1: {'Kyllä' if tuote.prompt_1 else 'Ei'}")
        print(f"Prompt 2: {'Kyllä' if tuote.prompt_2 else 'Ei'}")
        print(f"Viite tuote ID: {tuote.viite_tuote_id or '-'}")
        
    except Exception as e:
        print(f"Virhe tuotteen haussa: {str(e)}")
    
    finally:
        session.close()


#==================================== tallenna_tuotteet_tiedostoon(tiedostopolku)
def tallenna_tuotteet_tiedostoon(tiedostopolku):
    """
    Hakee kaikki tuotteet ja tallentaa ne CSV-tiedostoon.
    
    Args:
        tiedostopolku (str): Polku, johon CSV-tiedosto tallennetaan
    """
    try:
        session = SessionLocal()
        
        # Hae kaikki tuotteet
        tuotteet = session.query(Tuote).order_by(Tuote.id).all()
        
        if not tuotteet:
            print("Tuotteet-taulu on tyhjä!")
            return False
        
        # Lisää aikaleima tiedostonimeen
        aikaleima = datetime.now().strftime("%Y%m%d_%H%M%S")
        tiedostonimi = f"tuotteet_{aikaleima}.csv"
        
        if tiedostopolku:
            koko_polku = f"{tiedostopolku}/{tiedostonimi}"
        else:
            koko_polku = tiedostonimi
        
        # Määritä sarakkeet
        headers = ['ID', 'Tuote', 'Tarkenne', 'Yksikkö', 'Hinta', 'Absoluuttinen hinta', 
                  'Prompt 1', 'Prompt 2', 'Viite tuote ID']
        
        # Kirjoita CSV-tiedosto
        with open(koko_polku, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')  # Käytä puolipistettä erottimena
            
            # Kirjoita otsikkorivi
            writer.writerow(headers)
            
            # Kirjoita tuotteet
            for t in tuotteet:
                # Muotoile hinta siististi
                hinta = f"{float(t.hinta):.2f}" if t.hinta is not None else ""
                
                writer.writerow([
                    t.id,
                    t.tuote,
                    t.tuote_tarkennus if t.tuote_tarkennus else "",
                    t.yksikko if t.yksikko else "",
                    hinta,
                    "Kyllä" if t.onko_hinta_absoluuttinen else "Ei",
                    "Kyllä" if t.prompt_1 else "Ei",
                    "Kyllä" if t.prompt_2 else "Ei",
                    t.viite_tuote_id if t.viite_tuote_id else ""
                ])
        
        print(f"\nTuotteet tallennettu tiedostoon: {koko_polku}")
        print(f"Yhteensä {len(tuotteet)} tuotetta tallennettu")
        return True
        
    except Exception as e:
        print(f"Virhe tuotteiden tallennuksessa: {str(e)}")
        return False
    
    finally:
        session.close()

#==================================== tallenna_tuotteet_ID_ja_nimi_tiedostoon(tiedostopolku)
def tallenna_tuotteet_ID_ja_nimi_tiedostoon(tiedostopolku):
    """
    Hakee tuotteista vain ID:n ja nimen sellaisista riveistä, joissa prompt_1 on True.
    Tallentaa tulokset CSV-tiedostoon.
    """
    try:
        session = SessionLocal()
        
        # Korjattu kysely ilman ylimääräisiä rivinvaihtoja
        tuotteet = session.query(Tuote.id, Tuote.tuote).filter(Tuote.prompt_1.is_(True)).order_by(Tuote.id).all()
        
        if not tuotteet:
            print("Ei löytynyt tuotteita joissa prompt_1 on True!")
            return False
        
        # Lisää aikaleima tiedostonimeen
        aikaleima = datetime.now().strftime("%Y%m%d_%H%M%S")
        tiedostonimi = f"tuotteet_prompt1_true_{aikaleima}.csv"
        
        if tiedostopolku:
            koko_polku = f"{tiedostopolku}/{tiedostonimi}"
        else:
            koko_polku = tiedostonimi
        
        # Määritä sarakkeet
        headers = ['ID', 'Tuote']
        
        # Kirjoita CSV-tiedosto
        with open(koko_polku, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(headers)
            
            for t in tuotteet:
                writer.writerow([
                    t[0],  # id
                    t[1]   # tuote
                ])
        
        print(f"\nPrompt 1 = True tuotteet tallennettu tiedostoon: {koko_polku}")
        print(f"Yhteensä {len(tuotteet)} tuotetta tallennettu")
        return True
        
    except Exception as e:
        print(f"Virhe tuotteiden tallennuksessa: {str(e)}")
        return False
    
    finally:
        session.close()

#==================================== hae_tuotteet_prompt1_str()
def hae_tuotteet_prompt1_str():
    """
    Hakee tuotteista ID:n ja nimen sellaisista riveistä, joissa prompt_1 on True.
    Palauttaa tiedot str-muotoisena CSV-formaatissa.
    """
    try:
        session = SessionLocal()
        
        # Debug: tulostetaan ensin koko kysely
        kysely = session.query(Tuote.id, Tuote.tuote).filter(Tuote.prompt_1.is_(True))
        logging.debug(f"SQL kysely: {kysely}")
        
        # Suoritetaan kysely
        tuotteet = kysely.order_by(Tuote.id).all()
        
        # Debug: tulostetaan jokaisen rivin prompt_1 arvo
        for t in tuotteet:
            rivi = session.query(Tuote).get(t[0])
            logging.debug(f"ID: {t[0]}, prompt_1: {rivi.prompt_1}")
        
        output = StringIO()
        writer = csv.writer(output, delimiter=';', lineterminator='\n')
        writer.writerow(['ID', 'Tuote'])
        
        for t in tuotteet:
            writer.writerow([t[0], t[1]])
        
        csv_str = output.getvalue()
        output.close()
        
        return csv_str
        
    except Exception as e:
        logging.error(f"Virhe tuotteiden haussa: {str(e)}")
        return None
    
    finally:
        session.close()


def tarkista_prompt1_arvot():
    """
    Tarkistaa prompt_1 sarakkeen arvot tietokannasta
    """
    try:
        session = SessionLocal()
        
        # Haetaan kaikki rivit ja tulostetaan prompt_1 arvot
        tuotteet = session.query(Tuote.id, Tuote.tuote, Tuote.prompt_1).all()
        
        # print("\nPrompt_1 arvojen tarkistus:")
        # print("ID | Tuote | prompt_1 | Tyyppi")
        # print("-" * 50)
        for t in tuotteet:
            print(f"{t.id} | {t.tuote} | {t.prompt_1} | {type(t.prompt_1)}")
            
    except Exception as e:
        print(f"Virhe tarkistuksessa: {str(e)}")
    finally:
        session.close()


