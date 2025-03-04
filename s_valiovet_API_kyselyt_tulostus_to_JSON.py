import os
import re
import fitz  # PyMuPDF
import google.generativeai as genai
from file_handler import lue_txt_tiedosto, kirjoita_txt_tiedosto
from datetime import datetime



#============== S  I E V I T A L O == V A L I O V E T ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



# **API-kysely. Poimii kaikki väliovitiedot poistamatta mitään**
def api_kysely_poimi_valiovitiedot():
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")  # Vaihda API-avain
    
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
    
    Tehtävänäsi on poimia toimitussisällöstä väliovitiedot ja palauttaa ne sellaisenaan.
    Väliovitiedot alkavat sanalla 'VÄLIOVET' ja päättyvät seuraavaan otsikkoon.

    Palauta väliovitiedot sellaisenaan, älä muokkaa niitä millään tavalla.

    Tässä on esimerkki väliovitiedoista:

    VÄLIOVET 
    Väliovi kosteantilan ovet Bath satiini, valkoinen ovipaketti satiinilasilla 8-9x21 1 kpl Asennettuna 
    Väliovi sauna Lasiovi Harmaa 9x19 Lasi 8mm karkaistua turvalasia Pyöreä nuppivedin Mäntykarmit 1 kpl Asennettuna
    Väliovi WC2, SAUNATUPA Unique 501, 1-peilinen massiiviovi 7-9x21 2 kpl Asennettuna Väliovenpainike perusmalli, valkoinen tai satiinikromi Asennettuna Tammikynnys Asennettuna
    Väliovi WC2, WC1 Huom ennen tilausta varmistettava asiakkaalta haluavatko Unique vai alla valitun- oven Ääneneristysovi Sound 201DB, 25dB, 8-10x21 2 kpl Asennettuna Väliovenpainike perusmalli, valkoinen tai satiinikromi Asennettuna Tammikynnys Asennettuna 
    Väliovi MH1, MH2, MH3 Unique 501, 1-peilinen massiiviovi 7-9x21 3 kpl Asennettuna Väliovenpainike perusmalli, valkoinen tai satiinikromi Asennettuna 
    Väliovi VH Unique 501, 1-peilinen massiiviovi 7-9x21 1 kpl Asennettuna Väliovenpainike perusmalli, valkoinen tai satiinikromi Asennettuna Tammikynnys Asennettuna
    Liukuovi Eclisse MH1 Eclisse Single 1P, puuovi 700-900 1 kpl Asennettuna Soft Close-ovensulkija 1-way Asennettuna 
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

       
    sisalto = lue_txt_tiedosto("data/s/puhdistettu_toimitussisalto.txt")
        
    #print("Tiedosto löytyi:", sisalto)
        #with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
        #    sisalto = tiedosto.read()

    kysymys = f"Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)

    kirjoita_txt_tiedosto(response.text, "data/s/valiovi_tiedot_kokonaisuudessa.txt")




#============== S  I E V I T A L O == V A L I O V E T ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



# **API-kysely. Tiivistää valioviteidot JSON-taulukoksi, joka ilmaisee ainoastaan millaisia väliovityyppejä tiedostossa on.**
# **Funktio lukee tiedoston "data/s/valiovi_tiedot_kokonaisuudessa.txt" ja kirjoittaa tuloksen valiovet_json.txt -tiedostoon.
def api_kysely_anna_valiovimallit():
    #import os
    import json
    #import google.generativeai as genai
    import pandas as pd
    from tabulate import tabulate
    from datetime import datetime

    # Konfiguroi Gemini API
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")

    # Määritä tiedostopolku
    #tiedostopolku = "data/s/valiovitiedot_kokonaisuudessa.txt"

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
    Tehtävänäsi on selvittää millaisia väliovimalleja tekstissä on.
    Mene teksti läpi ja kerro mitkä seuraavista malleista löytyivät:
    'Bath', 'Unique', 'Eclisse', 'Craft', 'Easy', 'Style', 'Sound', 'Fire'', 'Lasiovi', 'Liune'.
    
    Tulosta tarkasti vain löytämäsi ovimallit. Mikään ovimalli ei saa esiintyä tulostuksessa useammin kuin yhdesti.
    
    Älä lisää mitään ylimääräistä.
    """

    # Alusta Gemini-malli system instructions -kentällä
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

     
    sisalto = lue_txt_tiedosto("data/s/valiovi_tiedot_kokonaisuudessa.txt")
        
    #print("Tiedosto löytyi:", sisalto)
        #with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
        #    sisalto = tiedosto.read()

    kysymys = f"Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)

    kirjoita_txt_tiedosto(response.text, "data/s/valiovityypit.txt")
    
    
    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("api_kysely_poimi_ikkunatiedot", kellonaika)
    return kellonaika


