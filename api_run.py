
import os
import sys

sys.path.append(os.path.abspath("utils"))  # Lisää utils-kansion polku moduulihakemistoksi
sys.path.append(os.path.abspath("api_kyselyt"))

from config_data import (VALIOVITYYPIT_TXT, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT,  
                        IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNA2_JSON, ULKO_OVI_TIEDOT_2_JSON,
                        PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, 
                        PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON,
                        PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT,

                        PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT, PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON,
                        IKKUNATIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, IKKUNA_KASTELLI_JSON_2, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT,
                        PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT, PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT, PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, 
                        PROMPT_KASTELLI_ULKO_OVI_TIEDOT_JSON_MUOTOON, IKKUNA_KASTELLI_JSON)



from datetime import datetime 
import json
from werkzeug.utils import secure_filename
from generation_config import GENERATION_CONFIG
from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet
from utils.s_tietosissallon_kasittely import jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi, clean_text2, kastelli_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi
from s_api_kyselyt import api_kysely, api_kysely_kirjoitus_json
                        




def api_run_sievitalo():

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        api_kysely(PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNATIEDOT_KOKONAISUUDESSA_TXT)
        api_kysely_kirjoitus_json(PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, GENERATION_CONFIG, IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                               %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



        #00000000000000000000000000 IKKUNATIEDOT OMILLE RIVEILLEEN JA KOKO MILLIMETREIKSI 000000000000000000000000000000
        #jokainen ikkuna omalle rivilleen ja koko millimetreiksi
        jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(IKKUNA_JSON, IKKUNA2_JSON)
        #000000000000000000000000000                                                    000000000000000000000000000000
        
        
        
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        api_kysely(PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_TXT, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT)
        api_kysely_kirjoitus_json(PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON, GENERATION_CONFIG, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_2_JSON)
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        
        
        
        #++++++++++++++++++++++++++++++++++++++       ROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT     ++++++++++++++++++++++++++++++++++++++++++++++
        api_kysely(PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT)
        api_kysely(PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT, GENERATION_CONFIG, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVITYYPIT_TXT)
        #++++++++++++++++++++++++++++++++++++++++++++++                                      ++++++++++++++++++++++++++++++++++++++++++++++++++++
    











def api_run_kastelli():

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        api_kysely(PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT, IKKUNATIEDOT_KASTELLI_KOKONAISUUDESSA_TXT)
        api_kysely_kirjoitus_json(PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, GENERATION_CONFIG, IKKUNATIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, IKKUNA_KASTELLI_JSON)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                               %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



        #00000000000000000000000000 IKKUNATIEDOT OMILLE RIVEILLEEN JA KOKO MILLIMETREIKSI 000000000000000000000000000000
        #jokainen ikkuna omalle rivilleen ja koko millimetreiksi
        kastelli_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(IKKUNA_KASTELLI_JSON, IKKUNA_KASTELLI_JSON_2)
        #000000000000000000000000000                                                    000000000000000000000000000000
        
        
        
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        # api_kysely(PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_TXT, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT)
        # api_kysely_kirjoitus_json(PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON, GENERATION_CONFIG, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_2_JSON)
        # #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                                        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        
        
        
        # #++++++++++++++++++++++++++++++++++++++       ROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT     ++++++++++++++++++++++++++++++++++++++++++++++
        # api_kysely(PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT)
        # api_kysely(PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT, GENERATION_CONFIG, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVITYYPIT_TXT)
        # #++++++++++++++++++++++++++++++++++++++++++++++                                      ++++++++++++++++++++++++++++++++++++++++++++++++++++


