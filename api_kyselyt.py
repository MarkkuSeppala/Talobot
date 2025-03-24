import os
import re
import sys

from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet, kirjoita_vastaus_jsoniin

# Lisätään projektin juurihakemisto Python-polkuun usealla eri tavalla
# Tapa 1: Suhteellinen polku
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Tapa 2: Absoluuttinen polku (muokkaa tarvittaessa)
sys.path.append('C:/Users/Public/testibot/Talobot')
# Tapa 3: Nykyinen hakemisto
sys.path.append(os.getcwd())



import google.generativeai as genai
from datetime import datetime



#Tuodaan GEMINI_API_KEY
try:
    from config_data import GEMINI_API_KEY
    print("config_data tuonti onnistui!")
except ImportError as e:
    print(f"Virhe config_data tuonnissa: {e}")
    
genai.configure(api_key=GEMINI_API_KEY)
print("Gemini API konfiguroitu onnistuneesti!")







#============== API-KYSELY, KIRJOITUS TXT-TIEDOSTOON ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


def api_kysely(system_instruction, generation_config, input_text, output_text):
    genai.configure(api_key=GEMINI_API_KEY)  # Vaihda API-avain
    #tiedostopolku = "data/s/puhdistettu_toimitussisalto.txt"

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=lue_txt_tiedosto(system_instruction)
    )
    #print("system_instruction", lue_txt_tiedosto(system_instruction))
    #print("input_text 54", lue_txt_tiedosto(input_text))
    #sisalto = lue_txt_tiedosto(input_text)
    kysymys = f"Tässä on teksti: \n{input_text}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)
    #print("response.text", response.text)
    kirjoita_txt_tiedosto(response.text, output_text)
    return response.text

    
#============== API-KYSELY, KIRJOITUS JSON ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


# **API-kysely. Poimii kaikki ikkunatiedot poistamatta mitään


def api_kysely_kirjoitus_json(system_instruction, generation_config, input_text, output_text):
    genai.configure(api_key=GEMINI_API_KEY)  # Vaihda API-avain
    #tiedostopolku = "data/s/puhdistettu_toimitussisalto.txt"

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=lue_txt_tiedosto(system_instruction)
    )

    #sisalto = lue_txt_tiedosto(input_text)
    kysymys = f"Tässä on teksti: \n{input_text}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)
    print("response.text", response.text)
    kirjoita_vastaus_jsoniin(response, output_text)
    return response.text
   




