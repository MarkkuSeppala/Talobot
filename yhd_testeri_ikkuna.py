from flask import Flask, request, render_template_string, make_response
import os
import json
import pandas as pd
from datetime import datetime
from werkzeug.utils import secure_filename
from yhdistetaan_ikkunat import yhdista_ikkunat, laske_ikkunatiedot

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
    
    # **Välimuistin estämiseksi lisätään timestamp**
    timestamp = int(datetime.timestamp(datetime.now()))

    status_viestit = []  # Lista, johon kerätään suoritusvaiheet
    output_tiedosto = "data/yhd/ikkunat_yhdessa_json.txt"
    toinen_tiedosto = "data/yhd/ikkunatiedot_yhdella_rivilla_json.txt"

    if request.method == "POST":
        if "sievitalo_json" in request.files and "kastelli_json" in request.files:
            sievitalo_file = request.files["sievitalo_json"]
            kastelli_file = request.files["kastelli_json"]

            if sievitalo_file and kastelli_file:
                try:
                    os.makedirs("data/s", exist_ok=True)
                    os.makedirs("data/k", exist_ok=True)

                    sievitalo_filename = secure_filename(sievitalo_file.filename)
                    kastelli_filename = secure_filename(kastelli_file.filename)

                    sievitalo_tiedosto = os.path.join("data/s", sievitalo_filename)
                    kastelli_tiedosto = os.path.join("data/k", kastelli_filename)

                    sievitalo_file.save(sievitalo_tiedosto)
                    kastelli_file.save(kastelli_tiedosto)

                    status_viestit.append(f"Tiedostot ladattu onnistuneesti - {kellonaika}")

                    yhdista_ikkunat(sievitalo_tiedosto, kastelli_tiedosto, output_tiedosto)
                    status_viestit.append(f"Ikkunat yhdistetty - {kellonaika}")

                    laske_ikkunatiedot("data/yhd/ikkunat_yhdessa_json.txt", "data/yhd/ikkunatiedot_yhdella_rivilla_json.txt")

                except Exception as e:
                    status_viestit.append(f"Virhe tiedostojen tallennuksessa: {str(e)}")

    # **Luetaan ensimmäinen taulukko**
    try:
        with open(output_tiedosto, "r", encoding="utf-8") as tiedosto:
            json_data = json.load(tiedosto)

        for item in json_data:
            for key in item.keys():
                item[key] = muunna_symboliksi(item[key])

        df1 = pd.DataFrame(json_data)
        ikkuna_taulukko = df1.to_html(classes="table", index=False, escape=False)

    except (json.JSONDecodeError, FileNotFoundError):
        ikkuna_taulukko = "<p style='color: red;'>Virhe: ikkunat_yhdessa_json.txt -tiedostoa ei löytynyt tai se on tyhjä.</p>"

    # **Luetaan toinen taulukko**
    try:
        with open(toinen_tiedosto, "r", encoding="utf-8") as tiedosto:
            toinen_json_data = json.load(tiedosto)

        df2 = pd.DataFrame([toinen_json_data])  # JSON on yksirivinen, tehdään siitä DataFrame
        toinen_taulukko = df2.to_html(classes="table", index=False, escape=False)

    except (json.JSONDecodeError, FileNotFoundError):
        toinen_taulukko = "<p style='color: red;'>Virhe: ikkunatiedot_yhdella_rivilla_json.txt -tiedostoa ei löytynyt tai se on tyhjä.</p>"

    # **HTML-pohja**
    html_template = f"""
    <!DOCTYPE html>
    <html lang="fi">
    <head>
        <meta charset="UTF-8">
        <title>Yhdistetään ikkunat - {timestamp}</title>

        <script>
            window.onload = function() {{
                document.querySelector("form").addEventListener("submit", function() {{
                    setTimeout(function() {{
                        window.location.href = window.location.href + "?nocache=" + new Date().getTime();
                    }}, 1000);
                }});
            }};
        </script>
    </head>
    <body>
        <h2>==== YHDISTETÄÄN IKKUNAT ====</h2>
        <h3>Lataa Sievitalon ja Kastellin JSON-tiedostot</h3>
        <form method="post" enctype="multipart/form-data">
            <label for="sievitalo_json">Sievitalo JSON -tiedosto:</label>
            <input type="file" name="sievitalo_json" required><br><br>
            
            <label for="kastelli_json">Kastelli JSON -tiedosto:</label>
            <input type="file" name="kastelli_json" required><br><br>
            
            <input type="submit" value="Yhdistä ikkunat">
        </form>

        <h3>Suoritusvaiheet:</h3>
        <ul>
            {"".join(f"<li>{viesti}</li>" for viesti in status_viestit)}
        </ul>

        <h3>Yhdistetyt ikkunat taulukkona:</h3>
        {ikkuna_taulukko}

        <h3>Ikkunatiedot yhdellä rivillä:</h3>
        {toinen_taulukko}
    </body>
    </html>
    """

    # **Poista välimuisti**
    response = make_response(html_template)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response  # ✅ Palautetaan vain yksi response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
