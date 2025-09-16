
import os
import sys
import time
#from muunna_ikkunat import muunna_raaka_ikkunat_yksittaisiksi, parsi_rivit_tiedoiksi, kastelli_parsi_rivit_tiedoiksi, muunna_raaka_ikkunat_yksittaisiksi_kastelli
from SQL_kyselyt import lisaa_ikkunat_kantaan_ja_koko_x_100, lisaa_ikkunat_kantaan, lisaa_ulko_ovet_kantaan, lisaa_valiovet_kantaan, lisaa_toimitussisalto_tuotteet_kantaan, hae_toimitussisallon_tuotteet, hae_toimitussisallon_tuotteet_2
from SQL_kyselyt_tuotteet_tauluun import hae_tuotteet_if_prompt_1_true


sys.path.append(os.path.abspath("utils"))  # Lisää utils-kansion polku moduulihakemistoksi
#sys.path.append(os.path.abspath("api_kyselyt"))

from config_data import (VALIOVITYYPIT_SIEVITALO_JSON, ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT, VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT,  
                        IKKUNATIEDOT_KOKONAISUUDESSA_TXT, IKKUNA_JSON, PUHDISTETTU_TOIMITUSSISALTO_TXT, IKKUNA2_JSON, ULKO_OVI_TIEDOT_2_JSON,
                        PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, 
                        PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT,
                        PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT,TOIMITUSSISALTO_TXT, TOIMITUSSISALTO_SIEVITALO_TXT,
                        PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_LUOKKAMUOTOON, PROMPT_POIMI_TUOTTEET_1_TXT, PROMPT_POIMI_TUOTTEET_2_TXT)

from config_data import (PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT, PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, IKKUNATIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, 
                         IKKUNA_KASTELLI_JSON, IKKUNA2_KASTELLI_JSON, PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT,
                         PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT, ULKO_OVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, PROMPT_KASTELLI_ULKO_OVI_TIEDOT_LUOKKAMUOTOON, ULKO_OVI_TIEDOT_KASTELLI_2_JSON,
                         VALIOVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT, PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT,  PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, VALIOVITYYPIT_KASTELLI_JSON, TOIMITUSSISALTO_KASTELLI_TXT, PROMPT_KASTELLI_POIMI_TUOTTEET_TXT)

# from config_data import (PROMPT_DESIGNTALO_POIMI_IKKUNATIEDOT_TXT, PROMPT_DESIGNTALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, IKKUNATIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT, 
#                          IKKUNA_DESIGNTALO_JSON, IKKUNA2_DESIGNTALO_JSON, PUHDISTETTU_TOIMITUSSISALTO_DESIGNTALO_TXT,
#                          PROMPT_DESIGNTALO_POIMI_ULKO_OVI_TIEDOT_TXT, ULKO_OVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT, PROMPT_DESIGNTALO_ULKO_OVI_TIEDOT_JSON_MUOTOON, ULKO_OVI_TIEDOT_DESIGNTALO_2_JSON,
#                          VALIOVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT, PROMPT_DESIGNTALO_POIMI_VALIOVITIEDOT_TXT,  PROMPT_DESIGNTALO_ANNA_VALIOVIMALLIT_TXT, VALIOVITYYPIT_DESIGNTALO_JSON, TOIMITUSSISALTO_DESIGNTALO_TXT)




from datetime import datetime 
import json
from werkzeug.utils import secure_filename
from generation_config import GENERATION_CONFIG, GENERATION_CONFIG_JSON
from utils.file_handler import *
from utils.tietosissallon_kasittely import * 
from SQL_kyselyt_tuotteet_tauluun import *                               
from api_kyselyt import api_kysely, api_kysely_kirjoitus_json, api_kysely_ulko_ovet, api_kysely_nelja_parametria, groq_api_kysely, groq_api_kysely_nelja_parametria, groq_api_kysely_ulko_ovet
from csv_export_functions import tallenna_puhdistettu_toimitussisalto_csv
from logger_config import configure_logging
import logging

# Loggerin alustus
configure_logging()
logger = logging.getLogger(__name__)






#============== S I E V I T A L O ============#
def run_sievitalo(toimitussisalto_pdf, toimitussisalto_id: int):

        # Ensimmäisenä siivotaan toimitussisältö. Tehdään se mahdollisimman helppolukuiseksi LLM-APILLE
        print("run.py 55")
        puhdistettu_toimitussisalto = muuta_pdf_ja_puhdista_teksti_docling(toimitussisalto_pdf)
      
        # Lisätään toimitussisältön alku- ja loppuviittaukset
        puhdistettu_toimitussisalto = f"**TOIMITUSSISÄLTÖ START**\n{puhdistettu_toimitussisalto}\n**TOIMITUSSISÄLTÖ END**"
  
        kirjoita_txt_tiedosto(puhdistettu_toimitussisalto, "C:/talobot_env/data/puhdistettu_toimitussisalto.txt")
        
        # Tallenna puhdistettu toimitussisältö CSV-muotoon testausta varten
        tallenna_puhdistettu_toimitussisalto_csv(puhdistettu_toimitussisalto, "Sievitalo", toimitussisalto_id)
      
        
        #---------------------------------------     Sievitalo ikkunat kantaan      ----------------------------------------
        
        print(f"\n🔍 SIEVITALO API-KYSELY: Ikkunatiedot")
        # Palauttaa tekstimuodossa listan toimitussisällön ikkunoista
        ikkunatiedot_kokonaisuudessa = groq_api_kysely(PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, puhdistettu_toimitussisalto)
        kirjoita_txt_tiedosto(ikkunatiedot_kokonaisuudessa, f"terminaalitulosteet/sievitalo_ikkunatiedot_raaka_{toimitussisalto_id}.txt")
        print(f"📋 Ikkunatiedot tallennettu: terminaalitulosteet/sievitalo_ikkunatiedot_raaka_{toimitussisalto_id}.txt")

        print(f"\n🔍 SIEVITALO API-KYSELY: Ikkunat JSON-muotoon")
        # Palauttaa ikkunat JSON-muodossa
        ikkunat_json = groq_api_kysely(PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, ikkunatiedot_kokonaisuudessa)
        kirjoita_txt_tiedosto(ikkunat_json, f"terminaalitulosteet/sievitalo_ikkunat_json_{toimitussisalto_id}.txt")
        print(f"📋 Ikkunat JSON tallennettu: terminaalitulosteet/sievitalo_ikkunat_json_{toimitussisalto_id}.txt")

        # Lisätään ikkunat tietokantaan
        lisaa_ikkunat_kantaan_ja_koko_x_100(ikkunat_json, toimitussisalto_id)
        
      


        #---------------------------------------     Sievitalo ulko-ovet kantaan      ----------------------------------------
        # Lisätään viive ennen ulko-ovien käsittelyä
        logging.info("⏳ Odotetaan 30 sekuntia ennen Sievitalo ulko-ovien käsittelyä...")
        time.sleep(30)
        
        print(f"\n🔍 SIEVITALO API-KYSELY: Ulko-ovet")
        ulko_ovet_teksti = groq_api_kysely(PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, puhdistettu_toimitussisalto)
        kirjoita_txt_tiedosto(ulko_ovet_teksti, f"terminaalitulosteet/sievitalo_ulko_ovet_raaka_{toimitussisalto_id}.txt")
        print(f"📋 Ulko-ovet tallennettu: terminaalitulosteet/sievitalo_ulko_ovet_raaka_{toimitussisalto_id}.txt")
        
        # Tarkista että API-kutsu onnistui
        if not ulko_ovet_teksti or ulko_ovet_teksti.strip() == "":
            logging.warning("❌ Sievitalo ulko-ovien API-kutsu palautti tyhjän vastauksen")
            ulko_ovet = []
        else:
            # Lisätään viive ennen toista API-kutsua
            logging.info("⏳ Odotetaan 30 sekuntia ennen Sievitalo ulko-ovien JSON-muunnosta...")
            time.sleep(30)
            
            print(f"\n🔍 SIEVITALO API-KYSELY: Ulko-ovet JSON-muotoon")
            ulko_ovet = groq_api_kysely_ulko_ovet(PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_LUOKKAMUOTOON, ulko_ovet_teksti)
            kirjoita_txt_tiedosto(str(ulko_ovet), f"terminaalitulosteet/sievitalo_ulko_ovet_json_{toimitussisalto_id}.txt")
            print(f"📋 Ulko-ovet JSON tallennettu: terminaalitulosteet/sievitalo_ulko_ovet_json_{toimitussisalto_id}.txt")
            
            # Tarkista että toinen API-kutsu onnistui
            if not ulko_ovet:
                logging.warning("❌ Sievitalo ulko-ovien JSON-muunnos palautti tyhjän vastauksen")
                ulko_ovet = []
            else:
                logging.info(f"✅ Sievitalo: {len(ulko_ovet)} ulko-ovea löytyi")
        
        lisaa_ulko_ovet_kantaan(ulko_ovet, toimitussisalto_id)
          
        
        
       #---------------------------------------     Sievitalo vali-ovet kantaan      ----------------------------------------
        # Lisätään pidempi viive rate limitingin välttämiseksi
        logging.info("⏳ Odotetaan 30 sekuntia ennen väliovien käsittelyä...")
        time.sleep(30)
        
        print(f"\n🔍 SIEVITALO API-KYSELY: Väliovet")
        valio_ovet = groq_api_kysely(PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, puhdistettu_toimitussisalto)
        kirjoita_txt_tiedosto(valio_ovet, f"terminaalitulosteet/sievitalo_valiovet_raaka_{toimitussisalto_id}.txt")
        print(f"📋 Väliovet tallennettu: terminaalitulosteet/sievitalo_valiovet_raaka_{toimitussisalto_id}.txt")
        
        # Tarkista että API-kutsu onnistui
        if not valio_ovet or valio_ovet.strip() == "":
            logging.warning("❌ Väliovien API-kutsu palautti tyhjän vastauksen")
            valio_ovet = []
        else:
            # Lisätään pidempi viive ennen toista API-kutsua
            logging.info("⏳ Odotetaan 30 sekuntia ennen väliovien mallien käsittelyä...")
            time.sleep(30)
            
            print(f"\n🔍 SIEVITALO API-KYSELY: Väliovet mallit")
            valio_ovet = groq_api_kysely(PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT, valio_ovet)
            kirjoita_txt_tiedosto(valio_ovet, f"terminaalitulosteet/sievitalo_valiovet_mallit_{toimitussisalto_id}.txt")
            print(f"📋 Väliovet mallit tallennettu: terminaalitulosteet/sievitalo_valiovet_mallit_{toimitussisalto_id}.txt")
            
            # Tarkista että toinen API-kutsu onnistui
            if not valio_ovet or valio_ovet.strip() == "":
                logging.warning("❌ Väliovien mallien API-kutsu palautti tyhjän vastauksen")
                valio_ovet = []
            else:
                try:
                    # Puhdista JSON-merkkijono ```-merkinnöistä
                    json_text = valio_ovet.replace("```json", "").replace("```", "").strip()
                    
                    # Parsi JSON-data
                    try:
                        data = json.loads(json_text)
                        valio_ovet = data.get("ovimallit", [])
                        logging.info(f"✅ Parsittu {len(valio_ovet)} väliovimallia")
                    except json.JSONDecodeError as e:
                        logging.warning(f"❌ Virheellinen JSON-muoto: {str(e)}")
                        logging.warning(f"❌ Raw vastaus: {valio_ovet[:200]}...")
                        valio_ovet = []
                    
                except Exception as e:
                    logging.error(f"❌ Virhe väliovien lisäämisessä: {str(e)}")
                    valio_ovet = []
        
        lisaa_valiovet_kantaan(valio_ovet, toimitussisalto_id)
        
        #---------------------------------------     Sievitalo tuotteet kantaan      ----------------------------------------
        # Lisätään viive ennen tuotteiden käsittelyä
        logging.info("⏳ Odotetaan 30 sekuntia ennen Sievitalo tuotteiden käsittelyä...")
        time.sleep(30)
        
        tuotteet = hae_tuotteet_if_prompt_1_true()
        # Lisätään tuotteet alku- ja loppuviittaukset
        tuotteet = f"**TUOTELISTAUS START**\n{tuotteet}\n**TUOTELISTAUS END**"
        #print("run.py 108", tuotteet)
        #print("run.py 109", puhdistettu_toimitussisalto)
        
        #---------------------eka api-kysely tuotteista
        print(f"\n🔍 SIEVITALO API-KYSELY: Tuotteet")
        kirjoita_txt_tiedosto(tuotteet, f"terminaalitulosteet/sievitalo_tuotelista_raaka_{toimitussisalto_id}.txt")
        print(f"📋 Tuotelista tallennettu: terminaalitulosteet/sievitalo_tuotelista_raaka_{toimitussisalto_id}.txt")
        
        print(f"\n🔍 SIEVITALO API-KYSELY: Tuotteet analyysi")
        toimitussisalto_tuotteet = groq_api_kysely_nelja_parametria(PROMPT_POIMI_TUOTTEET_1_TXT, puhdistettu_toimitussisalto, tuotteet)
        kirjoita_txt_tiedosto(toimitussisalto_tuotteet, f"terminaalitulosteet/sievitalo_tuotteet_analyysi_raaka_{toimitussisalto_id}.txt")
        print(f"📋 Tuotteet analyysi tallennettu: terminaalitulosteet/sievitalo_tuotteet_analyysi_raaka_{toimitussisalto_id}.txt")
        
        kirjoita_vastaus_jsoniin(toimitussisalto_tuotteet, "C:/talobot_env/data/testi/testi_1.json")
        #lisaa_toimitussisalto_tuotteet_kantaan(toimitussisalto_tuotteet, toimitussisalto_id)
        tallenna_ai_hakutulokset_kantaan(toimitussisalto_tuotteet)



        #tuotteet = hae_tuotteet_prompt1_str()
        # Lisätään tuotteet alku- ja loppuviittaukset
        #tuotteet = f"**TUOTELISTAUS START**\n{tuotteet}\n**TUOTELISTAUS END**"
        
        
        #toimitussisalto_tuotteet = f"**LOYDETYT TUOTTEET START**\n{toimitussisalto_tuotteet}\n**LOYDETYT TUOTTEET END**"
        #print("run.py 119", toimitussisalto_tuotteet)

        #---------------------toka api-kysely tuotteista. Asetetaan löydetyt tuotteet tuote_id:n mukaisesti json-muodossa
        # toimitussisalto_tuotteet = api_kysely_nelja_parametria(GENERATION_CONFIG, PROMPT_POIMI_TUOTTEET_2_TXT, puhdistettu_toimitussisalto, tuotteet)
        # toimitussisalto_tuotteet = puhdista_tekoalyn_palauttama_json_response_json(toimitussisalto_tuotteet)
       
        print("run.py 126",toimitussisalto_id )
        
      
       




#============== K A S T E L L I ============#
def run_kastelli(toimitussisalto_pdf, toimitussisalto_id: int):
        
        # Ensimmäisenä siivotaan toimitussisältö. Tehdään se mahdollisimman helppolukuiseksi LLM-APILLE
        print("run.py 222 - Kastelli PDF-käsittely")
        puhdistettu_toimitussisalto = muuta_pdf_ja_puhdista_teksti_docling(toimitussisalto_pdf)
      
        # Lisätään toimitussisältön alku- ja loppuviittaukset
        puhdistettu_toimitussisalto = f"**TOIMITUSSISÄLTÖ START**\n{puhdistettu_toimitussisalto}\n**TOIMITUSSISÄLTÖ END**"
        
        # Tallenna puhdistettu toimitussisältö CSV-muotoon testausta varten
        tallenna_puhdistettu_toimitussisalto_csv(puhdistettu_toimitussisalto, "Kastelli", toimitussisalto_id)

       #---------------------------------------     Kastelli ikkunat kantaan      ----------------------------------------
        print(f"\n🔍 KASTELLI API-KYSELY: Ikkunatiedot")
        ikkunatiedot_kokonaisuudessa = groq_api_kysely(PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT, puhdistettu_toimitussisalto)
        kirjoita_txt_tiedosto(ikkunatiedot_kokonaisuudessa, f"terminaalitulosteet/kastelli_ikkunatiedot_raaka_{toimitussisalto_id}.txt")
        print(f"📋 Ikkunatiedot tallennettu: terminaalitulosteet/kastelli_ikkunatiedot_raaka_{toimitussisalto_id}.txt")
        
        print(f"\n🔍 KASTELLI API-KYSELY: Ikkunat JSON-muotoon")
        ikkunat_json = groq_api_kysely(PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, ikkunatiedot_kokonaisuudessa)
        kirjoita_txt_tiedosto(ikkunat_json, f"terminaalitulosteet/kastelli_ikkunat_json_{toimitussisalto_id}.txt")
        print(f"📋 Ikkunat JSON tallennettu: terminaalitulosteet/kastelli_ikkunat_json_{toimitussisalto_id}.txt")
        
        lisaa_ikkunat_kantaan(ikkunat_json, toimitussisalto_id)
        
        
        #---------------------------------------     Kastelli ulko-ovet kantaan      ----------------------------------------
        # Lisätään viive ennen ulko-ovien käsittelyä
        logging.info("⏳ Odotetaan 30 sekuntia ennen Kastelli ulko-ovien käsittelyä...")
        time.sleep(30)
        
        print(f"\n🔍 KASTELLI API-KYSELY: Ulko-ovet")
        ulko_ovet_teksti = groq_api_kysely(PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT, puhdistettu_toimitussisalto)
        kirjoita_txt_tiedosto(ulko_ovet_teksti, f"terminaalitulosteet/kastelli_ulko_ovet_raaka_{toimitussisalto_id}.txt")
        print(f"📋 Ulko-ovet tallennettu: terminaalitulosteet/kastelli_ulko_ovet_raaka_{toimitussisalto_id}.txt")
        
        # Tarkista että API-kutsu onnistui
        if not ulko_ovet_teksti or ulko_ovet_teksti.strip() == "":
            logging.warning("❌ Kastelli ulko-ovien API-kutsu palautti tyhjän vastauksen")
            ulko_ovet = []
        else:
            # Lisätään viive ennen toista API-kutsua
            logging.info("⏳ Odotetaan 30 sekuntia ennen Kastelli ulko-ovien JSON-muunnosta...")
            time.sleep(30)
            
            print(f"\n🔍 KASTELLI API-KYSELY: Ulko-ovet JSON-muotoon")
            ulko_ovet = groq_api_kysely_ulko_ovet(PROMPT_KASTELLI_ULKO_OVI_TIEDOT_LUOKKAMUOTOON, ulko_ovet_teksti)
            kirjoita_txt_tiedosto(str(ulko_ovet), f"terminaalitulosteet/kastelli_ulko_ovet_json_{toimitussisalto_id}.txt")
            print(f"📋 Ulko-ovet JSON tallennettu: terminaalitulosteet/kastelli_ulko_ovet_json_{toimitussisalto_id}.txt")
            
            # Tarkista että toinen API-kutsu onnistui
            if not ulko_ovet:
                logging.warning("❌ Kastelli ulko-ovien JSON-muunnos palautti tyhjän vastauksen")
                ulko_ovet = []
            else:
                logging.info(f"✅ Kastelli: {len(ulko_ovet)} ulko-ovea löytyi")
        
        lisaa_ulko_ovet_kantaan(ulko_ovet, toimitussisalto_id)
        
        
        
       #---------------------------------------     Kastelli vali-ovet kantaan      ----------------------------------------
        # Lisätään pidempi viive rate limitingin välttämiseksi
        logging.info("⏳ Odotetaan 30 sekuntia ennen Kastelli väliovien käsittelyä...")
        time.sleep(30)
        
        print(f"\n🔍 KASTELLI API-KYSELY: Väliovet")
        valio_ovet = groq_api_kysely(PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT, puhdistettu_toimitussisalto)
        kirjoita_txt_tiedosto(valio_ovet, f"terminaalitulosteet/kastelli_valiovet_raaka_{toimitussisalto_id}.txt")
        print(f"📋 Väliovet tallennettu: terminaalitulosteet/kastelli_valiovet_raaka_{toimitussisalto_id}.txt")
        
        # Tarkista että API-kutsu onnistui
        if not valio_ovet or valio_ovet.strip() == "":
            logging.warning("❌ Kastelli väliovien API-kutsu palautti tyhjän vastauksen")
            valio_ovet = []
        else:
            # Lisätään pidempi viive ennen toista API-kutsua
            logging.info("⏳ Odotetaan 30 sekuntia ennen Kastelli väliovien mallien käsittelyä...")
            time.sleep(30)
            
            print(f"\n🔍 KASTELLI API-KYSELY: Väliovet mallit")
            valio_ovet = groq_api_kysely(PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, valio_ovet)
            kirjoita_txt_tiedosto(valio_ovet, f"terminaalitulosteet/kastelli_valiovet_mallit_{toimitussisalto_id}.txt")
            print(f"📋 Väliovet mallit tallennettu: terminaalitulosteet/kastelli_valiovet_mallit_{toimitussisalto_id}.txt")
            
            # Tarkista että toinen API-kutsu onnistui
            if not valio_ovet or valio_ovet.strip() == "":
                logging.warning("❌ Kastelli väliovien mallien API-kutsu palautti tyhjän vastauksen")
                valio_ovet = []
            else:
                try:
                    # Puhdista JSON-merkkijono ```-merkinnöistä
                    json_text = valio_ovet.replace("```json", "").replace("```", "").strip()
                    
                    # Parsi JSON-data
                    try:
                        data = json.loads(json_text)
                        valio_ovet = data.get("ovimallit", [])
                        logging.info(f"✅ Parsittu {len(valio_ovet)} Kastelli väliovimallia")
                    except json.JSONDecodeError as e:
                        logging.warning(f"❌ Virheellinen JSON-muoto: {str(e)}")
                        logging.warning(f"❌ Raw vastaus: {valio_ovet[:200]}...")
                        valio_ovet = []
                    
                except Exception as e:
                    logging.error(f"❌ Virhe Kastelli väliovien lisäämisessä: {str(e)}")
                    valio_ovet = []
        
        lisaa_valiovet_kantaan(valio_ovet, toimitussisalto_id)
       


        # Lisätään viive ennen tuotteiden käsittelyä
        logging.info("⏳ Odotetaan 30 sekuntia ennen Kastelli tuotteiden käsittelyä...")
        time.sleep(30)
        
        tuotteet = hae_tuotteet_if_prompt_1_true()
        
        print(f"\n🔍 KASTELLI API-KYSELY: Tuotteet")
        kirjoita_txt_tiedosto(tuotteet, f"terminaalitulosteet/kastelli_tuotelista_raaka_{toimitussisalto_id}.txt")
        print(f"📋 Tuotelista tallennettu: terminaalitulosteet/kastelli_tuotelista_raaka_{toimitussisalto_id}.txt")
        
        print(f"\n🔍 KASTELLI API-KYSELY: Tuotteet analyysi")
        toimitussisalto_tuotteet = groq_api_kysely_nelja_parametria(PROMPT_KASTELLI_POIMI_TUOTTEET_TXT, puhdistettu_toimitussisalto, tuotteet)
        kirjoita_txt_tiedosto(toimitussisalto_tuotteet, f"terminaalitulosteet/kastelli_tuotteet_analyysi_raaka_{toimitussisalto_id}.txt")
        print(f"📋 Tuotteet analyysi tallennettu: terminaalitulosteet/kastelli_tuotteet_analyysi_raaka_{toimitussisalto_id}.txt")
        
        toimitussisalto_tuotteet = poista_json_merkinta(toimitussisalto_tuotteet)
        kirjoita_txt_tiedosto(toimitussisalto_tuotteet, f"terminaalitulosteet/kastelli_tuotteet_analyysi_puhdistettu_{toimitussisalto_id}.txt")
        print(f"📋 Tuotteet analyysi (puhdistettu) tallennettu: terminaalitulosteet/kastelli_tuotteet_analyysi_puhdistettu_{toimitussisalto_id}.txt")
        #print("run.py 158. toimitussisalto_tuotteet", toimitussisalto_tuotteet)
        kirjoita_txt_tiedosto(toimitussisalto_tuotteet, IKKUNATIEDOT_KASTELLI_KOKONAISUUDESSA_TXT)
        lisaa_toimitussisalto_tuotteet_kantaan(toimitussisalto_tuotteet, toimitussisalto_id)
        print("run.py 160. toimitussisalto_id", toimitussisalto_id)
        kirjoita_txt_tiedosto(hae_toimitussisallon_tuotteet_2(toimitussisalto_id), IKKUNATIEDOT_KASTELLI_KOKONAISUUDESSA_TXT)

        print("run_kastelli 162")






#============== D E S I G N T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


def run_designtalo():
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     clean_text2       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        puhdistettu_toimitussisalto = puhdista_teksti(lue_txt_tiedosto(TOIMITUSSISALTO_DESIGNTALO_TXT))
        kirjoita_txt_tiedosto(puhdistettu_toimitussisalto, PUHDISTETTU_TOIMITUSSISALTO_DESIGNTALO_TXT)
        
        # Lisää toimitussisältön alku- ja loppuviittaukset
        puhdistettu_toimitussisalto = f"**TOIMITUSSISÄLTÖ START**\n{puhdistettu_toimitussisalto}\n**TOIMITUSSISÄLTÖ END**"
        
        # Tallenna puhdistettu toimitussisältö CSV-muotoon testausta varten
        tallenna_puhdistettu_toimitussisalto_csv(puhdistettu_toimitussisalto, "Designtalo", 0)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



        #---------------------------------------     PROMPT_DESIGNTALO_POIMI_IKKUNATIEDOT_TXT      ----------------------------------------
        ikkunatiedot_designtalo = groq_api_kysely(PROMPT_DESIGNTALO_POIMI_IKKUNATIEDOT_TXT, puhdistettu_toimitussisalto)
        kirjoita_txt_tiedosto(ikkunatiedot_designtalo, IKKUNATIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT)
        ikkunat_json_designtalo = groq_api_kysely(PROMPT_DESIGNTALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, ikkunatiedot_designtalo)
        kirjoita_txt_tiedosto(ikkunat_json_designtalo, IKKUNA_DESIGNTALO_JSON)
        #-------------------------------------------------------------------------------------------------------------------------------



        #00000000000000000000000000 IKKUNATIEDOT OMILLE RIVEILLEEN JA KOKO MILLIMETREIKSI 000000000000000000000000000000
        #jokainen ikkuna omalle rivilleen ja koko millimetreiksi
        designtalo_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(IKKUNA_DESIGNTALO_JSON, IKKUNA2_DESIGNTALO_JSON)
        #000000000000000000000000000                                                    000000000000000000000000000000
        
        
        
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     PROMPT_DESIGNTALO_POIMI_ULKO_OVI_TIEDOT_TXT    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ulko_ovi_tiedot_designtalo = groq_api_kysely(PROMPT_DESIGNTALO_POIMI_ULKO_OVI_TIEDOT_TXT, puhdistettu_toimitussisalto)
        kirjoita_txt_tiedosto(ulko_ovi_tiedot_designtalo, ULKO_OVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT)
        ulko_ovi_json_designtalo = groq_api_kysely(PROMPT_DESIGNTALO_ULKO_OVI_TIEDOT_JSON_MUOTOON, ulko_ovi_tiedot_designtalo)
        kirjoita_txt_tiedosto(ulko_ovi_json_designtalo, ULKO_OVI_TIEDOT_DESIGNTALO_2_JSON)
        #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        
        
        
        # #++++++++++++++++++++++++++++++++++++++       PROMPT_DESIGNTALO_POIMI_VALIOVITIEDOT_TXT     ++++++++++++++++++++++++++++++++++++++++++++++
        valiovi_tiedot_designtalo = groq_api_kysely(PROMPT_DESIGNTALO_POIMI_VALIOVITIEDOT_TXT, puhdistettu_toimitussisalto)
        kirjoita_txt_tiedosto(valiovi_tiedot_designtalo, VALIOVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT)
        valiovi_json_designtalo = groq_api_kysely(PROMPT_DESIGNTALO_ANNA_VALIOVIMALLIT_TXT, valiovi_tiedot_designtalo)
        kirjoita_txt_tiedosto(valiovi_json_designtalo, VALIOVITYYPIT_DESIGNTALO_JSON)
        # #++++++++++++++++++++++++++++++++++++++++++++++                                      ++++++++++++++++++++++++++++++++++++++++++++++++++++

