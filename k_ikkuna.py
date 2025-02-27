import io
import os
import re
import fitz  # PyMuPDF
import google.generativeai as genai
#import tkinter as tk
#from tkinter import filedialog
from datetime import datetime



##======================= K A S T E L L I ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#


# **muuta_tekstiksi muuttaa pdf-tiedoston tekstiksi. Lukee tiedoston ja kirjoittaa sen uudelleen.
def muuta_tekstiksi(pdf_file):
    def pdf_to_text(pdf):
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            return "".join(page.get_text() for page in doc)

    teksti = pdf_to_text(pdf_file)

    # Varmista, että kansio 'data/k/' on olemassa ennen kirjoittamista
    os.makedirs("data/k", exist_ok=True)
    
    csv_polku = "data/k/tiedosto.txt"
    with open(csv_polku, "w", encoding="utf-8") as tiedosto:
        tiedosto.write(teksti)

    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("lohko2 suoritettu", kellonaika)
    return kellonaika


##======================= K A S T E L L I ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#


#clean_text poistaa turhat erikoismerkit, korjaa numeromuodot ja selkeyttää tekstiä. Lukee tiedoston ja kirjoittaa sen uudelleen.
import re

def clean_text():
 
    tiedostopolku = "data/k/tiedosto.txt"
    korjattu_tiedosto = "data/k/tiedosto.txt"

    if os.path.exists(tiedostopolku):
        with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
            sisalto = tiedosto.read()

    text = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s@._,-:/]', '', sisalto)  # Poistetaan erikoismerkit (paitsi @, ., _ ja ,)
    text = re.sub(r'\s+', ' ', text).strip()  # Poistetaan ylimääräiset välilyönnit
    text = re.sub(r'(\d{1,3})\s(\d{3})', r'\1\2', text)  # Korjataan hajonneet numerot, esim. 173 500 € -> 173500 €
    text = text.replace("•", "-")  # Korvataan listapallot viivoilla
    

    with open(korjattu_tiedosto, "w", encoding="utf-8") as tiedosto:
        tiedosto.write(text)
    


##======================= K A S T E L L I ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#


# **Poista sanat tekstistä**
'''
def poista_sanat_tekstista():
    tiedostopolku = "data/k/tiedosto.txt"
    korjattu_tiedosto = "data/k/tiedosto.txt"
    poistettavat_sanat = [
        "Sievitalo Oy", "Mestarintie 6", "TOIMITUSTAPASELOSTE", "67101 KOKKOLA",
        "Puh. 06 822 1111", "Fax 06 822 1112", "www.sievitalo.fi", "Y-tunnus: 2988131-5", "RAKENNE- JA"
    ]

    if os.path.exists(tiedostopolku):
        with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
            sisalto = tiedosto.read()

        puhdistettu_sisalto = poista_sanat_tekstista2(sisalto, poistettavat_sanat)

        with open(korjattu_tiedosto, "w", encoding="utf-8") as tiedosto:
            tiedosto.write(puhdistettu_sisalto)

        print(f"Korjattu teksti tallennettu tiedostoon: {korjattu_tiedosto}")
    else:
        print("Tiedostoa ei löytynyt. Tarkista polku.")

    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("lohko3 suoritettu", kellonaika)
    return kellonaika

def poista_sanat_tekstista2(teksti, poistettavat_sanat):
    for sana in poistettavat_sanat:
        teksti = teksti.replace(sana, "")
    teksti = re.sub(r'TOIMITUSTAPASELOSTE\s+\d+', '', teksti)
    teksti = re.sub(r'^\d{1,2}$', '', teksti, flags=re.MULTILINE)
    return teksti
'''



##======================= K A S T E L L I ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#



# **API-kysely. Poimii kaikki ikkunatiedot poistamatta mitään**
def api_kysely_poimi_ikkunatiedot():
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")  # Vaihda API-avain
    tiedostopolku = "data/k/tiedosto.txt"

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

    if os.path.exists(tiedostopolku):
        with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
            sisalto = tiedosto.read()

        kysymys = f"Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan."
        response = model.generate_content(kysymys)

        if response.text:
            ikkuna1 = "data/k/tiedosto2.txt"
            with open(ikkuna1, "w", encoding="utf-8") as tiedosto:
                tiedosto.write(response.text)
            print("Tiedosto tallennettu:", ikkuna1)
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
    tiedostopolku = "data/k/tiedosto2.txt"

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

        #print("Gemini API:n vastaus:", response.text)

        
        if response.text:
            try:
                ikkuna_data = json.loads(response.text)
                ikkuna_tiedosto = "data/k/ikkuna_json.txt"
                
                with open(ikkuna_tiedosto, "w", encoding="utf-8") as tiedosto:
                    json.dump(ikkuna_data, tiedosto, ensure_ascii=False, indent=4)
                
                #print("JSON-tiedosto tallennettu:", ikkuna_tiedosto)

                # Muodostetaan DataFrame ja tulostetaan se taulukkona
                df = pd.DataFrame(ikkuna_data)
                #print("\nIkkunat taulukkona:\n")
                #print(df.to_string(index=False))

                # Korvataan True "✓" ja False tyhjällä
                df.replace({True: "😊", False: ""}, inplace=True)

                # Muodostetaan kaunis taulukko
                taulukko = tabulate(df, headers="keys", tablefmt="grid")


                
                # Tulostetaan JSON-objektit terminaaliin
                #print(taulukko)
            except json.JSONDecodeError:
                print("Virhe JSON-datan käsittelyssä. Tarkista Gemini-vastaus.")
        else:
            print("Virhe: response.text on tyhjä")
    else:
        print("Tiedostoa ei löytynyt. Tarkista polku.")

    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("api_kysely_poimi_ikkunatiedot", kellonaika)
    return kellonaika
    



#========================================================================================================#
#========================================================================================================#
#========================================================================================================#




def ikkunat_omille_riveille_koon_pyoristys():
    import json
    #import math

    '''
    # Alkuperäinen JSON-tiedosto
    input_json = [
        {"koko": "2030x2290", "kpl": 3, "turvalasi": True, "välikarmi": False, "sälekaihtimet": True},
        {"koko": "1130x2290", "kpl": 1, "turvalasi": True, "välikarmi": False, "sälekaihtimet": True},
        {"koko": "1130x390", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True},
        {"koko": "1730x490", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True},
        {"koko": "1130x2290", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True},
        {"koko": "1130x2290", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True},
        {"koko": "830x2090", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True},
        {"koko": "830x2090", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True}
    ]
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

 
