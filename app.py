from flask import Flask, request, render_template, render_template_string, Response, redirect, url_for, jsonify
import os
import sys
import uuid
from werkzeug.utils import secure_filename
import io
from db_luokat import SessionLocal, Toimitussisallot
from sqlalchemy import create_engine, text
import logging

sys.path.append(os.path.abspath("utils"))  # Lisää utils-kansion polku moduulihakemistoksi
sys.path.append(os.path.abspath("api_kyselyt"))

from config_data import (VALIOVITYYPIT_SIEVITALO_JSON, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT,  
                        IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNA2_JSON, ULKO_OVI_TIEDOT_2_JSON,
                        TOIMITUSSISALTO_SIEVITALO_TXT, TOIMITUSSISALTO_KASTELLI_TXT, TOIMITUSSISALTO_TXT,                        
                        PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, 
                        PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT,
                        PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT,
                        PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT, PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, VALIOVITYYPIT_KASTELLI_JSON, TOIMITUSSISALTO_DESIGNTALO_TXT,
                        UPLOAD_FOLDER_DATA)


from datetime import datetime 
import json
from generation_config import GENERATION_CONFIG

from utils.file_handler import (tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto,
                                kirjoita_txt_tiedosto, normalisoi_ulko_ovet, muuta_pdf_tekstiksi_ilman_tallennusta, 
                                lue_txt_sisalto_uuidlla)

from utils.tietosissallon_kasittely import sievitalo_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi, clean_text2
from run import run_sievitalo, run_kastelli
from factory import get_sievitalo_ikkunat, get_sievitalo_ulko_ovet, get_sievitalo_valiovi_mallit, get_kastelli_ikkunat, get_kastelli_ulko_ovet, get_kastelli_valiovi_mallit
from SQL_kyselyt import hae_toimittaja_uuidlla, hae_toimitussisalto_txt_polku_uuidlla, hae_toimitussisalto_id_uuidlla

import google.generativeai as genai 

# Sovelluksen käynnistyessä
logging.basicConfig(level=logging.INFO)
logging.info("🔹 Sovellus käynnistyy")

print("Haetaan ympäristömuuttujat")
print(f"- DATABASE_URL löytyy: {'Kyllä' if os.environ.get('DATABASE_URL') else 'Ei'}")
print(f"- GEMINI_API_KEY löytyy: {'Kyllä' if os.environ.get('GEMINI_API_KEY') else 'Ei'}")
env = os.getenv('ENV')
print(f"Ympäristö: {env}")

print("TULOSTETAAN PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT")
print(PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT)

print("JUHON LISÄYS")

print("Lue PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT")
with open("C:\\talobot_env\data\s\prompt_sievitalo_poimi_ikkunatiedot.txt", "r") as tiedosto:
    print(tiedosto.read())

#with open(PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, "r") as tiedosto:
    #print(tiedosto.read())


def generate_uuid():
    return str(uuid.uuid4())

# Jos käytät tietokantayhteyttä, lisää sen testaus
try:
    with SessionLocal() as db:
        db.execute(text("SELECT 1"))
        print("✅ Tietokantayhteys toimii")
except Exception as e:
    print(f"❌ Tietokantayhteys epäonnistui: {str(e)}")

print(f"aika nyt {datetime.now}")

#🔹 Tunnistaa toimittajan nimen toimitussisällöstä
def tunnista_toimittaja(teksti):
    """Etsii toimittajan nimen toimitussisällöstä"""
    #toimittajat = ["Sievitalo", "Kastelli"]
    toimittajat = ["Sievitalo", "Kastelli", "Designtalo"]
    for nimi in toimittajat:
        if nimi in teksti:
            return nimi
    return None

#------------------------------------------------------------------
#kirjoitetaan ensimmainen_toimitussisalto kantaan
#-----------------------------------------------------------------
def ensimmainen_toimitussisalto(file):
    print("Aloitetaan ensimmainen_toimitussisalto")
    #file = request.files["ensimmainen_toimitussisalto"]            
    # 🔹 Luo UUID-tunniste ja tallenna PDF palvelimelle
    unique_id = generate_uuid()
    pdf_filename = f"{unique_id}.pdf"
    pdf_filepath = UPLOAD_FOLDER_DATA / pdf_filename
    
    # 🔹 Lue tiedosto muistiin ennen tallennusta
    file_data = file.read()  # Lue sisältö talteen
    
    # 🔹 Varmista, että kansio on olemassa
    if not UPLOAD_FOLDER_DATA.exists():
        print("❌ Kansio puuttuu, luodaan...")
        UPLOAD_FOLDER_DATA.mkdir(parents=True, exist_ok=True)

    pdf_filepath = UPLOAD_FOLDER_DATA / pdf_filename  # tämä on Path-objekti
    
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

        
          
    db = SessionLocal()
    try:
        uusi_toimitussisalto = Toimitussisallot(
            kayttaja_id=1,
            uuid=unique_id,
            pdf_url=str(pdf_filepath),
            txt_sisalto=str(txt_filepath),
            toimittaja=toimittaja,
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


#------------------------------------------------------------------
#kirjoitetaan toinen_toimitussisalto kantaan
#-----------------------------------------------------------------
def toinen_toimitussisalto(file):
    print("toinen_toimitussisalto")
    #file = request.files["toinen_toimitussisalto"]            
    # 🔹 Luo UUID-tunniste ja tallenna PDF palvelimelle
    unique_id = generate_uuid()
    pdf_filename = f"{unique_id}.pdf"
    pdf_filepath = UPLOAD_FOLDER_DATA / pdf_filename
    
    # 🔹 Lue tiedosto muistiin ennen tallennusta
    file_data = file.read()  # Lue sisältö talteen
    
    # 🔹 Varmista, että kansio on olemassa
    if not UPLOAD_FOLDER_DATA.exists():
        print("❌ Kansio puuttuu, luodaan...")
        UPLOAD_FOLDER_DATA.mkdir(parents=True, exist_ok=True)

    pdf_filepath = UPLOAD_FOLDER_DATA / pdf_filename  # tämä on Path-objekti
    
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

        
          
    db = SessionLocal()
    try:
        uusi_toimitussisalto = Toimitussisallot(
            kayttaja_id=1,
            uuid=unique_id,
            pdf_url=str(pdf_filepath),
            txt_sisalto=str(txt_filepath),
            toimittaja=toimittaja,
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








app = Flask(__name__)
os.makedirs(UPLOAD_FOLDER_DATA, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER_DATA
@app.route("/suodata_tiedot", methods=["GET", "POST"])
def suodata_tiedot():
    try:
        # Jos kyseessä on POST-pyyntö, käsittele PDF-tiedostot
        if request.method == "POST":
            tulokset = {}
        
            
            #Ensimmainen toimitussisalto. Tallentaa pdf ja tekstitiedoston palvelimelle uuid -tunnuksella
            if "ensimmainen_toimitussisalto" in request.files:
                file = request.files["ensimmainen_toimitussisalto"]            
                print("rivi 78")
                unique_id_ensimmainen_toimitussisalto = ensimmainen_toimitussisalto(file)
                print("ensimmainen_toimitussialato lisatty")
                print(f"toimittaja: {unique_id_ensimmainen_toimitussisalto}")
            #Toinen toimitussisalto. Tallentaa pdf ja tekstitiedoston palvelimelle uuid -tunnuksella
            if "toinen_toimitussisalto" in request.files:
                file = request.files["toinen_toimitussisalto"]            
                unique_id_toinen_toimitussisalto = toinen_toimitussisalto(file)
                print("toinen_toimitussisalto lisatty")


        #Käsittele Sievitalo txt-tiedosto
        if hae_toimittaja_uuidlla(unique_id_ensimmainen_toimitussisalto) == "Sievitalo":
            
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     run_sievitalo       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            print("run_sievitalo 224")
            run_sievitalo(lue_txt_tiedosto(hae_toimitussisalto_txt_polku_uuidlla(unique_id_ensimmainen_toimitussisalto)), hae_toimitussisalto_id_uuidlla(unique_id_ensimmainen_toimitussisalto))
                      
           
           
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     run_kastelli       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

            print(f"unique_id_toinen_toimitussisalto: {unique_id_toinen_toimitussisalto}")
        if hae_toimittaja_uuidlla(unique_id_toinen_toimitussisalto) == "Kastelli":
            print("app.py 224")
            run_kastelli(lue_txt_tiedosto(hae_toimitussisalto_txt_polku_uuidlla(unique_id_toinen_toimitussisalto)), hae_toimitussisalto_id_uuidlla(unique_id_toinen_toimitussisalto))
        
        


            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     run_designtalo       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        else:
                    print("app.py 228")
                    tulokset["sievitalo"] = {"error": "Väärä toimittaja"}
        '''
       


            # Käsittele Designtalon PDF
            if "designtalo_pdf" in request.files:
                file = request.files["designtalo_pdf"]
                if file.filename != '':
                    teksti = muuta_pdf_tekstiksi(file)
                    toimittaja = tunnista_toimittaja(teksti)
                    

                    if toimittaja == "Designtalo":
                        kirjoita_txt_tiedosto(teksti, TOIMITUSSISALTO_DESIGNTALO_TXT)
                        
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     run_designtalo       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        run_designtalo()
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                               
                        tulokset["designtalo"] = {
                            "ikkunat": get_designtalo_ikkunat(),
                            "ulko_ovet": get_designtalo_ulko_ovet(),
                            "valiovi_mallit": get_designtalo_valiovi_mallit()
                        }
                    else:
                        tulokset["designtalo"] = {"error": "Väärä toimittaja"}
                '''



        # Jos pyyntö on AJAX-pyyntö, palauta JSON-data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response(
                json.dumps(tulokset),
                mimetype='application/json'
            )
        
        # Jos ei ole AJAX-pyyntö, näytä template
        return render_template("index.html", tulokset=tulokset)

    except Exception as e:
        # Virheiden käsittely
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response(
                json.dumps({'error': str(e)}),
                mimetype='application/json'
            )
        return render_template("virhe.html", virheviesti=f"Tietojen käsittelyssä tapahtui virhe: {e}")

    # Oletuspalautus GET-pyynnölle
    return render_template("index.html")


   

@app.route("/", methods=["GET", "POST"])
def index():
    # Näytä index.html-sivu
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)



