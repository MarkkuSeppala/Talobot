import os
import json




#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


# Lukee annetun txt-tiedoston ja palauttaa sen sisällön merkkijonona."""
def lue_txt_tiedosto(tiedostopolku: str) -> str:
    try:
        with open(tiedostopolku, "r", encoding="utf-8") as tiedosto:
            return tiedosto.read()
    except FileNotFoundError:
        print(f"⚠️Virhe: Tiedostoa '{tiedostopolku}' ei löytynyt.")
        return ""
    except Exception as e:
        print(f"⚠️Virhe tiedostoa luettaessa: {e}")

        return ""
    
#==================================================================================================#


#Kirjoittaa annetun tekstin tiedostoon annettuun polkuun.
#Palauttaa virheen, jos tiedostopolku ei ole kelvollinen.
def kirjoita_txt_tiedosto(sisalto: str, tiedostopolku: str):
    
    try:
        if not sisalto:
            raise ValueError("Virhe: Sisältö ei voi olla tyhjä.")

        if not tiedostopolku or not tiedostopolku.endswith(".txt"):
            raise ValueError("Virhe: Tiedostopolun täytyy olla kelvollinen .txt-tiedosto.")

        os.makedirs(os.path.dirname(tiedostopolku), exist_ok=True)  # Luo kansiot tarvittaessa

        with open(tiedostopolku, "w", encoding="utf-8") as tiedosto:
            tiedosto.write(sisalto)

        print(f"✅Tiedosto kirjoitettu onnistuneesti: {tiedostopolku}")

    except Exception as e:
        print(f"⚠️Virhe tiedostoa kirjoittaessa: {e}")



#==================================================================================================#


#Kirjoittaa annetun tekstin json-muodossa tiedostoon annettuun polkuun.
#Palauttaa virheen, jos tiedostopolku ei ole kelvollinen.

def kirjoita_vastaus_jsoniin(response, tiedostopolku: str):
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

def kirjoita_json_tiedostoon(data, tiedostopolku: str):
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


#Kirjoittaa annetun tekstin json-muodossa tiedostoon annettuun polkuun.
#Palauttaa virheen, jos tiedostopolku ei ole kelvollinen.

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

    