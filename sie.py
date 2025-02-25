
import os
import google.generativeai as genai
from datetime import datetime
def suorita_lohko1():
    
    # Konfiguroi Gemini API
    genai.configure(api_key="AIzaSyBHoovpxWyDat5Jg6On-WxxfCYaUaGHyn8")
    #kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #tulosta_viesti("Gemini API toimii!")
    root.update()
    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tulosta_viesti("lohko1 suoritettu", kellonaika)  

#2222222222222222222222222222222222222222222222222222222222222222222#
##**suorita_lohko2()**##
def suorita_lohko2(pdf_file):
    import fitz  # PyMuPDF
    from datetime import datetime

    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def pdf_to_text(pdf_file):
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
        return text

    # Muunna PDF-tiedosto
    teksti = pdf_to_text(pdf_file)

    # Tallenna teksti tiedostoon
    csv_polku = "C:/Talobot/data/tiedosto.txt"
    with open(csv_polku, "w", encoding="utf-8") as tiedosto:
        tiedosto.write(teksti)

    print(f"PDF muunnettu tekstiksi ja tallennettu tiedostoon: {csv_polku}", flush=True)
    
    return kellonaika  # Palautetaan aika Flaskin käyttöön


#33333333333333333333333333333333333333333333333333333333333333333333#
##**suorita_lohko3()**##

import re
from datetime import datetime

def suorita_lohko3():
    tiedostopolku = "C:/Talobot/data/tiedosto.txt"
    korjattu_tiedosto = "C:/Talobot/data/korjattu_teksti.txt"
    
    poistettavat_sanat = ["Sievitalo Oy", "Mestarintie 6", "TOIMITUSTAPASELOSTE", "67101 KOKKOLA", "Puh. 06 822 1111", "Fax 06 822 1112", "www.sievitalo.fi", "Y-tunnus: 2988131-5", "RAKENNE- JA"]
    
    
    if os.path.exists(tiedostopolku):
        with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
            sisalto = tiedosto.read()
        
        puhdistettu_sisalto = poista_sanat_tekstista(sisalto, poistettavat_sanat)
        
        with open(korjattu_tiedosto, "w", encoding="utf-8") as tiedosto:
            tiedosto.write(puhdistettu_sisalto)
        
        print(f"Korjattu teksti tallennettu tiedostoon: {korjattu_tiedosto}")
    else:
        print("Tiedostoa ei löytynyt. Tarkista polku.")
    
    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"lohko3 suoritettu: {kellonaika}")



def poista_sanat_tekstista(teksti, poistettavat_sanat):
    """
    #Poistaa annetut sanat tekstistä ja poistaa myös sanan 'TOIMITUSTAPASELOSTE' jälkeisen numeron.
    """
    for sana in poistettavat_sanat:
        teksti = teksti.replace(sana, "")
    
    # Poistaa sanan 'TOIMITUSTAPASELOSTE' jälkeisen numeron
    teksti = re.sub(r'TOIMITUSTAPASELOSTE\s+\d+', '', teksti)
    
    # Poistaa rivillä yksinään olevat sivunumerot (yhden tai kahden numeron sarjat)
    teksti = re.sub(r'^\d{1,2}$', '', teksti, flags=re.MULTILINE)
    
    return teksti

# Suoritetaan funktio
tulosta_viesti = print  # Varmistetaan, että tulosta_viesti-funktio on määritelty
#suorita_lohko3()





#44444444444444444444444444444444444444444444444444444444444444444#
##**suorita_lohko4()**##
def suorita_lohko4():
  
    import google.generativeai as genai
    from datetime import datetime

    # Konfiguroi Gemini API
    genai.configure(api_key="AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")

    # Määritä tiedostopolku
    tiedostopolku = "C:/Talobot/data/korjattu_teksti.txt"

    # Määritä generation_config ja system_instruction

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

        
        
        kysymys = f"""Tässä on teksti: \n{sisalto}\n\nToimi ohjeen mukaan      """

        # Lähetä kysymys Gemini-mallille
        #model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(kysymys)
        print(response.text)

    else:
        print("Tiedostoa ei löytynyt. Tarkista polku.")

    # Tallenna teksti
    if response.text:  # Varmistetaan, että tekstiä on
        ikkuna1 = "C:/Talobot/data/ikkuna1.txt"
        with open(ikkuna1, "w", encoding="utf-8") as tiedosto:
            tiedosto.write(response.text)
        print("Tiedosto tallennettu:", ikkuna1)
    else:
        print("Virhe: response.text on tyhjä")
    tulosta_viesti(response.text)    
    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    tulosta_viesti("lohko4 suoritettu", kellonaika)

#5555555555555555555555555555555555555555555555#
##**suorita_lohko5()**##  
def suorita_lohko5():
    import google.generativeai as genai
    from datetime import datetime
    #Lohko poistaa ikkunatiedoista ylimääräiset sanat
    #tulosta_viesti("lohko5 alku")
    # Määritä tiedostopolku
    tiedostopolku = "C:/Talobot/data/ikkuna1.txt"
    
    # Tarkista tiedoston olemassaolo ja lue sisältö
    if os.path.exists(tiedostopolku):
        with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
            sisalto = tiedosto.read()
           
    else:
        print("Tiedostoa ei löytynyt. Tarkista polku.")
    
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
    
    system_instruction = f"""
    Tehtäväsi on etsiä tekstistä seuraavat ikkunatiedot:
    Ikkunoiden kappalemäärä, koko, onko sälekaihdin, onko turvalasi, onko kiinteä välikarmi.
    """
    
    # Alusta Gemini-malli system instructions -kentällä
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )
    
    kysymys = f""" {sisalto} Suorita tehtävä ja laske ikkunoiden määrä ja tulosta se."""
    
    #Lähetä kysymys Gemini-mallille

    response = model.generate_content(kysymys)

      
    tulosta_viesti(response.text)

    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tulosta_viesti("lohko5 suoritettu", kellonaika)
    tulosta_viesti("""                 
                   

    """)
    #MSE, MEK, vesipelti, smyykilauta HS, Tuuletusmekanismi, Avattava ikkuna, kpl, Hätäpoistumistiekahva, Asennettuna'.
    #ikkuna1 = "C:/Talobot/data/ikkunat1.txt"
    print(response.text)