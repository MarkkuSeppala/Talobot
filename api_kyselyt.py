import os
import re
import sys
from pathlib import Path
#from config_data import GEMINI_API_KEY
from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet, kirjoita_vastaus_jsoniin
from luokat_ikkuna_ulkoovi_valiovi import UlkoOvi
import json

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


def api_kysely(generation_config, system_instruction, input_text):
    print("api_kysely 54")
    #genai.configure(api_key=GEMINI_API_KEY)  # Vaihda API-avain
    #tiedostopolku = "data/s/puhdistettu_toimitussisalto.txt"

    api_key = os.environ.get('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    print("🔹 Gemini API konfiguroitu onnistuneesti!")
    print(f"🔹 Gemini API-avain: {api_key}")

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=lue_txt_tiedosto(system_instruction)
    )
    print("api-kysely // malli määritelty")
    #print("system_instruction", lue_txt_tiedosto(system_instruction))
    #print("input_text 54", lue_txt_tiedosto(input_text))
    #sisalto = lue_txt_tiedosto(input_text)
    kysymys = f"Tässä on teksti: \n{input_text}\n\nToimi ohjeen mukaan."
    response = model.generate_content(kysymys)
    print("api-kysely // vastaus saatu")
    #print("response.text", response.text)
    #kirjoita_txt_tiedosto(response.text, output_text)
    return response.text


    
#============== API-KYSELY, KIRJOITUS JSON ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


# **API-kysely. Poimii kaikki ikkunatiedot poistamatta mitään


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
    kirjoita_vastaus_jsoniin(response, output_text)
    return response.text
   

def api_kysely_ulko_ovet(generation_config, system_instruction, input_text):
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=lue_txt_tiedosto(system_instruction)
        )

        
        kysymys = f"Tässä on teksti: \n{input_text}\n\nToimi ohjeen mukaan."
        response = model.generate_content(kysymys)
        print("response.text", response.text)
        if not response.text:
            print("❌ API-kutsu palautti tyhjän vastauksen")
            return []

        # Muunna vastaus UlkoOvi-olioiksi
        ovet_data = json.loads(response.text)
        ovet = []
        for ovi_data in ovet_data:
            ovi = UlkoOvi(
                malli=ovi_data["malli"],
                paloluokitus_EI_15=ovi_data["paloluokitus_EI_15"],
                lukko=ovi_data["lukko"],
                maara=ovi_data["maara"]
            )
            ovet.append(ovi)
            
        print(f"✅ Muunnettu {len(ovet)} ovea UlkoOvi-olioiksi")
        return ovet





