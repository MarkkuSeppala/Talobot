
import os
import sys

sys.path.append(os.path.abspath("utils"))  # Lisää utils-kansion polku moduulihakemistoksi
sys.path.append(os.path.abspath("api_kyselyt"))

from config_data import (VALIOVITYYPIT_SIEVITALO_JSON, TOIMITUSSISALTO_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT,  
                        IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNA2_JSON, ULKO_OVI_TIEDOT_2_JSON,
                        TOIMITUSSISALTO_SIEVITALO_TXT, 
                        PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, 
                        PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON,
                        PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT, ULKO_OVI_TIEDOT_KASTELLI_2_JSON)

from config_data import (IKKUNA2_KASTELLI_JSON, VALIOVITYYPIT_KASTELLI_JSON)


from datetime import datetime 
import json
from werkzeug.utils import secure_filename
from generation_config import GENERATION_CONFIG

from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet
from utils.tietosissallon_kasittely import jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi, clean_text2

#from api_kyselyt import api_kysely, api_kysely_kirjoitus_json
                        



#=============  SIEVITALO  ================================================================
def get_sievitalo_ikkunat():
    json_ikkunat = lue_json_tiedosto(IKKUNA2_JSON)
    if json_ikkunat is None or len(json_ikkunat) == 0:
        json_ikkunat = []  # Varmista, että json_ikkunat on vähintään tyhjä lista
        print("Varoitus: Ikkunatietoja ei löytynyt tai tiedosto on tyhjä.")


    return json_ikkunat


def get_sievitalo_ulko_ovet():
    json_ulko_ovet = lue_json_tiedosto(ULKO_OVI_TIEDOT_2_JSON)
    if json_ulko_ovet is None:
        json_ulko_ovet = []
        print("Varoitus: Ulko-ovitietoja ei löytynyt tai tiedosto on tyhjä.")

    return json_ulko_ovet


def get_sievitalo_valiovi_mallit():
    json_valiovi_mallit = lue_json_tiedosto(VALIOVITYYPIT_SIEVITALO_JSON)
    if json_valiovi_mallit is None:
        json_valiovi_mallit = []
        print("Varoitus: väliovimallitietoja ei löytynyt tai tiedosto on tyhjä.")

    return json_valiovi_mallit





#=============  KASTELLI  ================================================================

def get_kastelli_ikkunat():
    json_ikkunat = lue_json_tiedosto(IKKUNA2_KASTELLI_JSON)
    if json_ikkunat is None or len(json_ikkunat) == 0:
        json_ikkunat = []  # Varmista, että json_ikkunat on vähintään tyhjä lista
        print("Varoitus: Ikkunatietoja ei löytynyt tai tiedosto on tyhjä.")

    return json_ikkunat


def get_kastelli_ulko_ovet():
    json_ulko_ovet = lue_json_tiedosto(ULKO_OVI_TIEDOT_KASTELLI_2_JSON)
    if json_ulko_ovet is None:
        json_ulko_ovet = []
        print("Varoitus: Ulko-ovitietoja ei löytynyt tai tiedosto on tyhjä.")

    return json_ulko_ovet


def get_kastelli_valiovi_mallit():
    json_valiovi_mallit = lue_json_tiedosto(VALIOVITYYPIT_KASTELLI_JSON)
    if json_valiovi_mallit is None:
        json_valiovi_mallit = []
        print("Varoitus: väliovimallitietoja ei löytynyt tai tiedosto on tyhjä.")

    return json_valiovi_mallit


# def get_kastelli_valiovi_mallit():
#     try:
#         # Tarkista ensin onko tiedosto olemassa ja ei-tyhjä
#         if not os.path.exists(VALIOVITYYPIT_KASTELLI_TXT):
#             print(f"Tiedostoa {VALIOVITYYPIT_KASTELLI_TXT} ei löydy")
#             return {'ovimallit': []}
            
#         with open(VALIOVITYYPIT_KASTELLI_TXT, 'r', encoding='utf-8') as file:
#             content = file.read().strip()
#             if not content:  # Jos tiedosto on tyhjä
#                 print("Väliovityyppien tiedosto on tyhjä")
#                 return {'ovimallit': []}
                
#             try:
#                 data = json.loads(content)
#                 if isinstance(data, dict) and 'ovimallit' in data:
#                     return data
#                 else:
#                     print("Virheellinen JSON-rakenne väliovimalleissa")
#                     return {'ovimallit': []}
#             except json.JSONDecodeError as e:
#                 print(f"JSON-parsintavirhe: {e}")
#                 # Kokeillaan luoda oletusdata
#                 default_data = {'ovimallit': ["Perusovi", "Kylpyhuoneovi"]}  # Testidataa
                
#                 # Tallennetaan oletusdata tiedostoon
#                 with open(VALIOVITYYPIT_KASTELLI_TXT, 'w', encoding='utf-8') as f:
#                     json.dump(default_data, f, ensure_ascii=False, indent=2)
                
#                 return default_data
                
#     except Exception as e:
#         print(f"Virhe väliovimallien lukemisessa: {e}")
#         return {'ovimallit': []}
