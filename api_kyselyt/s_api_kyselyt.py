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

def api_kysely_poimi_ikkunatiedot(puhdistettu_toimitussisalto, ikkunatiedot_kokonaisuudessa):
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

    sisalto = puhdistettu_toimitussisalto

    kysymys = f"Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)
        
    kirjoita_txt_tiedosto(response.text, ikkunatiedot_kokonaisuudessa)
    





#============== S  I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



# **API-kysely. Ryhmittelee valitut ikkunatiedot JSON-taulukoksi**
def api_ryhmittele_valitut_ikkunatiedot_json_muotoon(ikkunatiedot_kokonaisuudessa_txt, ikkuna_json):
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

    sisalto = lue_txt_tiedosto(ikkunatiedot_kokonaisuudessa_txt)

    kysymys = f"""Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan"""
    response = model.generate_content(kysymys)

    print(response.text)
    kirjoita_vastaus_jsoniin(response, ikkuna_json)
    return
    


#============== S I E V I T A L O == V A L I O V E T ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



# **API-kysely. Poimii kaikki väliovitiedot poistamatta mitään**
def api_kysely_poimi_valiovitiedot(puhdistettu_toimitussisalto_txt, valiovi_tiedot_kokonaisuudessa_txt):
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

       
    sisalto = lue_txt_tiedosto(puhdistettu_toimitussisalto_txt)
   
    kysymys = f"Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)

    kirjoita_txt_tiedosto(response.text, valiovi_tiedot_kokonaisuudessa_txt)



    
#============== S I E V I T A L O == V A L I O V E T ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



# **API-kysely. Tiivistää valioviteidot JSON-taulukoksi, joka ilmaisee ainoastaan millaisia väliovityyppejä tiedostossa on.**
# **Funktio lukee tiedoston "data/s/valiovi_tiedot_kokonaisuudessa.txt" ja kirjoittaa tuloksen valiovet_json.txt -tiedostoon.
def api_kysely_anna_valiovimallit(valiovi_tiedot_kokonaisuudessa_txt, valiovityypit_txt):
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

     
    sisalto = lue_txt_tiedosto(valiovi_tiedot_kokonaisuudessa_txt)
        
    #print("Tiedosto löytyi:", sisalto)
        #with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
        #    sisalto = tiedosto.read()

    kysymys = f"Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)

    kirjoita_txt_tiedosto(response.text, valiovityypit_txt)
    
    
    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #tulosta_viesti("api_kysely_poimi_ikkunatiedot", kellonaika)
    return kellonaika


#============== S I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#




# **API-kysely. Poimii kaikki ikkunatiedot poistamatta mitään**

def api_kysely_poimi_ulko_ovitiedot(puhdistettu_toimitussisalto_txt, ulko_ovi_tiedot_kokonaisuudessa_txt):
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

    sisalto = lue_txt_tiedosto(puhdistettu_toimitussisalto_txt)
   
    kysymys = f"Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)

    kirjoita_txt_tiedosto(response.text, ulko_ovi_tiedot_kokonaisuudessa_txt)



#============== S I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



# **API-kysely. Ryhmittelee valitut ulko-ovitiedot JSON-taulukoksi**
def api_ryhmittele_valitut_ulko_ovitiedot_json_muotoon(ulko_ovi_tiedot_kokonaisuudessa_txt, ulko_ovi_tiedot_json):
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

    sisalto = lue_txt_tiedosto(ulko_ovi_tiedot_kokonaisuudessa_txt)

    kysymys = f"""Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan"""
    response = model.generate_content(kysymys)

    
    kirjoita_vastaus_jsoniin(response, ulko_ovi_tiedot_json)
    return


#============== S I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



# **API-kysely. Ryhmittelee valitut ulko-ovitiedot JSON-taulukoksi**
def api_poistaa_valitut_sanat_ulko_ovitiedoista_json_muotoon(ulko_ovi_tiedot_json, ulko_ovi_tiedot_2_json):
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

    sisalto = lue_json_tiedosto(ulko_ovi_tiedot_json)

    kysymys = f"""Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan"""
    response = model.generate_content(kysymys)

    
    kirjoita_vastaus_jsoniin(response, ulko_ovi_tiedot_2_json)
    return
