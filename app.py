from flask import Flask, request, render_template, render_template_string, Response, redirect, url_for, jsonify
import os
import sys
import uuid
from werkzeug.utils import secure_filename
import io
from db_config import SessionLocal, Toimitussisallot


from sqlalchemy import create_engine, text

sys.path.append(os.path.abspath("utils"))  # Lisää utils-kansion polku moduulihakemistoksi
sys.path.append(os.path.abspath("api_kyselyt"))

from config_data import (VALIOVITYYPIT_SIEVITALO_JSON, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT,  
                        IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNA2_JSON, ULKO_OVI_TIEDOT_2_JSON,
                        TOIMITUSSISALTO_SIEVITALO_TXT, TOIMITUSSISALTO_KASTELLI_TXT, TOIMITUSSISALTO_TXT,                        
                        PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, 
                        PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON,
                        PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT,
                        PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT, PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, VALIOVITYYPIT_KASTELLI_JSON, TOIMITUSSISALTO_DESIGNTALO_TXT,
                        UPLOAD_FOLDER_DATA)




from datetime import datetime 
import json
from werkzeug.utils import secure_filename
from generation_config import GENERATION_CONFIG

from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet, muuta_pdf_tekstiksi_ilman_tallennusta
from utils.tietosissallon_kasittely import jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi, clean_text2

from run import run_sievitalo, run_kastelli
from factory import get_sievitalo_ikkunat, get_sievitalo_ulko_ovet, get_sievitalo_valiovi_mallit, get_kastelli_ikkunat, get_kastelli_ulko_ovet, get_kastelli_valiovi_mallit



#🔹 Tunnistaa toimittajan nimen toimitussisällöstä
def tunnista_toimittaja(teksti):
    """Etsii toimittajan nimen toimitussisällöstä"""
    #toimittajat = ["Sievitalo", "Kastelli"]
    toimittajat = ["Sievitalo", "Kastelli", "Designtalo"]
    for nimi in toimittajat:
        if nimi in teksti:
            return nimi
    return None


app = Flask(__name__)


os.makedirs(UPLOAD_FOLDER_DATA, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER_DATA

def generate_uuid():
    return str(uuid.uuid4())  # 🔹 Luo yksilöllinen UUID



@app.route("/suodata_tiedot", methods=["GET", "POST"])
def suodata_tiedot():
    try:
        # Jos kyseessä on POST-pyyntö, käsittele PDF-tiedostot
        if request.method == "POST":
            tulokset = {}
        
            # uuttaa koodia:
            # tallentaa pdf -toimitussillön palvelimelle uuid -tunnuksella
            # muuttaa pdf -tiedoston tekstiksi
            # tunnistaa toimittajan
            # käsittelee toimittajan tiedot
            # tallentaa tekstidata tiedostoksi
            # tallentaa tiedot tietokantaan
            
            if "sievitalo_pdf" in request.files:
                file = request.files["sievitalo_pdf"]            
                print(f"🔹 rivi: 86 ")
                # 🔹 Luo UUID-tunniste ja tallenna PDF palvelimelle
                unique_id = generate_uuid()
                pdf_filename = f"{unique_id}.pdf"
                pdf_filepath = os.path.join(UPLOAD_FOLDER_DATA, pdf_filename)

                # 🔹 Lue tiedosto muistiin ennen tallennusta
                file_data = file.read()  # Lue sisältö talteen

                # 🔹 Tallenna tiedosto palvelimelle
                with open(pdf_filepath, "wb") as f:
                    f.write(file_data)  # Kirjoitetaan alkuperäinen tiedosto levylle

                print(f"🔹 Tallennetaan PDF-tiedosto: {pdf_filepath}")
                
                # 🔹 Muunna PDF tekstiksi
                # Muunna PDF tekstiksi ilman tallennusta
                teksti = muuta_pdf_tekstiksi(io.BytesIO(file_data))  # Luo muistissa oleva tiedosto-objekti
                #print(f"🔹 Muunna PDF tekstiksi: {teksti}")

                # 🔹 Tunnista toimittaja
                toimittaja = tunnista_toimittaja(teksti)
                #print(f"🔹 Toimittaja: {toimittaja}")

                # 🔹 Tallennetaan tekstidata tiedostoksi
                txt_filename = f"{unique_id}.txt"
                txt_filepath = os.path.join(UPLOAD_FOLDER_DATA, txt_filename)
                kirjoita_txt_tiedosto(teksti, txt_filepath)
                #print(f"🔹 Tallennetaan tekstidata tiedostoksi 97")
            else:
                tulokset["sievitalo"] = {"error": "Väärä toimittaja"}
            # print(pdf_filepath)
            # print(txt_filepath)

            db = SessionLocal()
            try:
                uusi_toimitussisalto = Toimitussisallot(
                    kayttaja_id=1,
                    uuid=unique_id,
                    pdf_url=pdf_filepath,
                    txt_sisalto=txt_filepath,
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





        '''
            # Käsittele Sievitalon PDF
            if "sievitalo_pdf" in request.files:
                file = request.files["sievitalo_pdf"]
                if file.filename != '':
                    teksti = muuta_pdf_tekstiksi(file)
                    toimittaja = tunnista_toimittaja(teksti)
                    
                    if toimittaja == "Sievitalo":
                        kirjoita_txt_tiedosto(teksti, TOIMITUSSISALTO_SIEVITALO_TXT)
                        
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     run_sievitalo       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        run_sievitalo()
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                        tulokset["sievitalo"] = {
                            "ikkunat": get_sievitalo_ikkunat(),
                            "ulko_ovet": get_sievitalo_ulko_ovet(),
                            "valiovi_mallit": get_sievitalo_valiovi_mallit()
                        }
                    else:
                        tulokset["sievitalo"] = {"error": "Väärä toimittaja"}

            # Käsittele Kastellin PDF
            if "kastelli_pdf" in request.files:
                file = request.files["kastelli_pdf"]
                if file.filename != '':
                    teksti = muuta_pdf_tekstiksi(file)
                    toimittaja = tunnista_toimittaja(teksti)
                    

                    if toimittaja == "Kastelli":
                        kirjoita_txt_tiedosto(teksti, TOIMITUSSISALTO_KASTELLI_TXT)
                        
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     run_kastelli       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        run_kastelli()
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                               
                        tulokset["kastelli"] = {
                            "ikkunat": get_kastelli_ikkunat(),
                            "ulko_ovet": get_kastelli_ulko_ovet(),
                            "valiovi_mallit": get_kastelli_valiovi_mallit()
                        }
                    else:
                        tulokset["kastelli"] = {"error": "Väärä toimittaja"}



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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


# %%
