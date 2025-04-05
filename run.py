
import os
import sys
#from muunna_ikkunat import muunna_raaka_ikkunat_yksittaisiksi, parsi_rivit_tiedoiksi, kastelli_parsi_rivit_tiedoiksi, muunna_raaka_ikkunat_yksittaisiksi_kastelli
from SQL_kyselyt import lisaa_ikkunat_kantaan, lisaa_ulko_ovet_kantaan, lisaa_valiovet_kantaan, lisaa_toimitussisalto_tuotteet_kantaan, hae_toimitussisallon_tuotteet, hae_toimitussisallon_tuotteet_2


sys.path.append(os.path.abspath("utils"))  # Lisää utils-kansion polku moduulihakemistoksi
#sys.path.append(os.path.abspath("api_kyselyt"))

from config_data import (VALIOVITYYPIT_SIEVITALO_JSON, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT,  
                        IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNA2_JSON, ULKO_OVI_TIEDOT_2_JSON,
                        PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, 
                        PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT,
                        PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT,TOIMITUSSISALTO_TXT, TOIMITUSSISALTO_SIEVITALO_TXT,
                        PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_LUOKKAMUOTOON, PROMPT_SIEVITALO_POIMI_TUOTTEET_TXT)

from config_data import (PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT, PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, IKKUNATIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, 
                         IKKUNA_KASTELLI_JSON, IKKUNA2_KASTELLI_JSON, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT,
                         PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT, ULKO_OVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, PROMPT_KASTELLI_ULKO_OVI_TIEDOT_JSON_MUOTOON, ULKO_OVI_TIEDOT_KASTELLI_2_JSON,
                         VALIOVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT,  PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, VALIOVITYYPIT_KASTELLI_JSON, TOIMITUSSISALTO_KASTELLI_TXT)

# from config_data import (PROMPT_DESIGNTALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_DESIGNTALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, IKKUNATIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT, 
#                          IKKUNA_DESIGNTALO_JSON, IKKUNA2_DESIGNTALO_JSON, PUHDISTETTU_TOIMITUSSISALTO_DESIGNTALO_TXT,
#                          PROMPT_DESIGNTALO_POIMI_ULKO_OVI_TIEDOT_TXT, ULKO_OVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT, PROMPT_DESIGNTALO_ULKO_OVI_TIEDOT_JSON_MUOTOON, ULKO_OVI_TIEDOT_DESIGNTALO_2_JSON,
#                          VALIOVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT, PROMPT_DESIGNTALO_POIMI_VALIOVITIEDOT_TXT,  PROMPT_DESIGNTALO_ANNA_VALIOVIMALLIT_TXT, VALIOVITYYPIT_DESIGNTALO_JSON, TOIMITUSSISALTO_DESIGNTALO_TXT)




from datetime import datetime 
import json
from werkzeug.utils import secure_filename
from generation_config import GENERATION_CONFIG, GENERATION_CONFIG_JSON
from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet
from utils.tietosissallon_kasittely import (sievitalo_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi, puhdista_teksti, 
                                            kastelli_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi, designtalo_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi)
from SQL_kyselyt_tuotteet_tauluun import hae_tuotteet_prompt1_str
                                
from api_kyselyt import api_kysely, api_kysely_kirjoitus_json, api_kysely_ulko_ovet, api_kysely_nelja_parametria
from logger_config import configure_logging
import logging

# Loggerin alustus
configure_logging()
logger = logging.getLogger(__name__)






#============== S I E V I T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#



def run_sievitalo(toimitussisalto_txt, toimitussisalto_id):

        # Ensimmäisenä siivotaan toimitussisältö. Tehdään se mahdollisimman helppolukuiseksi LLM-APILLE
        puhdistettu_toimitussisalto = puhdista_teksti(toimitussisalto_txt)
       
       
        
        #---------------------------------------     Sievitalo ikkunat kantaan      ----------------------------------------
        
        # Palauttaa tekstimuodossa listan toimitussisällön ikkunoista
        ikkunatiedot_kokonaisuudessa = api_kysely(GENERATION_CONFIG, PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, puhdistettu_toimitussisalto)

        # Palauttaa ikkunat JSON-muodossa
        ikkunat_json = api_kysely(GENERATION_CONFIG_JSON, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, ikkunatiedot_kokonaisuudessa)

        # Lisätään ikkunat tietokantaan
        lisaa_ikkunat_kantaan(ikkunat_json, toimitussisalto_id)
        
      


        #---------------------------------------     Sievitalo ulko-ovet kantaan      ----------------------------------------
        ulko_ovet = api_kysely(GENERATION_CONFIG, PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, puhdistettu_toimitussisalto)  
        ulko_ovet = api_kysely_ulko_ovet(GENERATION_CONFIG, PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_LUOKKAMUOTOON, ulko_ovet)
        lisaa_ulko_ovet_kantaan(ulko_ovet, toimitussisalto_id)
          
        
        
       #---------------------------------------     Sievitalo vali-ovet kantaan      ----------------------------------------
        valio_ovet = api_kysely(GENERATION_CONFIG, PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, puhdistettu_toimitussisalto)
        valio_ovet = api_kysely(GENERATION_CONFIG, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT, valio_ovet)
       
        try:
                # Puhdista JSON-merkkijono ```-merkinnöistä
                json_text = valio_ovet.replace("```json", "").replace("```", "").strip()
                
                # Parsi JSON-data
                try:
                        data = json.loads(json_text)
                        valio_ovet = data.get("ovimallit", [])
                except json.JSONDecodeError as e:
                        logging.warning(f"❌ Virheellinen JSON-muoto: {str(e)}")
                
        except Exception as e:
                logging.error(f"❌ Virhe väliovien lisäämisessä: {str(e)}")
        
        lisaa_valiovet_kantaan(valio_ovet, toimitussisalto_id)
        # valiovityypit = api_kysely_kirjoitus_json(GENERATION_CONFIG_JSON, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT, valio_ovet)
        # print("run.py 82. valio_ovet", valiovityypit)


        #---------------------------------------     Sievitalo tuotteet kantaan      ----------------------------------------
        tuotteet = hae_tuotteet_prompt1_str()
        toimitussisalto_tuotteet = api_kysely_nelja_parametria(GENERATION_CONFIG, PROMPT_SIEVITALO_POIMI_TUOTTEET_TXT, puhdistettu_toimitussisalto, tuotteet)
        #print("run.py 116. toimitussisalto_tuotteet", toimitussisalto_tuotteet)
        lisaa_toimitussisalto_tuotteet_kantaan(toimitussisalto_tuotteet, toimitussisalto_id)
        hae_toimitussisallon_tuotteet_2(toimitussisalto_id)
       




#============== K A S T E L L I ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


def run_kastelli(toimitussisalto_txt_polku: str, toimitussisalto_id: str):
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     clean_text2       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #puhdistettu_toimitussisalto = puhdista_teksti(toimitussisalto_txt_polku)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



        #---------------------------------------     PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT      ----------------------------------------
        # ikkunatiedot_kokonaisuudessa = api_kysely(GENERATION_CONFIG, PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT, puhdistettu_toimitussisalto)
        # #print("ikkunatiedot_kokonaisuudessa", ikkunatiedot_kokonaisuudessa)
        # print(kastelli_parsi_rivit_tiedoiksi(ikkunatiedot_kokonaisuudessa))
        # ikkunat_json = muunna_raaka_ikkunat_yksittaisiksi_kastelli(kastelli_parsi_rivit_tiedoiksi(ikkunatiedot_kokonaisuudessa))
        # #print("run_kastelli 110", toimitussisalto_id)
        # #print("ikkunat_json:", ikkunat_json)
        # lisaa_ikkunat_kantaan(ikkunat_json, toimitussisalto_id)
        #-------------------------------------------------------------------------------------------------------------------------------

        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        # api_kysely(PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT, ULKO_OVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT)
        # api_kysely_kirjoitus_json(PROMPT_KASTELLI_ULKO_OVI_TIEDOT_JSON_MUOTOON, GENERATION_CONFIG, ULKO_OVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_KASTELLI_2_JSON)
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        
        
        
        # #++++++++++++++++++++++++++++++++++++++       PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT     ++++++++++++++++++++++++++++++++++++++++++++++
        # api_kysely(PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT, VALIOVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT)
        # api_kysely_kirjoitus_json(PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, GENERATION_CONFIG, VALIOVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, VALIOVITYYPIT_KASTELLI_JSON)
        # #++++++++++++++++++++++++++++++++++++++++++++++                                      ++++++++++++++++++++++++++++++++++++++++++++++++++++

        print("run_kastelli 179")






#============== D E S I G N T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


def run_designtalo():
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     clean_text2       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        puhdista_teksti(lue_txt_tiedosto(TOIMITUSSISALTO_DESIGNTALO_TXT), PUHDISTETTU_TOIMITUSSISALTO_DESIGNTALO_TXT)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



        #---------------------------------------     PROMPT_DESIGNTALO_POIMI_IKKUNATIEDOT_TXT      ----------------------------------------
        api_kysely(PROMPT_DESIGNTALO_POIMI_IKKUNATIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_DESIGNTALO_TXT, IKKUNATIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT)
        api_kysely_kirjoitus_json(PROMPT_DESIGNTALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, GENERATION_CONFIG, IKKUNATIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT, IKKUNA_DESIGNTALO_JSON)
        #-------------------------------------------------------------------------------------------------------------------------------



        #00000000000000000000000000 IKKUNATIEDOT OMILLE RIVEILLEEN JA KOKO MILLIMETREIKSI 000000000000000000000000000000
        #jokainen ikkuna omalle rivilleen ja koko millimetreiksi
        designtalo_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(IKKUNA_DESIGNTALO_JSON, IKKUNA2_DESIGNTALO_JSON)
        #000000000000000000000000000                                                    000000000000000000000000000000
        
        
        
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     PROMPT_DESIGNTALO_POIMI_ULKO_OVI_TIEDOT_TXT    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        api_kysely(PROMPT_DESIGNTALO_POIMI_ULKO_OVI_TIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_DESIGNTALO_TXT, ULKO_OVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT)
        api_kysely_kirjoitus_json(PROMPT_DESIGNTALO_ULKO_OVI_TIEDOT_JSON_MUOTOON, GENERATION_CONFIG, ULKO_OVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT, ULKO_OVI_TIEDOT_DESIGNTALO_2_JSON)
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        
        
        
        # #++++++++++++++++++++++++++++++++++++++       PROMPT_DESIGNTALO_POIMI_VALIOVITIEDOT_TXT     ++++++++++++++++++++++++++++++++++++++++++++++
        api_kysely(PROMPT_DESIGNTALO_POIMI_VALIOVITIEDOT_TXT, GENERATION_CONFIG, PUHDISTETTU_TOIMITUSSISALTO_DESIGNTALO_TXT, VALIOVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT)
        api_kysely_kirjoitus_json(PROMPT_DESIGNTALO_ANNA_VALIOVIMALLIT_TXT, GENERATION_CONFIG, VALIOVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT, VALIOVITYYPIT_DESIGNTALO_JSON)
        # #++++++++++++++++++++++++++++++++++++++++++++++                                      ++++++++++++++++++++++++++++++++++++++++++++++++++++

