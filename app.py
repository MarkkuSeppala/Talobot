from flask import Flask, request, render_template, render_template_string, Response, redirect, url_for, jsonify
import os
import sys
import uuid
from werkzeug.utils import secure_filename
import io
from db_luokat import SessionLocal, Toimitussisalto
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
from SQL_kyselyt import hae_toimittaja_uuidlla, hae_toimitussisalto_txt_polku_uuidlla, hae_toimitussisalto_id_uuidlla, vastaanota_toimitussisalto

import google.generativeai as genai 



# Loggerin alustus
logging.basicConfig(level=logging.INFO)
logging.info("🔹 Sovellus käynnistyy")

# Tietokantayhteyden testaus
try:
    with SessionLocal() as db:
        db.execute(text("SELECT 1"))
        logging.info("✅ Tietokantayhteys toimii")
except Exception as e:
    logging.warning(f"❌ Tietokantayhteys epäonnistui: {str(e)}")

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
                unique_id_ensimmainen_toimitussisalto = vastaanota_toimitussisalto(file)
                    
            #Toinen toimitussisalto. Tallentaa pdf ja tekstitiedoston palvelimelle uuid -tunnuksella
            if "toinen_toimitussisalto" in request.files:
                file = request.files["toinen_toimitussisalto"]            
                unique_id_toinen_toimitussisalto = vastaanota_toimitussisalto(file)
                logging.info("Toinen toimitussisältö lisätty, toimittaja: {unique_id__toimitussisalto}")

                
        #Oliko toimitussisalto sievitalon?
        logging.info(unique_id_ensimmainen_toimitussisalto)
        if hae_toimitussisalto_id_uuidlla(unique_id_ensimmainen_toimitussisalto) == "Sievitalo":

            #Sievitalon toimitussisalto puhdistetaan turhista merkeistä ja suodatetaan ikkunat, ulko-ovet, valiovet ja tallennetaaan ne kantaan
            run_sievitalo(lue_txt_tiedosto(hae_toimitussisalto_txt_polku_uuidlla(unique_id_ensimmainen_toimitussisalto)), hae_toimitussisalto_id_uuidlla(unique_id_ensimmainen_toimitussisalto))

        #Oliko toimitussisalto kastellin?
        if hae_toimitussisalto_id_uuidlla(unique_id_toinen_toimitussisalto) == "Kastelli":

            #Kastellin toimitussisalto puhdistetaan turhista merkeistä ja suodatetaan ikkunat, ulko-ovet, valiovet ja tallennetaaan ne kantaan
            run_kastelli(lue_txt_tiedosto(hae_toimitussisalto_txt_polku_uuidlla(unique_id_toinen_toimitussisalto)), hae_toimitussisalto_id_uuidlla(unique_id_toinen_toimitussisalto))
        
        #Oliko toimitussisalto .....
        #if hae_toimittaja_uuidlla(unique_id_toinen_toimitussisalto) == "Designtalo":
        
            #Designtalon toimitussisalto puhdistetaan turhista merkeistä ja suodatetaan ikkunat, ulko-ovet, valiovet ja tallennetaaan ne kantaan
            #run_designtalo(lue_txt_tiedosto(hae_toimitussisalto_txt_polku_uuidlla(unique_id_toinen_toimitussisalto)), hae_toimitussisalto_id_uuidlla(unique_id_toinen_toimitussisalto)) 
    

        else:
            tulokset["sievitalo"] = {"error": "Tuntematon toimittaja"}



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



