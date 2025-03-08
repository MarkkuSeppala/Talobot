import os
import re
import google.generativeai as genai
from datetime import datetime
from file_handler import lue_txt_tiedosto, kirjoita_txt_tiedosto, kirjoita_vastaus_jsoniin, lue_json_tiedosto, kirjoita_json_tiedostoon



#============== S I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#




# **API-kysely. Poimii kaikki ikkunatiedot poistamatta mitään**

def api_kysely_poimi_ulko_ovitiedot():
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")  # Vaihda API-avain
    #tiedostopolku = "data/s/puhdistettu_toimitussisalto.txt"

    generation_config = {
        "temperature": 0.05,
        "top_p": 0.80,
        "top_k": 20,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    system_instruction = """
    Sinä olet asiantunteva avustaja, joka analysoi annettua tekstiä.
    Poimi annetusta tekstistä vain ulko-ovien tiedot.
    Ulko-ovien esittely alkaa sanalla "ULKO-OVET". Sen jälkeen on yleisesittely:
    "Ulko-ovet valkoisia tiivistettyjä Pihla Varma levyrakenteisia lämpöovia, karmisyvyys 170mm.
    Pihla Patio-parvekeovet yksilehtisiä lämpöovia, sisäpuoli valkoinen sävy NCS S 0502-Y.
    Ulkopuoli maalattua alumiinia, sävyvaihtoehdot valkoinen RAL 9010, tummanharmaa RAL7024,
    musta RAL9005 tai tummanruskea RR32. Karmisyvyys 170mm.
    Varastonovet valkoisia Pihla Vieno levyrakenteisia lämpöovia, karmisyvyys 130mm."
    Yleisesittelyä ei saa poimia ulko-oviteitoihin.
    Yleisesittelyn jälkeen ulko-oviesittely jatkuu keskeyksestä.
    Poimi tekstiä vasta sanasta "Pääovi" lähtien.    
    Mikäli aineistossa on autotallin nosto-ovi tai ulkoliukuovi, poimi myös niiden tiedot mukaan tähän listaukseen.
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

    sisalto = lue_txt_tiedosto("data/s/puhdistettu_toimitussisalto.txt")
   
    kysymys = f"Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)

    kirjoita_txt_tiedosto(response.text, "data/s/ulko_ovi_tiedot_kokonaisuudessa.txt")
    




#============== S I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



# **API-kysely. Ryhmittelee valitut ulko-ovitiedot JSON-taulukoksi**
def api_ryhmittele_valitut_ulko_ovitiedot_json_muotoon():
    #import os
    import json
    #import google.generativeai as genai
    import pandas as pd
    from tabulate import tabulate
    from datetime import datetime

    # Konfiguroi Gemini API
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")

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
    Annettu teksti on osa talotoimittajan tarjoukseen liittyvästä toimitussisältöstä.
    Tehtävänäsi on poimia annetusta tekstistä jokainen ulko-ovi ja siihen liittyvät tiedot omaksi ryhmäksi.
    Huomioi, että myös autotallin nosto-ovi ja ulkoliukuovi ovat ulko-oveja.
    Tekstissä esiintyvä kappalemäärä tarkoittaa ovien kappalemääriä.
    Palauta tiedot JSON -muodossa
    """

    # Alusta Gemini-malli system instructions -kentällä
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

    sisalto = lue_txt_tiedosto("data/s/ulko_ovi_tiedot_kokonaisuudessa.txt")

    kysymys = f"""Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan"""
    response = model.generate_content(kysymys)

    
    kirjoita_vastaus_jsoniin(response, "data/s/ulko_ovi_tiedot.json")
    return




#============== S I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



# **API-kysely. Ryhmittelee valitut ulko-ovitiedot JSON-taulukoksi**
def api_poistaa_valitut_sanat_ulko_ovitiedoista_json_muotoon():
    #import os
    import json
    #import google.generativeai as genai
    import pandas as pd
    from tabulate import tabulate
    from datetime import datetime

    # Konfiguroi Gemini API
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")

    # Määritä generation_config ja system_instruction
    generation_config = {
        "temperature": 0.05,
        "top_p": 0.80,
        "top_k": 20,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    system_instruction = """
    Sinä olet asiantunteva avustaja. Sinulle annetaan JSON-rakenne, jossa on ulko-ovien tietoja.  
    Tehtäväsi on poistaa **turhat avain-arvot** jokaisesta ovesta:  
    
    📌 **Esimerkki alkuperäisestä JSON-rakenteesta:**  
    "Ulko-ovi - Patio": {
        "merkki": "Pihla",
        "malli": "Patio",
        "tyyppi": "parvekeovi",
        "lasi": "kirkas, Asennettuna",
        "ulkoväri": [
            "valkoinen RAL9010",
            "musta RAL9005",
            "tummanharmaa RAL7024",
            "tummanruskea RR32"
        ],
        "sisäväri": "valkoinen",
        "määrä": "1 kpl",
        "asennus": "Asennettuna",
        "kynnyspelti": "alumiini, Asennettuna",
        "kahva": "Hoppe-Tokyo, pitkäsuljin, Asennettuna",
        "smyygilauta": "HS, Asennettuna"
        },
    
    
    **Esimerkki halutusta lopputuloksesta:**
    [
    "Ulko-ovi - Pääovi": {
        "merkki": "Pihla",
        "malli": "EI-15 M31",
        "lukko": "YALE dorman",
        "määrä": "1 kpl"
    }
    ]



    """

    # Alusta Gemini-malli system instructions -kentällä
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

    sisalto = lue_json_tiedosto("data/s/ulko_ovi_tiedot.json")

    kysymys = f"""Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan"""
    response = model.generate_content(kysymys)

    
    kirjoita_vastaus_jsoniin(response, "data/s/ulko_ovi_tiedot_2.json")
    return



#============== S I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#





#import json

# Avaa ikkuna_json.txt -tiedostoon., asettaa jokaisen ikkunan omalle riville ja muuttaa ikkunamitat millimetreiksi.
# Tallettaa lopuksi ikkuna_json_2.txt -tiedostoon.
'''
def  jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi():
    output_json = []

    # **Ladataan JSON-tiedot tiedostosta ennen käyttöä**
    with open("data/s/ikkuna_json.txt", "r", encoding="utf-8") as tiedosto:
        json_data = json.load(tiedosto)

    for item in json_data:
        leveys, korkeus = map(int, item["koko"].split("x"))  # Muutetaan mitat kokonaisluvuiksi (dm)
        
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
    with open("data/s/ikkuna_json_2.txt", "w", encoding="utf-8") as tiedosto:
        json.dump(output_json, tiedosto, ensure_ascii=False, indent=4)

    print("JSON-tiedosto luotu onnistuneesti!")
'''






