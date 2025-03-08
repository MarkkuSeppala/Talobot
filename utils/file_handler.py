import os
import json
from werkzeug.utils import secure_filename
import fitz
from pathlib import Path





#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


# Lukee annetun txt-tiedoston ja palauttaa sen sisällön merkkijonona."""
def lue_txt_tiedosto(tiedostopolku: str) -> str:
    try:
        with open(tiedostopolku, "r", encoding="utf-8") as tiedosto:
            return tiedosto.read()
    except FileNotFoundError:
        print(f"Virhe: Tiedostoa '{tiedostopolku}' ei löytynyt.")
        return ""
    except Exception as e:
        print(f"Virhe tiedostoa luettaessa: {e}")

        return ""
    
#==================================================================================================#


#Kirjoittaa annetun tekstin tiedostoon annettuun polkuun.
#Palauttaa virheen, jos tiedostopolku ei ole kelvollinen.
def kirjoita_txt_tiedosto(sisalto: str, tiedostopolku):
    try:
        if not sisalto:
            raise ValueError("Virhe: Sisältö ei voi olla tyhjä.")

        # Muunnetaan tiedostopolku merkkijonoksi tarvittaessa
        tiedostopolku = str(tiedostopolku)

        if not tiedostopolku.endswith(".txt"):
            raise ValueError("Virhe: Tiedostopolun täytyy olla kelvollinen .txt-tiedosto.")

        os.makedirs(os.path.dirname(tiedostopolku), exist_ok=True)  # Luo kansiot tarvittaessa
        
        with open(tiedostopolku, "w", encoding="utf-8") as tiedosto:
            tiedosto.write(sisalto)

        print(f"✅ Tiedosto kirjoitettu onnistuneesti: {tiedostopolku}")

    except Exception as e:
        print(f"⚠️ Virhe tiedostoa kirjoittaessa: {e}")



#==================================================================================================#


#Kirjoittaa annetun tekstin json-muodossa tiedostoon annettuun polkuun.
#Palauttaa virheen, jos tiedostopolku ei ole kelvollinen.

def kirjoita_vastaus_jsoniin(response, tiedostopolku):
    """Kirjoittaa AI-mallin JSON-muotoisen vastauksen tiedostoon."""
    try:
        if not response.text:
            raise ValueError("⚠️Virhe: Response-objekti ei sisällä tekstiä.")

        # Yritetään muuntaa vastaus JSON-muotoon
        vastaus_json = json.loads(response.text)

        # Tallennetaan JSON-tiedostoon
        with open(tiedostopolku, "w", encoding="utf-8") as tiedosto:
            json.dump(vastaus_json, tiedosto, ensure_ascii=False, indent=4)

        print(f"✅Vastaus tallennettu JSON-tiedostoon: {tiedostopolku}")

    except json.JSONDecodeError:
        print("⚠️Virhe: Response ei ole kelvollinen JSON.")
    except Exception as e:
        print(f"⚠️Virhe tiedostoa kirjoittaessa: {e}")

#==================================================================================================#

import json

def kirjoita_json_tiedostoon(data, tiedostopolku):
    """Kirjoittaa annetun JSON-datan tiedostoon.
    
    Args:
        data (dict | list): JSON-muotoinen Python-objekti.
        tiedostopolku (str): Tiedoston polku, johon JSON tallennetaan.
    
    Returns:
        bool: True, jos kirjoitus onnistui, False jos tuli virhe.
    """
    try:
        # Luodaan tarvittavat kansiot, jos niitä ei ole
        os.makedirs(os.path.dirname(tiedostopolku), exist_ok=True)

        # Kirjoitetaan JSON-tiedostoon
        with open(tiedostopolku, "w", encoding="utf-8") as tiedosto:
            json.dump(data, tiedosto, ensure_ascii=False, indent=4)

        print(f"✅ JSON-tiedosto tallennettu: {tiedostopolku}")
        return True

    except Exception as e:
        print(f"⚠️ Virhe JSON-tiedostoa kirjoittaessa: {e}")
        return False




#==================================================================================================#


#Lukee JSON-tiedoston ja palauttaa sen Python-objektina (dict tai list).

def lue_json_tiedosto(tiedostopolku: str):
    """Lukee JSON-tiedoston ja palauttaa sen Python-objektina (dict tai list)."""
    try:
        with open(tiedostopolku, "r", encoding="utf-8") as tiedosto:
            return json.load(tiedosto)  # Muunnetaan JSON Python-objektiksi

    except FileNotFoundError:
        print(f"⚠️ Virhe: Tiedostoa '{tiedostopolku}' ei löytynyt.")
        return None  # Palautetaan None, jos tiedostoa ei ole

    except json.JSONDecodeError:
        print(f"⚠️ Virhe: Tiedosto '{tiedostopolku}' ei ole kelvollinen JSON.")
        return None

    except Exception as e:
        print(f"⚠️ Virhe tiedostoa luettaessa: {e}")
        return None


#==================================================================================================#


def tallenna_pdf_tiedosto(file, tallennuspolku):
    """
    Tallentaa ladatun PDF-tiedoston haluttuun hakemistoon.
    
    :param file: Flaskin request.files["pdf"] -objekti
    :param tallennuspolku: Merkkijono, minne tiedosto tallennetaan
    :return: Tallennetun tiedoston polku tai virheviesti
    """
    try:
        if not file:
            return "Virhe: Tiedostoa ei ladattu."

        # Varmista, että tiedosto on PDF
        if not file.filename.lower().endswith(".pdf"):
            return "Virhe: Vain PDF-tiedostot ovat sallittuja."

        # Turvallinen tiedostonimi
        tiedostonimi = secure_filename(file.filename)

        # Luo kansio, jos sitä ei ole
        os.makedirs(tallennuspolku, exist_ok=True)

        # Määritä tiedoston tallennuspolku
        tallennettu_polku = os.path.join(tallennuspolku, tiedostonimi)

        # Tallenna tiedosto
        file.save(tallennettu_polku)

        return f"Tiedosto tallennettu onnistuneesti: {tallennettu_polku}"

    except Exception as e:
        return f"Virhe tallennettaessa tiedostoa: {e}"
    


#==================================================================================================#
# **Muuta tekstiksi ja palauttaa txt-tidoston**
import fitz  # PyMuPDF

def muuta_pdf_tekstiksi(pdf_file):
    """
    Muuntaa PDF-tiedoston tekstiksi ja palauttaa sen merkkijonona.
    
    :param pdf_file: Ladattu PDF-tiedosto
    :return: PDF:n sisältämä teksti merkkijonona
    """
    try:
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            return "\n".join(page.get_text() for page in doc)  # Yhdistetään sivut rivinvaihdoilla
        
    except Exception as e:
        print(f"❌ Virhe PDF:n muuntamisessa: {e}")
        return ""  # Jos virhe, palautetaan tyhjä merkkijono





#==================================================================================================#
# Muunnetaan ulko-ovet -json listaksi yhdenmukaisella rakenteella
def normalisoi_ulko_ovet(json_ulko_ovet):
    ovet_lista = []
    
    # Jos json_ulko_ovet on sanakirja, etsitään "ulko_ovet"-avain
    if isinstance(json_ulko_ovet, dict):
        json_ulko_ovet = json_ulko_ovet.get("ulko_ovet", [])

    # Jos json_ulko_ovet on lista, käsitellään suoraan
    if isinstance(json_ulko_ovet, list):
        for ovi in json_ulko_ovet:
            ovet_lista.append({
                "nimi": ovi.get("ovi", "Tuntematon ovi"),
                "määrä": ovi.get("määrä", "Ei tietoa"),
                "lukko": ovi.get("lukko", "Ei tietoa")
            })
    
    return ovet_lista

