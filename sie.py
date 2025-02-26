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
    tulosta_viesti("lohko1 suoritettu", kellonaika)
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
    tulosta_viesti("lohko2 suoritettu", kellonaika)
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
    tulosta_viesti("lohko3 suoritettu", kellonaika)
    return kellonaika

def poista_sanat_tekstista2(teksti, poistettavat_sanat):
    for sana in poistettavat_sanat:
        teksti = teksti.replace(sana, "")
    teksti = re.sub(r'TOIMITUSTAPASELOSTE\s+\d+', '', teksti)
    teksti = re.sub(r'^\d{1,2}$', '', teksti, flags=re.MULTILINE)
    return teksti






#==========================#
# **suorita_lohko4()**
def suorita_lohko4():
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
    Sinä olet asiantunteva avustaja, joka analysoi annettua tekstiä...
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
            ikkuna1 = "data/tiedosto.txt"
            with open(ikkuna1, "w", encoding="utf-8") as tiedosto:
                tiedosto.write(response.text)
            print("Tiedosto tallennettu:", ikkuna1)
        else:
            print("Virhe: response.text on tyhjä")

        tulosta_viesti(response.text)

    else:
        print("Tiedostoa ei löytynyt. Tarkista polku.")

    kellonaika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tulosta_viesti("lohko4 suoritettu", kellonaika)
    return kellonaika


#==========================#
# **suorita_lohko5()**
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
