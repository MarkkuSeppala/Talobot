from flask import Flask, request
import os

app = Flask(__name__)

from sie import suorita_lohko2, suorita_lohko3, suorita_lohko4  # Tuodaan lohkot

@app.route("/", methods=["GET", "POST"])
def index():
    pdf_kasitelty = False
    kellonaika = ""

    if request.method == "POST":
        if "pdf" in request.files:
            file = request.files["pdf"]
            if file:
                kellonaika = suorita_lohko2(file)
                lohko2_kasitelty = True
                if file:
                    kellonaika = suorita_lohko3(file)
                    lohko3_kasitelty = True
                    if file:
                        kellonaika = suorita_lohko4(file)
                        lohko4_kasitelty = True
                        if file:
                            kellonaika = suorita_lohko5(file)
                            lohko5_kasitelty = True


    return f'''
    <h2>PDF-käsittely</h2>

    <form method="post" enctype="multipart/form-data">
        <input type="file" name="pdf">
        <input type="submit" value="Lähetä">
    </form>

    {"<p>PDF käsitelty onnistuneesti!</p>" if lohko2_kasitelty else ""}
    {"<p>Käsittelyaika: " + kellonaika + "</p>" if lohko2_kasitelty else ""}
    
    {"<p>PDF käsitelty onnistuneesti!</p>" if lohko3_kasitelty else ""}
    {"<p>Käsittelyaika: " + kellonaika + "</p>" if lohko3_kasitelty else ""}
    '''
    




    #{"""
    #<form method="post">
    #    <input type="submit" name="lohko3" value="Suorita Lohko 3">
    #    </form>
    #""" if pdf_kasitelty else ""}
    
    #{"""
    #<form method="post">
    #    <input type="submit" name="lohko4" value="Suorita Lohko 4">
    #</form>
    #""" if pdf_kasitelty else ""}
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway käyttää PORT-muuttujaa
    app.run(host="0.0.0.0", port=port, debug=True)
