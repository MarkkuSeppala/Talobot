import os
import re
import fitz  # PyMuPDF
import google.generativeai as genai
from datetime import datetime
#test
# **suorita_lohko1()**
def suorita_lohko1():
    # Konfiguroi Gemini API
    genai.configure(api_key="AAIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")  # Vaihda API-avain
    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("lohko1 suoritettu", kellonaika)
    return kellonaika





#==========================#
# **Muuta tekstiksi**
def muuta_tekstiksi(pdf_file):
    def pdf_to_text(pdf):
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            return "".join(page.get_text() for page in doc)

    teksti = pdf_to_text(pdf_file)
    #csv_polku = "data/tiedosto.txt"
    csv_polku = "data/tiedosto.txt"
    with open(csv_polku, "w", encoding="utf-8") as tiedosto:
        tiedosto.write(teksti)

    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("lohko2 suoritettu", kellonaika)
    return kellonaika







#==========================#
# **Poista sanat tekstistä**
def poista_sanat_tekstista():
    tiedostopolku = "data/tiedosto.txt"
    korjattu_tiedosto = "data/tiedosto.txt"
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






#==========================#
# **API-kysely. Poimii kaikki ikkunatiedot poistamatta mitään**
def api_kysely_poimi_ikkunatiedot():
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")  # Vaihda API-avain
    tiedostopolku = "data/tiedosto.txt"

    generation_config = {
        "temperature": 0.05,
        "top_p": 0.80,
        "top_k": 20,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    system_instruction = """
    Sinä olet asiantunteva avustaja, joka analysoi annettua tekstiä.
    Vastaa selkeästi ja suomeksi. Kerro tulokset tiiviisti ja laske tarkasti.
    Annettu teksti on talotoimittajan tarjoukseen liittyvä toimitussisältö.
    Tehtävänäsi on poimia toimitussisällöstä ikkunatiedot.
    Ikkunat on ryhmitelty tekstiin kokojen mukaan.
    Ikkunoiden esittely alkaa sanalla 'IKKUNAT'.
    Jokainen ikkunalohko, jossa on yksi tai useampi saman kokoinen ikkuna esitellään siten, että ensin on sana 'Ikkuna' sitten koko (esim. '11x14') ja sen jälkeen kuinka montako kappaletta tämän kokoisia ikkunoita on.
    Yksi ikkunalohko näyttää esimerkiksi tältä: 'Ikkunat Ikkuna 16x16 2 kpl Asennettuna Avattava ikkuna MSE Ikkunan karmisyvyys 170mm Vesipelti Asennettuna Kiinteä välikarmi Asennettuna Tuuletusmekanismi (tuuletusikkunan maksimileveys 9 tai maksimikoko 1,5m2) Asennettuna Smyygilauta HS Asennettuna'
    Etsi ja listaa ainoastaan ne lohkot, joissa esiintyy 'Ikkuna' tai 'Paloikkuna'.
    Älä lisää rivejä tai arvioi tietoja. Palauta täsmälleen ne ikkunat, jotka esiintyvät tekstissä.
    Älä yhdistä eri kokoja tai lisää mitään ylimääräistä.
    Tulosta kaikki ikkunalohkoon liittyvät tiedot.
    Tulosta lohkojen väliin kolme tyhjää riviä.
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
            ikkuna1 = "data/tiedosto2.txt"
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


#==========================#
# **suorita_lohko5()**
'''
def suorita_lohko5():
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")  # Vaihda API-avain
    tiedostopolku = "data/tiedosto.txt"

    if os.path.exists(tiedostopolku):
        with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
            sisalto = tiedosto.read()
    else:
        print("Tiedostoa ei löytynyt. Tarkista polku.")
        return

    print("tulostuswew")
    print(sisalto)
    print("tulostuswew")

    generation_config = {
        "temperature": 0.05,
        "top_p": 0.40,
        "top_k": 20,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    system_instruction = """
    Tehtäväsi on etsiä tekstistä seuraavat ikkunatiedot...
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

    kysymys = f"{sisalto} Suorita tehtävä ja laske ikkunoiden määrä ja tulosta se."
    response = model.generate_content(kysymys)

    tulosta_viesti(response.text)

    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tulosta_viesti("lohko5 suoritettu", kellonaika)
    print(response.text)
    return kellonaika

#tulosta_viesti("lohko5 suoritettu", kellonaika)
tulosta_viesti = print
'''

#==========================#
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
    tiedostopolku = "data/tiedosto2.txt"

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

    Ikkunoiden esittely alkaa sanalla 'IKKUNAT'.
    Jokainen ikkunalohko, jossa on yksi tai useampi saman kokoinen ikkuna esitellään siten, että ensin on sana 'Ikkuna' sitten koko (esim. '11x14') ja sen jälkeen kuinka montako kappaletta tämän kokoisia ikkunoita on.
    Yksi ikkunalohko näyttää esimerkiksi tältä: 'Ikkunat Ikkuna 16x16 2 kpl Asennettuna Avattava ikkuna MSE Ikkunan karmisyvyys 170mm Vesipelti Asennettuna Kiinteä välikarmi Asennettuna Tuuletusmekanismi (tuuletusikkunan maksimileveys 9 tai maksimikoko 1,5m2) Asennettuna Smyygilauta HS Asennettuna'
    Etsi ja lisää JSON-objekteiksi ainoastaan ne lohkot, joissa esiintyy 'Ikkuna' tai 'Paloikkuna'.
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
                ikkuna_tiedosto = "data/ikkuna_json.txt"
                
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
    
