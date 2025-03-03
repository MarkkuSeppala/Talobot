import io
import os
import re
import fitz  # PyMuPDF
import google.generativeai as genai
import tkinter as tk
from tkinter import filedialog
from datetime import datetime






#======================= D E S I G N T A L O ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#



# **API-kysely. Poimii kaikki ikkunatiedot poistamatta mitään**
def api_kysely_poimi_ikkunatiedot(file):
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")  # Vaihda API-avain
    #tiedostopolku = "data/d/puhdistettu_toimitussisalto.txt"

    generation_config = {
        "temperature": 0.05,
        "top_p": 0.80,
        "top_k": 20,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    system_instruction = """
    Sinä olet asiantunteva avustaja, joka analysoi PDF-tiedostoista muunnettua tekstiä.
    Vastaa selkeästi ja suomeksi. Kerro tulokset tiiviisti ja laske tarkasti.
    Annettu teksti on talotoimittajan tarjoukseen liittyvä toimitussisältö.
    Tehtävänäsi on pomia toimitussisällöstä ikkunatiedot, ei mitään muuta.
    Ikkunat on ryhmitelty tekstiin kokojen mukaan.
    Jokainen ikkunalohko, jossa on yksi tai useampi saman kokoinen ikkuna esitellään erikseen.

    Tässä esimerkki yhdestä ikkunaryhmästä:
    'IKKUNA: Avattava, 3-lasinen, 12, U 1,0 Karmi 170-175mm - Mitoitus: 5,3 5,5 0,2915 m - Määrä: 3 kpl - Sisäpuiteväri: Ikkunan sisäpuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Sisäpuitteen helat valkoiset. Saunan ikkuna aina puunvärinen mänty. - Ulkopuiteväri: Ikkunan ulkopuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Ulkopuitteen sisä- ja ulkopinnat, ulkopuoliset karmiverhouksen alumiinilistat ja ikkunan vesipelti valitun värin mukaisena. - Helat: Valkoinen - Malli: 4 - Tuuletusikkuna: Kyllä - Sijoitus: MH3 MH 2 PH 5,5 --- 5,3 --- TI 
    IKKUNA: Avattava, 3-lasinen, 12, U 1,0 Karmi 170-175mm - Mitoitus: 13,3 5,5 0,7315 m - Määrä: 1 kpl - Sisäpuiteväri: Ikkunan sisäpuiteväri: saunan ikkuna suojakäsitelty mänty Ikkunan sisäpuite ja sisäkarmi mänty väritön suojakäsittely. Pintahelat ja kiintopainikkeet kromin väriset. - Ulkopuiteväri: Ikkunan ulkopuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Ulkopuitteen sisä- ja ulkopinnat, ulkopuoliset karmiverhouksen alumiinilistat ja ikkunan vesipelti valitun värin mukaisena. - Helat: Kromi - Malli: 4 - Tuuletusikkuna: Kyllä - Turvalasi: Karkaistu lasi - Sijoitus: S 5,5 --- 13,3 --- TI - K 
    IKKUNA: Avattava, 3-lasinen, 12, U 1,0 Karmi 170-175mm - Mitoitus: 10,3 13,5 1,3905 m - Määrä: 1 kpl - Sisäpuiteväri: Ikkunan sisäpuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Sisäpuitteen helat valkoiset. Saunan ikkuna aina puunvärinen mänty. - Ulkopuiteväri: Ikkunan ulkopuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Ulkopuitteen sisä- ja ulkopinnat, ulkopuoliset karmiverhouksen alumiinilistat ja ikkunan vesipelti valitun värin mukaisena. - Helat: Valkoinen 13,5 16 17 - Malli: 4 - Sijoitus: KHH --- 10,3 --- 
    IKKUNA: Avattava, 3-lasinen, 12, U 1,0 Karmi 170-175mm - Mitoitus: 15,3 19 2,907 m - Määrä: 2 kpl - Sisäpuiteväri: Ikkunan sisäpuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Sisäpuitteen helat valkoiset. Saunan ikkuna aina puunvärinen mänty. - Ulkopuiteväri: Ikkunan ulkopuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Ulkopuitteen sisä- ja ulkopinnat, ulkopuoliset karmiverhouksen alumiinilistat ja ikkunan vesipelti valitun värin mukaisena. - Helat: Valkoinen - Malli: 4 - Turvalasi: Karkaistu lasi - Sijoitus: OH 19 --- 15,3 --- K 
    IKKUNA: Avattava, 3-lasinen, 12, U 1,0 Karmi 170mm RwCtr max. 44 dB - Mitoitus: 13,3 19,5 2,5935 m - Määrä: 3 kpl - Sisäpuiteväri: Ikkunan sisäpuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Sisäpuitteen helat valkoiset. Saunan ikkuna aina puunvärinen mänty. - Ulkopuiteväri: Ikkunan ulkopuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Ulkopuitteen sisä- ja ulkopinnat, ulkopuoliset karmiverhouksen alumiinilistat ja ikkunan vesipelti valitun värin mukaisena. - Helat: Valkoinen - Malli: 3 - Tuuletusikkuna: Kyllä - Sijoitus: MH1, MH3, MH4 19,5 --- 13,3 --- TI 
    IKKUNA: Avattava, 3-lasinen, 12, U 1,0 Karmi 170-175mm - Mitoitus: 13,3 13,5 1,7955 m - Määrä: 1 kpl - Sisäpuiteväri: Ikkunan sisäpuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Sisäpuitteen helat valkoiset. Saunan ikkuna aina puunvärinen mänty. - Ulkopuiteväri: Ikkunan ulkopuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Ulkopuitteen sisä- ja ulkopinnat, ulkopuoliset karmiverhouksen alumiinilistat ja ikkunan vesipelti valitun värin mukaisena. 13,5 17 17 - Helat: Valkoinen - Malli: 3 - Tuuletusikkuna: Kyllä - Sijoitus: MH2 --- 13,3 --- TI 
    IKKUNA: Avattava, 3-lasinen, 12, U 1,0 Karmi 170mm RwCtr max. 44 dB - Mitoitus: 10,3 13,5 1,3905 m - Määrä: 1 kpl - Sisäpuiteväri: Ikkunan sisäpuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Sisäpuitteen helat valkoiset. Saunan ikkuna aina puunvärinen mänty. - Ulkopuiteväri: Ikkunan ulkopuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Ulkopuitteen sisä- ja ulkopinnat, ulkopuoliset karmiverhouksen alumiinilistat ja ikkunan vesipelti valitun värin mukaisena. - Helat: Valkoinen - Malli: 4 - Tuuletusikkuna: Kyllä - Sijoitus: Keittiö 13,5 --- 10,3 --- TI v
    IKKUNA: Avattava, 3-lasinen, 12, U 1,0 Karmi 170mm RwCtr max. 44 dB - Mitoitus: 15,3 13,5 2,0655 m - Määrä: 1 kpl - Sisäpuiteväri: Ikkunan sisäpuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Sisäpuitteen helat valkoiset. Saunan ikkuna aina puunvärinen mänty. - Ulkopuiteväri: Ikkunan ulkopuiteväri: valkoinen RAL9010 / NCS S0502Y valmistajan vakiosävyn mukaan Ulkopuitteen sisä- ja ulkopinnat, ulkopuoliset karmiverhouksen alumiinilistat ja ikkunan vesipelti valitun värin mukaisena. - Helat: Valkoinen - Malli: 4 - Sijoitus: RT 13,5 --- 15,3 --- 
    
    Tulosta jokainen ikkunaryhmä erikseen erottamalla ne toisistaan kolmella rivinvaihdoilla. Tulosta jokaisesta ikkunaryhmästä kaikki tiedot.
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

    kysymys = f"Tässä on teksti: \n{file}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)

    if response.text:
        ikkuna1 = "data/d/ikkunatiedot_kokonaisuudessa.txt"
        with open(ikkuna1, "w", encoding="utf-8") as tiedosto:
            tiedosto.write(response.text)
    else:
        print("Virhe: response.text on tyhjä")


    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("api_kysely_poimi_ikkunatiedot", kellonaika)
    return kellonaika




#======================= D E S I G N T A L O ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#




# **API-kysely. Ryhmittelee valitut ikkunatiedot JSON-taulukoksi**
def api_ryhmittele_valitut_ikkunatiedot_json_muotoon():
    #import os
    import json
    #import google.generativeai as genai
    import pandas as pd
    from tabulate import tabulate
    from datetime import datetime

    # Konfiguroi Gemini API
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")

    # Määritä tiedostopolku
    tiedostopolku = "data/d/ikkunatiedot_kokonaisuudessa.txt"

    # Määritä generation_config ja system_instruction
    generation_config = {
        "temperature": 0.05,
        "top_p": 0.80,
        "top_k": 20,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    system_instruction = """
    Sinä olet asiantunteva avustaja, joka analysoi annettua tekstiä.
    Vastaa selkeästi ja suomeksi. Kerro tulokset tiiviisti ja laske tarkasti.
    Annettu teksti on talotoimittajan tarjoukseen liittyvä toimitussisältö.
    Tehtävänäsi on poimia toimitussisällöstä ikkunatiedot ja ryhmitellä ne JSON-muotoon.

    Synonyyminisanaohje:
    - Mitoitus (esimerkisi 13,3*19,5) = koko
    - Karkaistu lasi = turvalasi
    - Malli 3 = välikarmi
    - SÄLEKAIHDIN = sälekaihtimet

    Ikkunat on ryhmitelty tekstiin kokojen mukaan.

    Palauta JSON-lista, jossa jokainen kohde on muotoa:
    {
    "koko": "LEVEYSxKORKEUS",
    "kpl": INTEGER,
    "turvalasi": BOOLEAN,
    "välikarmi": BOOLEAN,
    "sälekaihtimet": BOOLEAN
    }
    Palauta pelkkä JSON-lista, älä lisää ylimääräisiä tietoja.

    
    Esimerkki JSON-vastauksesta:
    [
    {"koko": "15x13", "kpl": 3, "turvalasi": true, "välikarmi": true, "sälekaihtimet": false},
    {"koko": "3x19", "kpl": 1, "turvalasi": true, "välikarmi": false, "sälekaihtimet": false}
    ]

    Älä yhdistä eri kokoja tai arvioi tietoja. Palauta täsmälleen ne ikkunat, jotka esiintyvät tekstissä.
    """

    # Alusta Gemini-malli system instructions -kentällä
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

    # Tarkista tiedoston olemassaolo ja lue sisältö
    if os.path.exists(tiedostopolku):
        with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
            sisalto = tiedosto.read()

        kysymys = f"""Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan"""
        
        # Lähetä kysymys Gemini-mallille
        response = model.generate_content(kysymys)

        #print("Gemini API:n vastaus:", response.text)

        
        if response.text:
            try:
                ikkuna_data = json.loads(response.text)
                ikkuna_tiedosto = "data/d/ikkuna_json.txt"
                
                with open(ikkuna_tiedosto, "w", encoding="utf-8") as tiedosto:
                    json.dump(ikkuna_data, tiedosto, ensure_ascii=False, indent=4)
                
                #print("JSON-tiedosto tallennettu:", ikkuna_tiedosto)

            except json.JSONDecodeError:
                print("Virhe JSON-datan käsittelyssä. Tarkista Gemini-vastaus.")
        else:
            print("Virhe: response.text on tyhjä")
    else:
        print("Tiedostoa ei löytynyt. Tarkista polku.")

    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("api_kysely_poimi_ikkunatiedot", kellonaika)
    return kellonaika
    



#======================= D E S I G N T A L O ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#



import json

def jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi():
    output_json = []

    # **Ladataan JSON-tiedot tiedostosta ennen käyttöä**
    with open("data/d/ikkuna_json.txt", "r", encoding="utf-8") as tiedosto:
        json_data = json.load(tiedosto)

    for item in json_data:
        # Muunnetaan koko kokonaisluvuiksi (mm) se muutetaan pilkku pisteeksi, koska kokonaisluku (int) ei hyväksy pilkkua
        leveys, korkeus = map(lambda x: round(float(x.replace(",", ".")) * 100), item["koko"].split("x")) 

        
        # Muunnetaan mitat millimetreiksi
        leveys_mm = leveys
        korkeus_mm = korkeus
        mm_koko = f"{leveys_mm}x{korkeus_mm}"

        for _ in range(item["kpl"]):
            output_json.append({
                "koko": item["koko"],  # Alkuperäinen koko dm
                "mm_koko": mm_koko,  # Muunnettu mm
                "leveys_mm": leveys_mm,  # Tarvitaan lajittelua varten
                "turvalasi": item["turvalasi"],
                "välikarmi": item["välikarmi"],
                "sälekaihtimet": item["sälekaihtimet"]
            })

    # **Lajitellaan lista leveyden mukaan pienimmästä suurimpaan**
    output_json = sorted(output_json, key=lambda x: x["leveys_mm"])

    # Poistetaan lajittelua varten lisätty "leveys_mm" ennen tallennusta
    for item in output_json:
        del item["leveys_mm"]

    # Tallennetaan JSON-tiedostoon
    with open("data/d/ikkuna_json_2.txt", "w", encoding="utf-8") as tiedosto:
        json.dump(output_json, tiedosto, ensure_ascii=False, indent=4)

    print("JSON-tiedosto luotu onnistuneesti!")






#======================= D E S I G N T A L O ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#


# Pyytää txt -tiedoston. Annettava puhdistettu_toimitussisalto.txt. Kutsuu api_kysely_poimi_ikkunatiedot(file), joka tekee API-kyselyn ja tallentaa tuloksen ikkunatiedot_kokonaisuudessa.txt -tiedostoon.

# Kutsuu seuraavaksi api_ryhmittele_valitut_ikkunatiedot_json_muotoon(), joka avaa ikkunatiedot_kokonaisuudessa.txt, metodi ryhmittelee valitut ikkunatiedot JSON-muotoon.
# Tallentaa tuloksen ikkuna_json.txt -tiedostoon.

# Kutsuu seuraavaksi jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi() -metodia, joka avaa ikkuna_json.txt -tiedostoon., asettaa jokaisen ikkunan omalle riville ja muuttaa ikkunamitat millimetreiksi.
# Tallettaa lopuksi ikkuna_json_2.txt -tiedostoon.

# Tämä on Flask-sovellus. Eli käyttöliittymä on selaimessa.

#================================================================#
#================================================================#

from flask import Flask, request
import os
import json
import pandas as pd

from datetime import datetime  # Lisätään kellonaika jokaiselle tapahtumalle

app = Flask(__name__)
print("line 261")

@app.route("/", methods=["GET", "POST"])
def index():
    print("line 265")
    txt_kasitelty = False
    kellonaika = ""
    status_viestit = []  # Lista, johon kerätään jokaisen vaiheen viestit
    print(f"Pyynnön metodi: {request.method}")  # Tulostaa GET tai POST
    if request.method == "POST":
        print("request.files sisältö:", request.files)  # Näyttää, mitä selaimesta saapuu
        if "txt" in request.files:  # Varmistetaan, että lomakkeessa on "txt"
            print("line 270")
            file = request.files["txt"]  # Haetaan tiedosto
            if file and file.filename.endswith(".txt"):  # Tarkistetaan, että se on .txt
                sisalto = file.read().decode("utf-8")  # Luetaan ja dekoodataan UTF-8-muotoon
                
                kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                api_kysely_poimi_ikkunatiedot(sisalto)
                status_viestit.append(f"Poimi ikkunatiedot API:sta. Suoritettu - {kellonaika}")
              
                kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                api_ryhmittele_valitut_ikkunatiedot_json_muotoon()
                status_viestit.append(f"Ryhmittele ikkunat JSON-muotoon. Suoritettu - {kellonaika}")
                print("line 291")
             
                jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi()

                           

                txt_kasitelty = True
                
                        
    #**Luetaan tiedoston sisältö**
    '''
    puhd_toimitussialto = "data/s/puhdistettu_toimitussisalto.txt"
    if os.path.exists(puhd_toimitussialto):
        with open(puhd_toimitussialto, "r", encoding="utf-8") as tiedosto:
            json_data = json.load(tiedosto)  # Lataa JSON-tiedot
            df = pd.DataFrame(json_data)  # Muunna DataFrameksi
            ikkuna_taulukko = df.to_html(classes='table', index=False)  # Muunna HTML-taulukoksi
    else:
        ikkuna_taulukko = "<p style='color: red;'>Virhe: ikkuna_json.txt -tiedostoa ei löytynyt.</p>"
    '''
    return f'''
    <!DOCTYPE html>
    <html lang="fi">
    <head>
        <meta charset="UTF-8">
        <title>PDF Käsittely</title>
    </head>
    <body>
         <h2>=== D E S I G N T A L O ===</h2><br>
         <h4>Tähän saa syöttää vain tämän Sievitalon tiedoston:<br>puhdistettu_toimitussisalto.txt<br><br>
         Tuloksen skripti tallentaa tähän Sievitalon tiedostoon:<br>ikkuna_json_2.txt</h4>

        <form method="post" enctype="multipart/form-data">
            <input type="file" name="txt">
            <input type="submit" value="Lähetä">
        </form>

        {"<p>PDF käsitelty onnistuneesti!</p>" if txt_kasitelty else ""}
                
        <h3>Suoritusvaiheet:</h3>
        <ul>
            {"".join(f"<li>{viesti}</li>" for viesti in status_viestit)}
        </ul>

        

               
    </body>
    </html>
    '''
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway käyttää PORT-muuttujaa
    app.run(host="0.0.0.0", port=port, debug=True)
