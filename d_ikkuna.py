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


# **muuta_tekstiksi muuttaa pdf-tiedoston tekstiksi. Lukee tiedoston ja kirjoittaa sen uudelleen.
def muuta_tekstiksi(pdf_file):
    def pdf_to_text(pdf):
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            return "".join(page.get_text() for page in doc)

    teksti = pdf_to_text(pdf_file)

    # Varmista, että kansio 'data/d/' on olemassa ennen kirjoittamista
    os.makedirs("data/d/", exist_ok=True)
    
    csv_polku = "data/d/toimitussisältö_kokonaisuudessa_tekstina.txt"
    with open(csv_polku, "w", encoding="utf-8") as tiedosto:
        tiedosto.write(teksti)

    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("lohko2 suoritettu", kellonaika)
    return kellonaika


#======================= D E S I G N T A L O ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#


#clean_text poistaa turhat erikoismerkit, korjaa numeromuodot ja selkeyttää tekstiä. Lukee tiedoston ja kirjoittaa sen uudelleen.
import re

def clean_text():
 
    tiedostopolku = "data/d/toimitussisältö_kokonaisuudessa_tekstina.txt"
    korjattu_tiedosto = "data/d/toimitussisältö_kokonaisuudessa_tekstina.txt"

    if os.path.exists(tiedostopolku):
        with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
            sisalto = tiedosto.read()

    text = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s@._,-:/]', '', sisalto)  # Poistetaan erikoismerkit (paitsi @, ., _ ja ,)
    text = re.sub(r'\s+', ' ', text).strip()  # Poistetaan ylimääräiset välilyönnit
    text = re.sub(r'(\d{1,3})\s(\d{3})', r'\1\2', text)  # Korjataan hajonneet numerot, esim. 173 500 € -> 173500 €
    text = text.replace("•", "-")  # Korvataan listapallot viivoilla
    

    with open(korjattu_tiedosto, "w", encoding="utf-8") as tiedosto:
        tiedosto.write(text)
    


#======================= D E S I G N T A L O ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#


# **Poista sanat tekstistä**
'''
def poista_sanat_tekstista():
    tiedostopolku = "data/d/toimitussisältö_kokonaisuudessa_tekstina.txt"
    korjattu_tiedosto = "data/d/toimitussisältö_kokonaisuudessa_tekstina.txt"
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




#======================= D E S I G N T A L O ==========================#
#========================================================================================================#
#========================================================================================================#
#========================================================================================================#



# **API-kysely. Poimii kaikki ikkunatiedot poistamatta mitään**
def api_kysely_poimi_ikkunatiedot():
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")  # Vaihda API-avain
    tiedostopolku = "data/d/toimitussisältö_kokonaisuudessa_tekstina.txt"

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

    if os.path.exists(tiedostopolku):
        with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
            sisalto = tiedosto.read()

        kysymys = f"Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan."
        response = model.generate_content(kysymys)

        if response.text:
            ikkuna1 = "data/d/tiedosto2.txt"
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
    tiedostopolku = "data/d/tiedosto2.txt"

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
        leveys, korkeus = map(lambda x: int(float(x.replace(",", "."))), item["koko"].split("x")) # Muunnetaan koko kokonaisluvuiksi (mm) se muutetaan pilkku pisteeksi, koska kokonaisluku (int) ei hyväksy pilkkua
        
        # Muunnetaan mitat millimetreiksi
        leveys_mm = leveys * 100
        korkeus_mm = korkeus * 100
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

