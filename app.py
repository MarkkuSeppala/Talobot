#============== S  I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



from flask import Flask, request, render_template_string, Response
from flask import Flask, request, render_template, render_template_string, Response
import os
from s_toimitussisalto_tekstiksi_ja_clean import muuta_tekstiksi, clean_text2, poista_sanat_tekstista
from file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet
from datetime import datetime 
import json
from werkzeug.utils import secure_filename

from s_ikkuna_API_kyselyt_tulostus_to_JSON import api_kysely_poimi_ikkunatiedot, api_ryhmittele_valitut_ikkunatiedot_json_muotoon, jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi
from s_ulko_ovi_API_kyselyt_tulostus_to_JSON import api_kysely_poimi_ulko_ovitiedot, api_ryhmittele_valitut_ulko_ovitiedot_json_muotoon, api_poistaa_valitut_sanat_ulko_ovitiedoista_json_muotoon
from s_valiovet_API_kyselyt_tulostus_to_JSON import api_kysely_poimi_valiovitiedot, api_kysely_anna_valiovimallit


def tunnista_toimittaja(teksti):
    """Etsii toimittajan nimen toimitussisällöstä"""
    toimittajat = ["Sievitalo"]
    #toimittajat = ["Sievitalo", "Kastelli", "Designtalo"]
    for nimi in toimittajat:
        if nimi in teksti:
            return nimi
    return None

tiedostopolut = {"Sievitalo": "data\\sievitalo\\toimitussisallot", "Kastelli": "data\\kastelli\\toimitussisallot", "Designtalo": "data\\designtalo\\toimitussisallot"}

app = Flask(__name__)



@app.route("/suodata_tiedot", methods=["GET"])
def suodata_tiedot():
    
    #api-ikkunakyselyt
    api_kysely_poimi_ikkunatiedot()
    api_ryhmittele_valitut_ikkunatiedot_json_muotoon()
    jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi()
    
    #api-ulko-ovikyselyt
    api_kysely_poimi_ulko_ovitiedot()
    api_ryhmittele_valitut_ulko_ovitiedot_json_muotoon()
    api_poistaa_valitut_sanat_ulko_ovitiedoista_json_muotoon()

    api_kysely_poimi_valiovitiedot()
    api_kysely_anna_valiovimallit()


    json_ikkunat = lue_json_tiedosto("data\\s\\ikkuna2.json")
    
    
    json_ulko_ovet = lue_json_tiedosto("data\\s\\ulko_ovi_tiedot_2.json")
    json_ulko_ovet_normalisoitu = normalisoi_ulko_ovet(json_ulko_ovet)
        
    
   # Lue ja käsittele välivovimallit
    valiovi_mallit = lue_txt_tiedosto("data/s/valiovityypit.txt")
    if valiovi_mallit is None:
        valiovi_mallit = {"ovimallit": ["Ei löydetty välivovimalleja"]}
    else:
        valiovi_mallit = json.loads(valiovi_mallit)  # Muutetaan JSON:ksi

    return render_template("json_tulosteet.html", data1=json_ikkunat, data2=json_ulko_ovet_normalisoitu, data3=valiovi_mallit)

   

@app.route("/", methods=["GET", "POST"])
def index():
    painike_nayta = False  # Aluksi painiketta ei näytetä

    if request.method == "POST":
        if "pdf" in request.files:
            file = request.files["pdf"]
            
            #Tunnista toimittaja
            teksti = muuta_pdf_tekstiksi(file)
            toimittaja = tunnista_toimittaja(teksti)
            if not toimittaja:
                return render_template("toimittajaa_ei_tunnisteta.html")    
                #return f"Ei voitu tunnistaa toimittajaa tiedostosta"

            if toimittaja == "Sievitalo":
                polku = tiedostopolut.get("Sievitalo")
                tallenna_pdf_tiedosto(file, polku)
                clean_text2(teksti)
                painike_nayta = True
                return render_template("sievitalo.html", painike_nayta=painike_nayta)
            
            
            
            
            
            
            
            
            if toimittaja == "Kastelli":
                polku = tiedostopolut.get("Kastelli")
                print(polku)
                tallenna_pdf_tiedosto(file, polku)
            if toimittaja == "Designtalo":
                polku = tiedostopolut.get("Designtalo")
                print(polku)
                tallenna_pdf_tiedosto(file, polku)
            
            
            #tallenna_pdf_tiedosto(file, ="data/s")
            
            if file:
                #muuta_tekstiksi(file)
                #poista_sanat_tekstista()
                #clean_text2()
                painike_nayta = True  # Kun funktiot on ajettu, näytetään painike

    return render_template("index.html")
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)

