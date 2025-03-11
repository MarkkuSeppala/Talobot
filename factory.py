
import os
import sys

sys.path.append(os.path.abspath("utils"))  # Lisää utils-kansion polku moduulihakemistoksi
sys.path.append(os.path.abspath("api_kyselyt"))

from config_data import (VALIOVITYYPIT_TXT, TOIMITUSSISALTO_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT,  
                        IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNA2_JSON, ULKO_OVI_TIEDOT_2_JSON,
                        TEMP_1_TXT, TOIMITUSSISALTO_TXT, 
                        PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, 
                        PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON,
                        PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT)


from datetime import datetime 
import json
from werkzeug.utils import secure_filename
from generation_config import GENERATION_CONFIG

from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet
from utils.s_tietosissallon_kasittely import jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi, clean_text2

#from s_api_kyselyt import api_kysely, api_kysely_kirjoitus_json
                        




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
    valiovi_mallit = lue_txt_tiedosto(VALIOVITYYPIT_TXT)
    if valiovi_mallit is None or valiovi_mallit.strip() == "":
        valiovi_mallit = {"ovimallit": ["Ei löydetty välivovimalleja"]}
    else:
        try:
            valiovi_mallit_lista = [m.strip() for m in valiovi_mallit.split(",")]
            valiovi_mallit = {"ovimallit": valiovi_mallit_lista}


