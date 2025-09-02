from flask import Flask, request, render_template, render_template_string, Response, redirect, url_for, jsonify
import os
import sys
import uuid
from werkzeug.utils import secure_filename
import io
from db_luokat import SessionLocal, Toimitussisalto
from sqlalchemy import create_engine, text
from logger_config import configure_logging
import logging
from SQL_kyselyt import*
print("app.py 12")

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
                                lue_txt_url_uuidlla)

from utils.tietosissallon_kasittely import *
from run import run_sievitalo, run_kastelli
from factory import get_sievitalo_ikkunat, get_sievitalo_ulko_ovet, get_sievitalo_valiovi_mallit, get_kastelli_ikkunat, get_kastelli_ulko_ovet, get_kastelli_valiovi_mallit
from SQL_kyselyt import (hae_toimittaja_uuidlla, hae_toimitussisalto_txt_url_uuidlla, hae_toimitussisalto_id_uuidlla, 
                         vastaanota_toimitussisalto, hae_paivan_toimitussisallot, hae_paivan_ulko_ovet, hae_paivan_valiovet, lisaa_vertailu,
                         hae_pdf_url_uuidlla, hae_uuid_toimitussisalto_idlla, hae_toimitussisallon_ikkunat, hae_toimitussisallon_ulko_ovet, hae_toimitussisallon_valiovet)

import google.generativeai as genai 

# Logger alustus
configure_logging()
logger = logging.getLogger(__name__)

logging.info("Sovellus käynnistyy")
logging.info("Test")
logging.info("TESTIMUUTOS: Git-ikkuna testi")

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
                pdf_file_1 = request.files["ensimmainen_toimitussisalto"]
                # pdf_content = pdf_file_1.read()
                # pdf_file_like = io.BytesIO(pdf_content)
                unique_tiedostonimi_ensimmainen_toimitussisalto = vastaanota_toimitussisalto(pdf_file_1)
                logging.info("Ensimmäinen toimitussisältö lisätty kantaan, toimittaja: {unique_tiedostonimi_ensimmainen_toimitussisalto}")

                
            #Toinen toimitussisalto. Tallentaa pdf ja tekstitiedoston palvelimelle uuid -tunnuksella
            if "toinen_toimitussisalto" in request.files:
                pdf_file_2 = request.files["toinen_toimitussisalto"]            
                unique_tiedostonimi_toinen_toimitussisalto = vastaanota_toimitussisalto(pdf_file_2)
                logging.info("Toinen toimitussisältö lisätty kantaan, toimittaja: {unique_tiedostonimi_toinen_toimitussisalto}")

                
                
                lisaa_vertailu(hae_toimitussisalto_id_uuidlla(unique_tiedostonimi_ensimmainen_toimitussisalto), hae_toimitussisalto_id_uuidlla(unique_tiedostonimi_toinen_toimitussisalto))  
        
        #Oliko toimitussisalto Sievitalon?
        if hae_toimittaja_uuidlla(unique_tiedostonimi_ensimmainen_toimitussisalto) == "Sievitalo":
            logging.info("Tunnistettu Sievitalo toimitussisalto")
            
            toimitussisallon_id = hae_toimitussisalto_id_uuidlla(unique_tiedostonimi_ensimmainen_toimitussisalto)
            logging.info(f"Toimitussisallon ID: {toimitussisallon_id}")
            
            pdf_url = hae_pdf_url_uuidlla(uuid=hae_uuid_toimitussisalto_idlla(toimitussisallon_id))
            logging.info(f"PDF URL: {pdf_url}")
            
            #Sievitalon toimitussisalto puhdistetaan turhista merkeistä ja suodatetaan ikkunat, ulko-ovet, valiovet ja tallennetaaan ne kantaan
            logging.info("Aloitetaan run_sievitalo")
            run_sievitalo(pdf_url, toimitussisallon_id)
            logging.info("run_sievitalo valmis")
            
            # Haetaan käsitellyt tiedot tietokannasta
            logging.info("Haetaan ikkunatiedot tietokannasta")
            ikkunat = hae_toimitussisallon_ikkunat(toimitussisallon_id)
            ulko_ovet = hae_toimitussisallon_ulko_ovet(toimitussisallon_id)
            valiovi_mallit = hae_toimitussisallon_valiovet(toimitussisallon_id)
            
            logging.info(f"Haettu ikkunoita: {len(ikkunat) if ikkunat else 0}")
            logging.info(f"Haettu ulko-ovia: {len(ulko_ovet) if ulko_ovet else 0}")
            logging.info(f"Haettu väliovi-malleja: {len(valiovi_mallit) if valiovi_mallit else 0}")
            
            tulokset["sievitalo"] = {
                "ikkunat": ikkunat,
                "ulko_ovet": ulko_ovet,
                "valiovi_mallit": valiovi_mallit
            }
        
        #Oliko toimitussisalto kastellin?
        if hae_toimittaja_uuidlla(unique_tiedostonimi_toinen_toimitussisalto) == "Kastelli":
            logging.info("Tunnistettu Kastelli toimitussisalto")
            
            toimitussisallon_id = hae_toimitussisalto_id_uuidlla(unique_tiedostonimi_toinen_toimitussisalto)
            logging.info(f"Toimitussisallon ID: {toimitussisallon_id}")
            
            pdf_url = hae_pdf_url_uuidlla(uuid=hae_uuid_toimitussisalto_idlla(toimitussisallon_id))
            logging.info(f"PDF URL: {pdf_url}")
            
            #Kastellin toimitussisalto puhdistetaan turhista merkeistä ja suodatetaan ikkunat, ulko-ovet, valiovet ja tallennetaaan ne kantaan
            logging.info("Aloitetaan run_kastelli")
            run_kastelli(pdf_url, toimitussisallon_id)
            logging.info("run_kastelli valmis")
            
            # Haetaan käsitellyt tiedot tietokannasta
            logging.info("Haetaan ikkunatiedot tietokannasta")
            ikkunat = hae_toimitussisallon_ikkunat(toimitussisallon_id)
            ulko_ovet = hae_toimitussisallon_ulko_ovet(toimitussisallon_id)
            valiovi_mallit = hae_toimitussisallon_valiovet(toimitussisallon_id)
            
            logging.info(f"Haettu ikkunoita: {len(ikkunat) if ikkunat else 0}")
            logging.info(f"Haettu ulko-ovia: {len(ulko_ovet) if ulko_ovet else 0}")
            logging.info(f"Haettu väliovi-malleja: {len(valiovi_mallit) if valiovi_mallit else 0}")
            
            tulokset["kastelli"] = {
                "ikkunat": ikkunat,
                "ulko_ovet": ulko_ovet,
                "valiovi_mallit": valiovi_mallit
            }
        
        #Oliko toimitussisalto ..... 
        #if hae_toimittaja_uuidlla(unique_id_toinen_toimitussisalto) == "Designtalo":
        
            #Designtalon toimitussisalto puhdistetaan turhista merkeistä ja suodatetaan ikkunat, ulko-ovet, valiovet ja tallennetaaan ne kantaan
            #run_designtalo(lue_txt_tiedosto(hae_toimitussisalto_txt_url_uuidlla(unique_id_toinen_toimitussisalto)), hae_toimitussisalto_id_uuidlla(unique_id_toinen_toimitussisalto)) 
    
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
            logging.info(f"Palautetaan AJAX-vastaus: {len(str(tulokset))} tavua")
            logging.info(f"Tulokset: {tulokset}")
            return Response(
                json.dumps(tulokset),
                mimetype='application/json'
            )
        
        # Jos ei ole AJAX-pyyntö, näytä template
        logging.info(f"Palautetaan template-vastaus: {len(str(tulokset))} tavua")
        return render_template("index.html", tulokset=tulokset)

    except Exception as e:
        # Virheiden käsittely
        logging.error(f"Virhe suodata_tiedot funktiossa: {str(e)}")
        logging.error(f"Virhetyyppi: {type(e).__name__}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response(
                json.dumps({'error': str(e), 'type': type(e).__name__}),
                mimetype='application/json'
            )
        return render_template("virhe.html", virheviesti=f"Tietojen käsittelyssä tapahtui virhe: {e}")

    # Oletuspalautus GET-pyynnölle
    return render_template("index.html")


   

@app.route("/", methods=["GET", "POST"])
def index():
    # Näytä index.html-sivu
    return render_template("index.html")

@app.route('/sql_hallinta')
def sql_hallinta():
    return render_template('sql_hallinta.html')

@app.route('/hae_toimitussisallot', methods=['POST'])
def hae_toimitussisallot():
    pvm = request.form.get('pvm')
    # Muunna HTML date-input suomalaiseen muotoon
    pvm_obj = datetime.strptime(pvm, '%Y-%m-%d')
    pvm_suomi = pvm_obj.strftime('%d.%m.%Y')
    tulokset = hae_paivan_toimitussisallot(pvm_suomi)
    return render_template('sql_hallinta.html', tulokset=tulokset)

@app.route('/hae_ulko_ovet', methods=['POST'])
def hae_ulko_ovet():
    pvm = request.form.get('pvm')
    pvm_obj = datetime.strptime(pvm, '%Y-%m-%d')
    pvm_suomi = pvm_obj.strftime('%d.%m.%Y')
    tulokset = hae_paivan_ulko_ovet(pvm_suomi)
    return render_template('sql_hallinta.html', tulokset=tulokset)

@app.route('/hae_valiovet', methods=['POST'])
def hae_valiovet():
    pvm = request.form.get('pvm')
    pvm_obj = datetime.strptime(pvm, '%Y-%m-%d')
    pvm_suomi = pvm_obj.strftime('%d.%m.%Y')
    tulokset = hae_paivan_valiovet(pvm_suomi)
    return render_template('sql_hallinta.html', tulokset=tulokset)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)



