from flask import Flask, request
import os

app = Flask(__name__)

from sie import muuta_tekstiksi, poista_sanat_tekstista, api_kysely_poimi_ikkunatiedot  # Tuodaan lohkot

@app.route("/", methods=["GET", "POST"])
def index():
    pdf_kasitelty = False
    kellonaika = ""

    if request.method == "POST":
        if "pdf" in request.files:
            file = request.files["pdf"]
            if file:
                kellonaika = muuta_tekstiksi(file)
                muuta_tekstiksi_kasitelty = True
                if file:
                    kellonaika = poista_sanat_tekstista()
                    poista_sanat_tekstista_kasitelty = True
                    if file:
                        kellonaika = api_kysely_poimi_ikkunatiedot()
                        api_kysely_poimi_ikkunatiedot_kasitelty = True
                        if file:
                            kellonaika = api_ryhmittele_valitut_ikkunatiedot_json_muotoon()
                            api_ryhmittele_valitut_ikkunatiedot_json_muotoon = True
                        
                

    return f'''
    <!DOCTYPE html>
    <html lang="fi">
    <head>
        <meta charset="UTF-8">
        <title>PDF Käsittely</title>
    </head>
    <body>
        <h2>PDF-käsittely</h2>

        <form method="post" enctype="multipart/form-data">
            <input type="file" name="pdf">
            <input type="submit" value="Lähetä">
        </form>

        {"<p>PDF käsitelty onnistuneesti!</p>" if pdf_kasitelty else ""}
        {"<p>Käsittelyaika: " + kellonaika + "</p>" if pdf_kasitelty else ""}
        
        {"""
        <form method="post">
            <input type="submit" name="lohko3" value="Suorita Lohko 3">
        </form>
        """ if pdf_kasitelty else ""}
    </body>
    </html>
    '''
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway käyttää PORT-muuttujaa
    app.run(host="0.0.0.0", port=port, debug=True)
