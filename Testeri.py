from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Sovellus toimii Railwayssa!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway määrittää portin ympäristömuuttujassa
    app.run(host="0.0.0.0", port=port)  # Kuuntelee kaikista osoitteista




import sys
#sys.path.append("C:/Talobot")  # Varmista, että polku on oikea
from sie import suorita_lohko2, suorita_lohko3, suorita_lohko4  # Tuodaan lohkot


from sie import suorita_lohko2, suorita_lohko3, suorita_lohko4  # Tuodaan myös suorita_lohko4
#testi
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "pdf" in request.files:
            file = request.files["pdf"]
            if file:
                kellonaika = suorita_lohko2(file)  # Lähetetään tiedosto käsittelyyn
                return f'''
                <h2>PDF käsitelty onnistuneesti</h2>
                <p>Käsittelyaika: {kellonaika}</p>
                <br>
                <form method="post">
                    <input type="submit" name="lohko3" value="Suorita Lohko 3">
                </form>
                '''

        if "lohko3" in request.form:  # Tarkistetaan, onko Lohko 3 -nappia painettu
            kellonaika = suorita_lohko3()  # Kutsutaan suorita_lohko3
            return f'''
            <h2>Lohko 3 suoritettu</h2>
            <p>Käsittelyaika: {kellonaika}</p>
            <br>
            <form method="post">
                <input type="submit" name="lohko4" value="Suorita Lohko 4">
            </form>
            '''

        if "lohko4" in request.form:  # Tarkistetaan, onko Lohko 4 -nappia painettu
            kellonaika = suorita_lohko4()  # Kutsutaan suorita_lohko4
            return f"<h2>Lohko 4 suoritettu</h2><p>Käsittelyaika: {kellonaika}</p>"

    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="pdf">
        <input type="submit" value="Lähetä">
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)

#import os
#if __name__ == "__main__":
#    port = int(os.environ.get("PORT", 5000))
#    app.run(host="0.0.0.0", port=port, debug=True)
# testu