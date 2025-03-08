import os
import re
import google.generativeai as genai
from datetime import datetime
from file_handler import lue_txt_tiedosto, kirjoita_txt_tiedosto, kirjoita_vastaus_jsoniin, lue_json_tiedosto, kirjoita_json_tiedostoon



#============== S  I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#




# **API-kysely. Poimii kaikki ikkunatiedot poistamatta mitään
# **Kirjoittaa vastauksen: data/s/ikkunatiedot_kokonaisuudessa.txt

def api_kysely_poimi_ikkunatiedot():
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

    sisalto = lue_txt_tiedosto("data/s/puhdistettu_toimitussisalto.txt")

    kysymys = f"Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)

    kirjoita_txt_tiedosto(response.text, "data/s/ikkunatiedot_kokonaisuudessa.txt")
    





#============== S  I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



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
    #tiedostopolku = "data/s/ikkunatiedot_kokonaisuudessa.txt"

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

    sisalto = lue_txt_tiedosto("data/s/ikkunatiedot_kokonaisuudessa.txt")

    kysymys = f"""Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan"""
    response = model.generate_content(kysymys)

    
    kirjoita_vastaus_jsoniin(response, "data/s/ikkuna.json")
    return
    


