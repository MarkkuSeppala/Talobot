
import os
import sys

sys.path.append(os.path.abspath("utils"))  # Lisää utils-kansion polku moduulihakemistoksi
#sys.path.append(os.path.abspath("api_kyselyt"))

from config_data import (VALIOVITYYPIT_SIEVITALO_JSON, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT,  
                        IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNA2_JSON, ULKO_OVI_TIEDOT_2_JSON,
                        PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, 
                        PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_LUOKKAMUOTOON,
                        PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT)

from config_data import (PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT, PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, IKKUNATIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, 
                         IKKUNA_KASTELLI_JSON, IKKUNA2_KASTELLI_JSON, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT,

                         PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT, ULKO_OVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, PROMPT_KASTELLI_ULKO_OVI_TIEDOT_JSON_MUOTOON, ULKO_OVI_TIEDOT_KASTELLI_2_JSON,

                         VALIOVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT,  PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, VALIOVITYYPIT_KASTELLI_JSON)



from datetime import datetime 
import json
from werkzeug.utils import secure_filename
from generation_config import GENERATION_CONFIG
from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet
from utils.tietosissallon_kasittely import jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi, puhdista_teksti, kastelli_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi
from api_kyselyt import api_kysely, api_kysely_kirjoitus_json, groq_api_kysely






#============== S I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


def run_sievitalo():

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ikkunatiedot_sievitalo = groq_api_kysely(PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, PUHDISTETTU_TOIMITUSSISALTO_TXT)
        kirjoita_txt_tiedosto(ikkunatiedot_sievitalo, IKKUNATIEDOT_KOKONAISUUDESSA_TXT)
        ikkunat_json_sievitalo = groq_api_kysely(PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, ikkunatiedot_sievitalo)
        kirjoita_txt_tiedosto(ikkunat_json_sievitalo, IKKUNA_JSON)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                               %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



        #00000000000000000000000000 IKKUNATIEDOT OMILLE RIVEILLEEN JA KOKO MILLIMETREIKSI 000000000000000000000000000000
        #jokainen ikkuna omalle rivilleen ja koko millimetreiksi
        jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(IKKUNA_JSON, IKKUNA2_JSON)
        #000000000000000000000000000                                                      000000000000000000000000000000
        
        
        
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ulko_ovi_tiedot_sievitalo = groq_api_kysely(PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, PUHDISTETTU_TOIMITUSSISALTO_TXT)
        kirjoita_txt_tiedosto(ulko_ovi_tiedot_sievitalo, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT)
        #api_kysely_kirjoitus_json(PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON, GENERATION_CONFIG, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_2_JSON)
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                                          xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        
        
        
        #++++++++++++++++++++++++++++++++++++++       ROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT     ++++++++++++++++++++++++++++++++++++++++++++++
        valiovi_tiedot_sievitalo = groq_api_kysely(PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, PUHDISTETTU_TOIMITUSSISALTO_TXT)
        kirjoita_txt_tiedosto(valiovi_tiedot_sievitalo, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT)
        valiovi_json_sievitalo = groq_api_kysely(PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT, valiovi_tiedot_sievitalo)
        kirjoita_txt_tiedosto(valiovi_json_sievitalo, VALIOVITYYPIT_SIEVITALO_JSON)
        #api_kysely_kirjoitus_json(PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT, GENERATION_CONFIG, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVITYYPIT_KASTELLI_JSON)
        #++++++++++++++++++++++++++++++++++++++++                                                 ++++++++++++++++++++++++++++++++++++++++++++++++
    






#============== K A S T E L L I ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#






def api_run_kastelli():

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ikkunatiedot_kastelli = groq_api_kysely(PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT)
        kirjoita_txt_tiedosto(ikkunatiedot_kastelli, IKKUNATIEDOT_KASTELLI_KOKONAISUUDESSA_TXT)
        ikkunat_json_kastelli = groq_api_kysely(PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, ikkunatiedot_kastelli)
        kirjoita_txt_tiedosto(ikkunat_json_kastelli, IKKUNA_KASTELLI_JSON)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                               %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



        #00000000000000000000000000 IKKUNATIEDOT OMILLE RIVEILLEEN JA KOKO MILLIMETREIKSI 000000000000000000000000000000
        #jokainen ikkuna omalle rivilleen ja koko millimetreiksi
        kastelli_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(IKKUNA_KASTELLI_JSON, IKKUNA2_KASTELLI_JSON)
        #000000000000000000000000000                                                    000000000000000000000000000000
        
        
        
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ulko_ovi_tiedot_kastelli = groq_api_kysely(PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT)
        kirjoita_txt_tiedosto(ulko_ovi_tiedot_kastelli, ULKO_OVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT)
        api_kysely_kirjoitus_json(PROMPT_KASTELLI_ULKO_OVI_TIEDOT_JSON_MUOTOON, GENERATION_CONFIG, ULKO_OVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_KASTELLI_2_JSON)
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        
        
        
        # #++++++++++++++++++++++++++++++++++++++       PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT     ++++++++++++++++++++++++++++++++++++++++++++++
        valiovi_tiedot_kastelli = groq_api_kysely(PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT)
        kirjoita_txt_tiedosto(valiovi_tiedot_kastelli, VALIOVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT)
        valiovi_json_kastelli = groq_api_kysely(PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, valiovi_tiedot_kastelli)
        kirjoita_txt_tiedosto(valiovi_json_kastelli, VALIOVITYYPIT_KASTELLI_JSON)
        # #++++++++++++++++++++++++++++++++++++++++++++++                                      ++++++++++++++++++++++++++++++++++++++++++++++++++++


