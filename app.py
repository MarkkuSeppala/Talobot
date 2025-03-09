#============== S  I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


from flask import Flask, request, render_template, render_template_string, Response, redirect, url_for, jsonify
import os
import sys

sys.path.append(os.path.abspath("utils"))  # Lisää utils-kansion polku moduulihakemistoksi
sys.path.append(os.path.abspath("api_kyselyt"))

from config_data import VALIOVITYYPIT_TXT, TOIMITUSSISALTO_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT
from config_data import IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNA2_JSON, ULKO_OVI_TIEDOT_2_JSON, ULKO_OVI_TIEDOT_JSON, TEMP_1_TXT, TOIMITUSSISALTO_TXT 


from datetime import datetime 
import json
from werkzeug.utils import secure_filename

from file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet
from s_tietosissallon_kasittely import jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi, clean_text2

from s_api_kyselyt import (api_kysely_poimi_ikkunatiedot, api_ryhmittele_valitut_ikkunatiedot_json_muotoon, 
                           api_kysely_poimi_ulko_ovitiedot, api_ryhmittele_valitut_ulko_ovitiedot_json_muotoon, 
                           api_poistaa_valitut_sanat_ulko_ovitiedoista_json_muotoon,
                           api_kysely_poimi_valiovitiedot, api_kysely_anna_valiovimallit)




api_kysely_poimi_ikkunatiedot(PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNATIEDOT_KOKONAISUUDESSA_TXT)



def tunnista_toimittaja(teksti):
    """Etsii toimittajan nimen toimitussisällöstä"""
    toimittajat = ["Sievitalo"]
    #toimittajat = ["Sievitalo", "Kastelli", "Designtalo"]
    for nimi in toimittajat:
        if nimi in teksti:
            return nimi
    return None

#tiedostopolut = {"Sievitalo": "data\\sievitalo\\toimitussisallot", "Kastelli": "data\\kastelli\\toimitussisallot", "Designtalo": "data\\designtalo\\toimitussisallot"}

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
                    return jsonify({"error": "Toimittajaa ei tunnistettu"})
                return render_template("index.html", error="Toimittajaa ei tunnistettu")

            if toimittaja != "Sievitalo":
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({"error": f"Toimittaja {toimittaja} ei ole tuettu"})
                return render_template("index.html", error=f"Toimittaja {toimittaja} ei ole tuettu")
            
            # Käsittele Sievitalo-toimittajan tiedosto
            kirjoita_txt_tiedosto(teksti, TOIMITUSSISALTO_TXT)
            clean_text2(lue_txt_tiedosto(TOIMITUSSISALTO_TXT), PUHDISTETTU_TOIMITUSSISALTO_TXT)
        
        # API-kyselyt
        api_kysely_poimi_ikkunatiedot(PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNATIEDOT_KOKONAISUUDESSA_TXT)
        api_ryhmittele_valitut_ikkunatiedot_json_muotoon(IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON)
        jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(IKKUNA_JSON, IKKUNA2_JSON)
        
        # API-ulko-ovikyselyt
        api_kysely_poimi_ulko_ovitiedot(PUHDISTETTU_TOIMITUSSISALTO_TXT, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT)
        api_ryhmittele_valitut_ulko_ovitiedot_json_muotoon(ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_JSON)
        api_poistaa_valitut_sanat_ulko_ovitiedoista_json_muotoon(ULKO_OVI_TIEDOT_JSON, ULKO_OVI_TIEDOT_2_JSON)

        # API-valiovikyselyt
        api_kysely_poimi_valiovitiedot(PUHDISTETTU_TOIMITUSSISALTO_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT) 
        api_kysely_anna_valiovimallit(VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVITYYPIT_TXT)

        # Lue tiedostot
        json_ikkunat = lue_json_tiedosto(IKKUNA2_JSON)
        if json_ikkunat is None or len(json_ikkunat) == 0:
            json_ikkunat = []  # Varmista, että json_ikkunat on vähintään tyhjä lista
            print("Varoitus: Ikkunatietoja ei löytynyt tai tiedosto on tyhjä.")
        
        json_ulko_ovet = lue_json_tiedosto(ULKO_OVI_TIEDOT_2_JSON)
        if json_ulko_ovet is None:
            json_ulko_ovet = []
            print("Varoitus: Ulko-ovitietoja ei löytynyt tai tiedosto on tyhjä.")
        json_ulko_ovet_normalisoitu = normalisoi_ulko_ovet(json_ulko_ovet)
            
        # Lue ja käsittele välivovimallit
        valiovi_mallit = lue_txt_tiedosto(VALIOVITYYPIT_TXT)
        if valiovi_mallit is None or valiovi_mallit.strip() == "":
            valiovi_mallit = {"ovimallit": ["Ei löydetty välivovimalleja"]}
        else:
            try:
                valiovi_mallit = json.loads(valiovi_mallit)  # Muutetaan JSON:ksi
            except json.JSONDecodeError:
                valiovi_mallit = {"ovimallit": ["Virheellinen JSON-muoto välivovimalleissa"]}

        # Jos pyyntö on AJAX-pyyntö, palauta JSON-data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response(
                json.dumps({
                    'ikkunat': json_ikkunat,
                    'ulko_ovet': json_ulko_ovet_normalisoitu,
                    'valiovi_mallit': valiovi_mallit
                }),
                mimetype='application/json'
            )
        
        # Muussa tapauksessa palauta HTML-sivu
        return render_template("json_tulosteet.html", data1=json_ikkunat, data2=json_ulko_ovet_normalisoitu, data3=valiovi_mallit)
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

