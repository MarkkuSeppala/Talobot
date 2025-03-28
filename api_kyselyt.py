import os
import re
import sys
from pathlib import Path
from config_data import GEMINI_API_KEY
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
# try:
#     from config_data import GEMINI_API_KEY
#     print("config_data tuonti onnistui!")
# except ImportError as e:
#     print(f"Virhe config_data tuonnissa: {e}")
#GEMINI_API_KEY = os.getenv("AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg")    
genai.configure(api_key=GEMINI_API_KEY)
print("Gemini API konfiguroitu onnistuneesti!")


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
    #genai.configure(api_key=GEMINI_API_KEY)  # Vaihda API-avain
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
    #kirjoita_txt_tiedosto(response.text, output_text)
    return response.text

'''
def api_kysely(prompt: str, content: str) -> str:
    print("\n🔹 API-kyselyn debug-tiedot:")
    try:
        # Tarkista API-avain
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY puuttuu")
            return None
        print("✅ API-avain löytyi")

        # Konfiguroi Gemini
        genai.configure(api_key=api_key)
        
        # Käytä uudempaa mallia
        model = genai.GenerativeModel('models/gemini-1.5-pro')
        print("✅ Malli luotu onnistuneesti")

        # Yhdistä prompt ja content
        full_prompt = f"{prompt}\n\n{content}"
        
        # Tee API-kutsu
        response = model.generate_content(full_prompt)
        
        if response.text:
            print("✅ API-kutsu onnistui")
            return response.text
        else:
            print("❌ API-kutsu palautti tyhjän vastauksen")
            return None

    except Exception as e:
        print(f"❌ Yleinen virhe: {str(e)}")
        print(f"Virhetyyppi: {type(e)}")
        return None
'''
    
#============== API-KYSELY, KIRJOITUS JSON ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


# **API-kysely. Poimii kaikki ikkunatiedot poistamatta mitään


def api_kysely_kirjoitus_json(system_instruction, generation_config, input_text, output_text):
    genai.configure(api_key=GEMINI_API_KEY)  # Vaihda API-avain
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
   




