#============== S  I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


from flask import Flask, request, render_template, render_template_string, Response, redirect, url_for, jsonify
import os
import sys

sys.path.append(os.path.abspath("utils"))  # Lisää utils-kansion polku moduulihakemistoksi
sys.path.append(os.path.abspath("api_kyselyt"))

from config_data import (VALIOVITYYPIT_TXT, TOIMITUSSISALTO_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT,  
                        IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNA2_JSON, ULKO_OVI_TIEDOT_2_JSON,
                        TEMP_1_TXT, TOIMITUSSISALTO_TXT, 
                        PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, 
                        PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON,
                        PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT)


from datetime import datetime 
import json
from werkzeug.utils import secure_filename
from generation_config import GENERATION_CONFIG

from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet
from utils.s_tietosissallon_kasittely import jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi, clean_text2

from s_api_kyselyt import api_kysely, api_kysely_kirjoitus_json

from api_run import api_run_sievitalo
                        


def tunnista_toimittaja(teksti):
    """Etsii toimittajan nimen toimitussisällöstä"""
    toimittajat = ["Sievitalo"]
    #toimittajat = ["Sievitalo", "Kastelli", "Designtalo"]
    for nimi in toimittajat:
        if nimi in teksti:
            return nimi
    return None


app = Flask(__name__)


#muuta_tekstiksi
@app.route("/suodata_tiedot", methods=["GET", "POST"])
def suodata_tiedot():
    try:
        # Jos kyseessä on POST-pyyntö, käsittele PDF-tiedosto
        if request.method == "POST" and "pdf" in request.files:
            file = request.files["pdf"]
            
            # Tarkista, että tiedosto on valittu ja sillä on nimi
            if file.filename == '':
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({"error": "Valitse tiedosto"})
                return render_template("index.html", error="Valitse tiedosto")
            
            # Tunnista toimittaja
            teksti = muuta_pdf_tekstiksi(file)
            toimittaja = tunnista_toimittaja(teksti)
            if not toimittaja:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({"error": "Toimittaja ei ole tuettu"})
                return render_template("index.html", error="Toimittaja ei ole tuettu")

            if toimittaja != "Sievitalo":
                return render_template("index.html", error=f"Toimittaja {toimittaja}")
            
            #Muuttaa pdf-tiedoston tekstiksi ja kirjoittaa sen tiedostoon.
            kirjoita_txt_tiedosto(teksti, TOIMITUSSISALTO_TXT)
            #clean_text2 poistaa turhat erikoismerkit, korjaa numeromuodot ja selkeyttää tekstiä. Kirjoittaa puhdistetun tekstin tiedostoon.
            clean_text2(lue_txt_tiedosto(TOIMITUSSISALTO_TXT), PUHDISTETTU_TOIMITUSSISALTO_TXT)
        
        api_run_sievitalo()

        '''
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        api_kysely(PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNATIEDOT_KOKONAISUUDESSA_TXT)
        api_kysely_kirjoitus_json(PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, GENERATION_CONFIG, IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                               %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



        #00000000000000000000000000 IKKUNATIEDOT OMILLE RIVEILLEEN JA KOKO MILLIMETREIKSI 000000000000000000000000000000
        #jokainen ikkuna omalle rivilleen ja koko millimetreiksi
        jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(IKKUNA_JSON, IKKUNA2_JSON)
        #000000000000000000000000000                                                    000000000000000000000000000000
        
        
        
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        api_kysely(PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_TXT, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT)
        api_kysely_kirjoitus_json(PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON, GENERATION_CONFIG, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_2_JSON)
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        
        
        
        #++++++++++++++++++++++++++++++++++++++       ROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT     ++++++++++++++++++++++++++++++++++++++++++++++
        api_kysely(PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT)
        api_kysely(PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT, GENERATION_CONFIG, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVITYYPIT_TXT)
        #++++++++++++++++++++++++++++++++++++++++++++++                                      ++++++++++++++++++++++++++++++++++++++++++++++++++++
        '''






        json_ikkunat = lue_json_tiedosto(IKKUNA2_JSON)
        if json_ikkunat is None or len(json_ikkunat) == 0:
            json_ikkunat = []  # Varmista, että json_ikkunat on vähintään tyhjä lista
            print("Varoitus: Ikkunatietoja ei löytynyt tai tiedosto on tyhjä.")
        
        
        #Lue ulko-ovitiedot
        json_ulko_ovet = lue_json_tiedosto(ULKO_OVI_TIEDOT_2_JSON)
        #print("Luettu json_ulko_ovet:", json_ulko_ovet)
        #print("Tyyppi:", type(json_ulko_ovet))
        
        if json_ulko_ovet is None:
            json_ulko_ovet = []
            print("Varoitus: Ulko-ovitietoja ei löytynyt tai tiedosto on tyhjä.")
        
        # Lue ja käsittele välivovimallit
        valiovi_mallit = lue_txt_tiedosto(VALIOVITYYPIT_TXT)
        print(f"Valiovimallit: {valiovi_mallit}")

        if valiovi_mallit is None or valiovi_mallit.strip() == "":
            valiovi_mallit = {"ovimallit": ["Ei löydetty välivovimalleja"]}
        else:
            try:
                # Muunnetaan pilkulla erotettu teksti listaksi
                valiovi_mallit_lista = [m.strip() for m in valiovi_mallit.split(",")]

                # Tallennetaan JSON-objektiin
                valiovi_mallit = {"ovimallit": valiovi_mallit_lista}

            except Exception as e:
                valiovi_mallit = {"ovimallit": ["Virheellinen JSON-muoto välivovimalleissa"]}
                print(f"Virhe JSON-käsittelyssä: {e}")

        
        
        
        
        # Jos pyyntö on AJAX-pyyntö, palauta JSON-data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            response_data = {
                'ikkunat': json_ikkunat,
                'ulko_ovet': json_ulko_ovet,
                'valiovi_mallit': valiovi_mallit
            }
            #print("Lähetettävä JSON:", response_data)
            
            return Response(
                json.dumps(response_data),
                mimetype='application/json'
            )
        
        # Muussa tapauksessa palauta HTML-sivu
        return render_template("json_tulosteet.html", data1=json_ikkunat, data2=json_ulko_ovet, data3=valiovi_mallit)
    except Exception as e:
        print(f"Virhe suodata_tiedot-funktiossa: {e}")
        
        # Jos pyyntö on AJAX-pyyntö, palauta virhe JSON-muodossa
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response(
                json.dumps({'error': str(e)}),
                mimetype='application/json'
            )
        
        return render_template("virhe.html", virheviesti=f"Tietojen käsittelyssä tapahtui virhe: {e}")

   

@app.route("/", methods=["GET", "POST"])
def index():
    # Näytä index.html-sivu
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


# %%
