from config_data import UPLOAD_FOLDER_DATA
from sqlalchemy import create_engine, text, inspect, Table, Column, Integer, Boolean, String, DECIMAL, ForeignKey, text
from sqlalchemy.orm import Session
from db_luokat import Base, Tuote, engine
from db_luokat import SessionLocal, Toimitussisalto, Kayttaja, Toimittaja, Ikkuna, Ulko_ovi, Valiovi, Base, Tuote
from decimal import Decimal
from tabulate import tabulate  # Asentaa: pip install tabulate
import os
import pandas as pd
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




#==================================== tyhjenna_tuotteet_taulu(kysy_varmistus=True)
def tyhjenna_tuotteet_taulu(kysy_varmistus=True):
    """
    Tyhjentää tuotteet-taulun tietokannasta.
    
    Args:
        kysy_varmistus (bool): Jos True, kysyy varmistuksen ennen poistoa
    
    Returns:
        bool: True jos tyhjennys onnistui, False jos epäonnistui
    """
    try:
        # Näytä ensin montako tuotetta ollaan poistamassa
        session = SessionLocal()
        tuotteiden_maara = session.query(Tuote).count()
        session.close()
        
        if tuotteiden_maara == 0:
            print("Taulu on jo tyhjä!")
            return True
        
        # Kysy varmistus jos tarpeen
        if kysy_varmistus:
            print(f"\nOlet poistamassa {tuotteiden_maara} tuotetta taulusta.")
            print("HUOMIO: Tätä toimintoa ei voi peruuttaa!")
            vastaus = input("Haluatko varmasti tyhjentää taulun? (kirjoita 'KYLLÄ' jatkaaksesi): ")
            
            if vastaus != "KYLLÄ":
                print("Toiminto peruttu.")
                return False
        
        # Tyhjennä taulu
        session = SessionLocal()
        try:
            session.query(Tuote).delete()
            session.commit()
            print(f"Taulu tyhjennetty onnistuneesti! {tuotteiden_maara} tuotetta poistettu.")
            return True
            
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Virhe taulun tyhjennyksessä: {str(e)}")
            return False
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"Odottamaton virhe: {str(e)}")
        return False


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

