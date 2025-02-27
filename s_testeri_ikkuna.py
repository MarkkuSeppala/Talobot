#============== S  I E V I T A L O ============#

# Tämä on testeri, joka käyttää s_ikkuna.py -tiedostoa. Tämä lataa PDF-tiedoston, muuntaa sen tekstiksi, poistaa tekstistä tietyt sanat, hakee API:sta ikkunatiedot ja ryhmittelee ne JSON-muotoon.
# Tämä on Flask-sovellus. Eli käyttöliittymä on selaimessa.

#================================================================#
#================================================================#

from flask import Flask, request
import os
import json
import pandas as pd

from datetime import datetime  # Lisätään kellonaika jokaiselle tapahtumalle

app = Flask(__name__)

from s_ikkuna import muuta_tekstiksi, poista_sanat_tekstista, api_kysely_poimi_ikkunatiedot, api_ryhmittele_valitut_ikkunatiedot_json_muotoon, ikkunat_omille_riveille_koon_pyoristys  # Tuodaan lohkot

@app.route("/", methods=["GET", "POST"])
def index():
    pdf_kasitelty = False
    kellonaika = ""
    status_viestit = []  # Lista, johon kerätään jokaisen vaiheen viestit

    if request.method == "POST":
        if "pdf" in request.files:
            file = request.files["pdf"]
            if file:
                kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                muuta_tekstiksi(file)
                status_viestit.append(f"Muuta tekstiksi. Suoritettu - {kellonaika}")

                kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                poista_sanat_tekstista()
                status_viestit.append(f"Poista sanat tekstistä. Suoritettu - {kellonaika}")

                kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                api_kysely_poimi_ikkunatiedot()
                status_viestit.append(f"Poimi ikkunatiedot API:sta. Suoritettu - {kellonaika}")

                kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                api_ryhmittele_valitut_ikkunatiedot_json_muotoon()
                status_viestit.append(f"Ryhmittele ikkunat JSON-muotoon. Suoritettu - {kellonaika}")

                ikkunat_omille_riveille_koon_pyoristys()

                pdf_kasitelty = True
                        
    
    
    #**Luetaan tiedoston sisältö**
    ikkuna_tiedosto = "data/s/ikkuna_json_2.txt"
    if os.path.exists(ikkuna_tiedosto):
        with open(ikkuna_tiedosto, "r", encoding="utf-8") as tiedosto:
            json_data = json.load(tiedosto)  # Lataa JSON-tiedot
            df = pd.DataFrame(json_data)  # Muunna DataFrameksi
            ikkuna_taulukko = df.to_html(classes='table', index=False)  # Muunna HTML-taulukoksi
    else:
        ikkuna_taulukko = "<p style='color: red;'>Virhe: ikkuna_json_2.txt -tiedostoa ei löytynyt.</p>"

    return f'''
    <!DOCTYPE html>
    <html lang="fi">
    <head>
        <meta charset="UTF-8">
        <title>PDF Käsittely</title>
    </head>
    <body>
        <h2>==== S I E V I T A L O ====</h2>
        <h3>pdf-käsittely</h3>

        <form method="post" enctype="multipart/form-data">
            <input type="file" name="pdf">
            <input type="submit" value="Lähetä">
        </form>

        {"<p>PDF käsitelty onnistuneesti!</p>" if pdf_kasitelty else ""}
                
        <h3>Suoritusvaiheet:</h3>
        <ul>
            {"".join(f"<li>{viesti}</li>" for viesti in status_viestit)}
        </ul>

         <h3>Ikkuna JSON -tiedoston sisältö taulukkona:</h3>
        {ikkuna_taulukko}  <!-- Näytetään JSON taulukkona -->

               
    </body>
    </html>
    '''
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway käyttää PORT-muuttujaa
    app.run(host="0.0.0.0", port=port, debug=True)
