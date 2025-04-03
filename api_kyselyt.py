import os
import re
import sys
from pathlib import Path
#from config_data import GEMINI_API_KEY
from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet, kirjoita_vastaus_jsoniin
from luokat_ikkuna_ulkoovi_valiovi import UlkoOvi
import json
from logger_config import configure_logging
import logging

# Lisätään projektin juurihakemisto Python-polkuun usealla eri tavalla
# Tapa 1: Suhteellinen polku
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Tapa 2: Absoluuttinen polku (muokkaa tarvittaessa)
sys.path.append('C:/Users/Public/testibot/Talobot')
# Tapa 3: Nykyinen hakemisto
sys.path.append(os.getcwd())

import google.generativeai as genai
from datetime import datetime


# Loggerin alustus
configure_logging()
logger = logging.getLogger(__name__)



#Tuodaan GEMINI_API_KEY
# try:
#     from config_data import GEMINI_API_KEY
#     print("config_data tuonti onnistui!")
# except ImportError as e:
#     print(f"Virhe config_data tuonnissa: {e}")
#GEMINI_API_KEY = os.getenv("AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")    
#genai.configure(api_key=GEMINI_API_KEY)
#print("Gemini API konfiguroitu onnistuneesti!")


# model = genai.GenerativeModel(
#     model_name="gemini-1.5-flash",
#     generation_config={},
#     system_instruction="Tämä on testi."
# )
#response = model.generate_content("Testikysymys")
#print(response.text)




#============== API-KYSELY============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


def api_kysely(generation_config, system_instruction, input_text) -> str:
    """Geneerinen API-kysely aihio, joka saa parametreina asetukset, system instructions ja syöte tekstin.
        Palauttaa API-kysely vastauksen string-muodossa."""

    api_key = os.environ.get('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=lue_txt_tiedosto(system_instruction)
    )

    logger.info("Gemini API konfiguroitu onnistuneesti!")

    kysymys = f"Tässä on teksti: \n{input_text}\n\nToimi ohjeen mukaan."
    try:
        response = model.generate_content(kysymys)
        if response is not None:
            logger.info("API-vastaus saatu")
        else:
            logger.warning("API-vastaus puuttuu")
    except Exception as e:
        logger.error(f"Odottamaton virhe: {e}")
    return response.text


    
#============== API-KYSELY ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#





def api_kysely_kirjoitus_json(system_instruction, generation_config, input_text, output_text):
    #genai.configure(api_key=GEMINI_API_KEY) 
    #tiedostopolku = "data/s/puhdistettu_toimitussisalto.txt"

    # model = genai.GenerativeModel(
    #     model_name="gemini-1.5-flash",
    #     generation_config=generation_config,
    #     system_instruction=lue_txt_tiedosto(system_instruction)
    # )

    #sisalto = lue_txt_tiedosto(input_text)
    kysymys = f"Tässä on teksti: \n{input_text}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)
    print("response.text", response.text)
    
    return response.text
   

def api_kysely_ulko_ovet(generation_config, system_instruction, input_text):
        """Funktion api-kysely palauttaa json-muotoisen vastauksen.
        Vastaus parsitaan ulko_ovi-olioiksi, joka palautetaan listana."""

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=lue_txt_tiedosto(system_instruction)
        )

        
        kysymys = f"Tässä on teksti: \n{input_text}\n\nToimi ohjeen mukaan."
        response = model.generate_content(kysymys)
        if not response.text:
            logger.warning("❌ API-kutsu palautti tyhjän vastauksen")
            return []
        
        # Puhdista response.text ```json-merkinnöistä
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        

        # Muunna vastaus UlkoOvi-olioiksi
        try:
            # Käytä puhdistettua json_text:iä response.text:n sijaan
            ovet_data = json.loads(json_text)
                
            ovet = []
            for ovi_data in ovet_data:
                ovi = UlkoOvi(
                    malli=ovi_data["malli"],
                    paloluokitus_EI_15=ovi_data["paloluokitus_EI_15"],
                    lukko=ovi_data["lukko"],
                    maara=ovi_data["maara"]
                )
                ovet.append(ovi)
                logging.info(f"Added ovi: {vars(ovi)}")  # Tarkista luotu ovi-olio
                
            return ovet
        except json.JSONDecodeError as e:
            logging.error(f"❌ JSON-parsinta epäonnistui: {str(e)}")
            return []
        except Exception as e:
            logging.error(f"❌ Muu virhe: {str(e)}")
            return []





