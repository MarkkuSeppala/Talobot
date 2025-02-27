#================================================================#
#==========Y H D I S T E T Ä Ä N   I K K U N A T   Y H T E E N==========#
#================================================================#

from flask import Flask, request, render_template_string
import os
import json
import pandas as pd
from datetime import datetime
from yhdistetaan_ikkunat import yhdista_ikkunat

app = Flask(__name__)

# **Muuntaa True/False arvot symboleiksi**
def muunna_symboliksi(value):
    if value is True:
        return "✅"
    elif value is False:
        return "❌"
    return value  # Palauttaa muun datan muuttamatta

@app.route("/", methods=["GET", "POST"])
def index():
    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_viestit = []  # Lista, johon kerätään suoritusvaiheet
    sievitalo_tiedosto = None
    kastelli_tiedosto = None
    output_tiedosto = "C:/Talobot/data/yhd/ikkunat_yhdessa_json.txt"

    if request.method == "POST":
        if "sievitalo_json" in request.files and "kastelli_json" in request.files:
            sievitalo_file = request.files["sievitalo_json"]
            kastelli_file = request.files["kastelli_json"]
            
            if sievitalo_file and kastelli_file:
                # Tallennetaan ladatut tiedostot väliaikaiseen kansioon
                sievitalo_tiedosto = os.path.join("data/s", sievitalo_file.filename)
                kastelli_tiedosto = os.path.join("data/k", kastelli_file.filename)

                sievitalo_file.save(sievitalo_tiedosto)
                kastelli_file.save(kastelli_tiedosto)

                status_viestit.append(f"Tiedostot ladattu onnistuneesti - {kellonaika}")
                
                # Suoritetaan yhdistäminen
                yhdista_ikkunat(sievitalo_tiedosto, kastelli_tiedosto, output_tiedosto)
                status_viestit.append(f"Ikkunat yhdistetty - {kellonaika}")

    # **Luetaan tulostiedosto ja muutetaan taulukoksi**
    if os.path.exists(output_tiedosto):
        with open(output_tiedosto, "r", encoding="utf-8") as tiedosto:
            json_data = json.load(tiedosto)
            
            # **Muunnetaan True/False arvot symboleiksi**
            for item in json_data:
                for key in item.keys():
                    item[key] = muunna_symboliksi(item[key])

            df = pd.DataFrame(json_data)
            ikkuna_taulukko = df.to_html(classes="table", index=False, escape=False)  # `escape=False` sallii HTML-symbolit
    else:
        ikkuna_taulukko = "<p style='color: red;'>Virhe: ikkunat_yhdessa_json.txt -tiedostoa ei löytynyt.</p>"

    # **HTML-pohja**
    html_template = """
    <!DOCTYPE html>
    <html lang="fi">
    <head>
        <meta charset="UTF-8">
        <title>Yhdistetään ikkunat</title>
    </head>
    <body>
        <h2>==== YHDISTETÄÄN IKKUNAT ====</h2>
        <h3>Lataa Sievitalon ja Kastellin JSON-tiedostot</h3>
        <form method="post" enctype="multipart/form-data">
            <label for="sievitalo_json">Sievitalo JSON:</label>
            <input type="file" name="sievitalo_json" required><br><br>
            
            <label for="kastelli_json">Kastelli JSON:</label>
            <input type="file" name="kastelli_json" required><br><br>
            
            <input type="submit" value="Yhdistä ikkunat">
        </form>

        <h3>Suoritusvaiheet:</h3>
        <ul>
            {% for viesti in status_viestit %}
                <li>{{ viesti }}</li>
            {% endfor %}
        </ul>

        <h3>Yhdistetyt ikkunat taulukkona:</h3>
        {{ ikkuna_taulukko|safe }}  <!-- Näytetään JSON taulukkona -->
    </body>
    </html>
    """

    return render_template_string(html_template, status_viestit=status_viestit, ikkuna_taulukko=ikkuna_taulukko)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway käyttää PORT-muuttujaa
    app.run(host="0.0.0.0", port=port, debug=True)
