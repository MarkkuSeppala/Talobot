#============== S  I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



from flask import Flask, request, render_template_string, Response
import os
from s_toimitussisalto_tekstiksi_ja_clean import muuta_tekstiksi, clean_text, poista_sanat_tekstista
from s_ikkuna_API_kyselyt_tulostus_to_JSON import api_kysely_poimi_ikkunatiedot, api_ryhmittele_valitut_ikkunatiedot_json_muotoon, jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi
from s_valiovet_API_kyselyt_tulostus_to_JSON import api_kysely_poimi_valiovitiedot, api_kysely_anna_valiovimallit
from s_ulko_ovi_API_kyselyt_tulostus_to_JSON import api_kysely_poimi_ulko_ovitiedot, api_ryhmittele_valitut_ulko_ovitiedot_json_muotoon, api_poistaa_valitut_sanat_ulko_ovitiedoista_json_muotoon
from file_handler import lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto
from datetime import datetime 
import json

app = Flask(__name__)


# 🔹 Ulko-ovet. Api-kyselyt ja tulostus selaimeen. 
@app.route("/suodata_ulko_ovitiedot", methods=["GET"])
def suodata_ulko_ovitiedot():
    api_kysely_poimi_ulko_ovitiedot()
    api_ryhmittele_valitut_ulko_ovitiedot_json_muotoon()
    api_poistaa_valitut_sanat_ulko_ovitiedoista_json_muotoon()
    ulko_ovitiedot_str_1 = lue_txt_tiedosto("data/s/ulko_ovi_tiedot_kokonaisuudessa.txt")
    #ulko_ovitiedot_str_1 = json.dumps(ulko_ovitiedot, ensure_ascii=False, indent=4)
    ulko_ovitiedot = lue_json_tiedosto("data/s/ulko_ovi_tiedot.json")
    ulko_ovitiedot_str_2 = json.dumps(ulko_ovitiedot, ensure_ascii=False, indent=4)
    ulko_ovitiedot = lue_json_tiedosto("data/s/ulko_ovi_tiedot_2.json")
    ulko_ovitiedot_str_3 = json.dumps(ulko_ovitiedot, ensure_ascii=False, indent=4)
    return Response(ulko_ovitiedot_str_1+"\n\n\n\n\n\n"+ulko_ovitiedot_str_2+"\n\n\n\n\n\n"+ulko_ovitiedot_str_3, mimetype="application/json")
        

# 🔹 Uusi funktio, jota painike "Suodata väliovitiedot" kutsuu
@app.route("/suodata_valiovitiedot", methods=["GET"])
def suodata_valiovitiedot():
    api_kysely_poimi_valiovitiedot()
    api_kysely_anna_valiovimallit()
    sisalto = lue_txt_tiedosto("data/s/valiovityypit.txt")
    return Response(sisalto, mimetype="text/plain")
    
    

# 🔹 Uusi funktio, jota painike "Suodata ikkunatiedot" kutsuu
@app.route("/suodata_ikkunatiedot", methods=["GET"])
def suodata_ikkunatiedot():
    api_kysely_poimi_ikkunatiedot()
    api_ryhmittele_valitut_ikkunatiedot_json_muotoon()
    jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi()
    #print("Uusi funktio suoritettiin!")
    return "<h3>Ikkunat suodatettu onnistuneesti!</h3><br><a href='/'>Takaisin</a>"

@app.route("/", methods=["GET", "POST"])
def index():
    painike_nayta = False  # Aluksi painiketta ei näytetä

    if request.method == "POST":
        if "pdf" in request.files:
            file = request.files["pdf"]
            if file:
                muuta_tekstiksi(file)
                poista_sanat_tekstista()
                clean_text()
                painike_nayta = True  # Kun funktiot on ajettu, näytetään painike

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="fi">
    <head>
        <meta charset="UTF-8">
        <title>PDF Käsittely</title>
    </head>
    <body>
         <h2>===  S I E V I T A L O  ===<br></h2><br>
        <h4>Valitse aina ensin toimitussisältö<br></h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="pdf">
            <input type="submit" value="Lähetä">
        </form>
        <br><br><br><h4>Valitse sitten haluatko suodattaa ikkunatiedot...</h2>
        {"<button onclick=\"window.location.href='/suodata_ikkunatiedot'\">Suodata ikkunatiedot</button>" if painike_nayta else ""}
        
        <br><br><br><h4>vai välioviteidot...<br></h2><br>
        {"<button onclick=\"window.location.href='/suodata_valiovitiedot'\">Suodata väliovitiedot</button>" if painike_nayta else ""}
        
        <br><br><br><h4>vai ulko-oviteidot...<br></h2><br>
        {"<button onclick=\"window.location.href='/suodata_ulko_ovitiedot'\">Suodata ulko-ovitiedot</button>" if painike_nayta else ""}
        
    </body>
    </html>
    """)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)

