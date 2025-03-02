import io
import os
import re
import fitz  # PyMuPDF
import google.generativeai as genai
import tkinter as tk
from tkinter import filedialog
from datetime import datetime



##======================= K A S T E L L I ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#



# **API-kysely. Poimii kaikki ikkunatiedot poistamatta mitään**
def api_kysely_poimi_ikkunatiedot(file):
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")  # Vaihda API-avain
    #tiedostopolku = "data/k/puhdistettu_toimitussisalto.txt"

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
    'Nro: 10, 20 2 Kpl Tyyppi: A /14.4x25 Karmimitat:1430x2490 KARMITYYPPI: MEKL 3-kertainen kiinteä, karmisyvyys 170 mm SISÄPUITTEEN LASITUS: 3-kertainen eristyslasielementti, U1,0, sisin ja uloin lasi karkaistu 6 mm ULKOPUITTEEN LASITUS: PUUOSIEN PINTAKÄSITTELY: maalattu valkoinen ALUMIINIOSIEN VÄRI: valkoinen RAL 9010 KARMI-/PUITEMATER: karmin ulkopuoli alumiinia HELOITUKSEN VÄRI: SÄLEKAIHDIN: integroitu, matta valkoinen P2 tunnus S HUONETILA: OLOKEITTIÖ, OLOKEITTIÖ HUOMAUTUS: HOX: Mahdolliset sälekaihtimet tulevat kiinteisiin ikkunoihin pinta-asennettuina.
    Nro: 30 1 Kpl Tyyppi: A /14.4x25 Karmimitat:1430x2490 KARMITYYPPI: MEKL 3-kertainen kiinteä, karmisyvyys 170 mm SISÄPUITTEEN LASITUS: 3-kertainen eristyslasielementti, U1,0, sisin ja uloin lasi karkaistu 6 mm ULKOPUITTEEN LASITUS: PUUOSIEN PINTAKÄSITTELY: maalattu valkoinen ALUMIINIOSIEN VÄRI: valkoinen RAL 9010 KARMI-/PUITEMATER: karmin ulkopuoli alumiinia HELOITUKSEN VÄRI: SÄLEKAIHDIN: integroitu, matta valkoinen P2 tunnus S RAITISILMAVENTTIILI: BIOBE VS-B60, yläkarmiin asennettuna, sis. suodattimen HUONETILA: OLOKEITTIÖ HUOMAUTUS: HOX: Mahdolliset sälekaihtimet tulevat kiinteisiin ikkunoihin pinta-asennettuina. 
    Nro: 40 1 Kpl oik Tyyppi: A /11.4x20 Karmimitat:1130x1990 KARMITYYPPI: MSEL, avattava, karmisyvyys 170 mm SISÄPUITTEEN LASITUS: 2-kertainen eristyslasielementti, U1,0, sisin lasi karkaistu 4 mm ULKOPUITTEEN LASITUS: Karkaistu lasi 4 mm PUUOSIEN PINTAKÄSITTELY: maalattu valkoinen ALUMIINIOSIEN VÄRI: valkoinen RAL 9010 KARMI-/PUITEMATER: ulkopuite ja karmin ulkopuoli alumiinia HELOITUKSEN VÄRI: valkoinen SÄLEKAIHDIN: integroitu, matta valkoinen P2 tunnus S HUONETILA: OLOKEITTIÖ IKKUNALUETTELO Sivu:2 Tarjousnro/versio: 14.09.2021386400/A 
    Nro: 50 1 Kpl ala Tyyppi: AT /11.4x5.4 Karmimitat:1130x530 KARMITYYPPI: MSEL, avattava, karmisyvyys 170 mm SISÄPUITTEEN LASITUS: 2-kertainen eristyslasielementti, U1,0 ULKOPUITTEEN LASITUS: 1-kertainen tasolasi PUUOSIEN PINTAKÄSITTELY: maalattu valkoinen ALUMIINIOSIEN VÄRI: valkoinen RAL 9010 KARMI-/PUITEMATER: ulkopuite ja karmin ulkopuoli alumiinia HELOITUKSEN VÄRI: valkoinen SÄLEKAIHDIN: integroitu, matta valkoinen P2 tunnus S TUULETUSIKKUNA: tuuletusikkunaheloitus tunnus T LISÄTARVIKE: Alasaranoituun ikkunaan 2 kpl Abloy WF 881 lisäaukipitolaitteita. HUONETILA: PE 
    Nro: 60 1 Kpl oik Tyyppi: AT /8.4x5.4 Karmimitat:830x530 KARMITYYPPI: MSEL, avattava, karmisyvyys 170 mm SISÄPUITTEEN LASITUS: 2-kertainen eristyslasielementti, U1,0 ULKOPUITTEEN LASITUS: 1-kertainen tasolasi PUUOSIEN PINTAKÄSITTELY: väritön suojakäsittely ALUMIINIOSIEN VÄRI: valkoinen RAL 9010 KARMI-/PUITEMATER: ulkopuite ja karmin ulkopuoli alumiinia HELOITUKSEN VÄRI: kromattu SÄLEKAIHDIN: integroitu, matta valkoinen P2 tunnus S TUULETUSIKKUNA: tuuletusikkunaheloitus tunnus T HUONETILA: SAUNA HUOMAUTUS: HOX: Mahdolliselle saunan ikkunan sälekaihtimelle ei myönnetä takuuta. 
    Nro: 70 1 Kpl vas Tyyppi: BA6 /11.4x18 Karmimitat:1130x1790 KARMITYYPPI: MSEL, avattava, karmisyvyys 170 mm SISÄPUITTEEN LASITUS: 2-kertainen eristyslasielementti, U1,0, sisin lasi karkaistu 4 mm ULKOPUITTEEN LASITUS: 1-kertainen tasolasi PUUOSIEN PINTAKÄSITTELY: maalattu valkoinen ALUMIINIOSIEN VÄRI: valkoinen RAL 9010 KARMI-/PUITEMATER: ulkopuite ja karmin ulkopuoli alumiinia HELOITUKSEN VÄRI: valkoinen SÄLEKAIHDIN: integroitu, matta valkoinen P2 tunnus S TUULETUSIKKUNA: tuuletusikkunaheloitus tunnus T LISÄTARVIKE: Varatieheloitus aukossa 2 ja tuuletusheloitus aukossa 1 HUONETILA: MH 1 
    Nro: 80, 90 2 Kpl oik Tyyppi: BA6 /11.4x18 Karmimitat:1130x1790 KARMITYYPPI: MSEL, avattava, karmisyvyys 170 mm SISÄPUITTEEN LASITUS: 2-kertainen eristyslasielementti, U1,0, sisin lasi karkaistu 4 mm ULKOPUITTEEN LASITUS: 1-kertainen tasolasi PUUOSIEN PINTAKÄSITTELY: maalattu valkoinen ALUMIINIOSIEN VÄRI: valkoinen RAL 9010 KARMI-/PUITEMATER: ulkopuite ja karmin ulkopuoli alumiinia HELOITUKSEN VÄRI: valkoinen SÄLEKAIHDIN: integroitu, matta valkoinen P2 tunnus S TUULETUSIKKUNA: tuuletusikkunaheloitus tunnus T LISÄTARVIKE: Varatieheloitus aukossa 2 ja tuuletusheloitus aukossa 1 HUONETILA: MH 2, MH 3 IKKUNALUETTELO Sivu:3 Tarjousnro/versio: 14.09.2021386400/A 
    Nro: 100, 110 2 Kpl Tyyppi: A /11.4x25 Karmimitat:1130x2490 KARMITYYPPI: MEKL 3-kertainen kiinteä, karmisyvyys 170 mm SISÄPUITTEEN LASITUS: 3-kertainen eristyslasielementti, U1,0, sisin ja uloin lasi karkaistu 6 mm ULKOPUITTEEN LASITUS: PUUOSIEN PINTAKÄSITTELY: maalattu valkoinen ALUMIINIOSIEN VÄRI: valkoinen RAL 9010 KARMI-/PUITEMATER: karmin ulkopuoli alumiinia HELOITUKSEN VÄRI: SÄLEKAIHDIN: integroitu, matta valkoinen P2 tunnus S HUONETILA: OLOKEITTIÖ, OLOKEITTIÖ HUOMAUTUS: HOX: Mahdolliset sälekaihtimet tulevat kiinteisiin ikkunoihin pinta-asennettuina.'
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
        ikkuna1 = "data/k/ikkunatiedot_kokonaisuudessa.txt"
        with open(ikkuna1, "w", encoding="utf-8") as tiedosto:
            tiedosto.write(response.text)
            print("Tiedosto tallennettu:", ikkuna1)
    else:
        print("Virhe: response.text on tyhjä")

        
    
    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("api_kysely_poimi_ikkunatiedot", kellonaika)
    return kellonaika




##======================= K A S T E L L I ==========================#
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
    tiedostopolku = "data/k/ikkunatiedot_kokonaisuudessa.txt"

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
    - Karmimitat = koko
    - karkaistu = turvalasi
    - Tyyppi: B = välikarmi
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

              
        if response.text:
            try:
                ikkuna_data = json.loads(response.text)
                ikkuna_tiedosto = "data/k/ikkuna_json.txt"
                
                with open(ikkuna_tiedosto, "w", encoding="utf-8") as tiedosto:
                    json.dump(ikkuna_data, tiedosto, ensure_ascii=False, indent=4)
                
               
            except json.JSONDecodeError:
                print("Virhe JSON-datan käsittelyssä. Tarkista Gemini-vastaus.")
        else:
            print("Virhe: response.text on tyhjä")
    else:
        print("Tiedostoa ei löytynyt. Tarkista polku.")

    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("api_kysely_poimi_ikkunatiedot", kellonaika)
    return kellonaika
    



##======================= K A S T E L L I ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#





def jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi():
    import json
    #import math


    # **Ladataan JSON-tiedot tiedostosta ennen käyttöä**
    with open("data/k/ikkuna_json.txt", "r", encoding="utf-8") as tiedosto:
        json_data = json.load(tiedosto)

    '''
    ikkuna_tiedosto = "data/k/ikkuna_json.txt"
    json_data = []  # Alustetaan tyhjä lista

    # Tarkistetaan, onko tiedosto olemassa, ja ladataan JSON-data
    if os.path.exists(ikkuna_tiedosto):
        try:
            with open(ikkuna_tiedosto, "r", encoding="utf-8") as tiedosto:
                json_data = json.load(tiedosto)  # Lataa JSON-tiedot
        except json.JSONDecodeError:
            print(f"Virhe: Tiedosto {ikkuna_tiedosto} ei sisällä validia JSON-dataa.")
            return []
        try:
            with open(ikkuna_tiedosto, "r", encoding="utf-8") as tiedosto:
                json_data = json.load(tiedosto)  # Lataa JSON-tiedot
        except json.JSONDecodeError:
            print(f"Virhe: Tiedosto {ikkuna_tiedosto} ei sisällä validia JSON-dataa.")
            return []
    '''
    
    output_json = []

    for item in json_data:
        leveys, korkeus = map(int, item["koko"].split("x"))  # Muutetaan mitat kokonaisluvuiksi
        pyoristetty_leveys = round(leveys / 100) * 100  # Pyöristetään lähimpään 100 mm
        pyoristetty_korkeus = round(korkeus / 100) * 100  # Pyöristetään lähimpään 100 mm
        pyoristetty_koko = f"{pyoristetty_leveys}x{pyoristetty_korkeus}"

        for _ in range(item["kpl"]):
            output_json.append({
                "koko": item["koko"],
                "pyoristetty_koko": pyoristetty_koko,  
                "turvalasi": item["turvalasi"],
                "välikarmi": item["välikarmi"],
                "sälekaihtimet": item["sälekaihtimet"]
            })

    
    # Tallennetaan muunnettu JSON-tiedosto
    #with open("muunnettu_ikkunat.json", "w", encoding="utf-8") as f:
    #    json.dump(output_json, f, ensure_ascii=False, indent=4)
    

    with open("data/k/ikkuna_json_2.txt", "w", encoding="utf-8") as tiedosto:
        json.dump(output_json, tiedosto, ensure_ascii=False, indent=4)

    # Tulostetaan muunnettu JSON
    #print(json.dumps(output_json, ensure_ascii=False, indent=4))


##======================= K A S T E L L I ==========================#
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
         <h2>K A S T E L L I</h2><br>
         <h4>puhdistettu_toimitussisalto.txt to ikkuna_json_2.txt</h4>

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
