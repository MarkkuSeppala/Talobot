import os
import re
import sys
from pathlib import Path
#from config_data import GEMINI_API_KEY
from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedosto, normalisoi_ulko_ovet, kirjoita_vastaus_jsoniin
from config_data import GROQ_API_KEY, GROQ_API_URL, GROQ_MODEL
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

import requests
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
#     model_name="gemini-2.0-flash-exp",
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

    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        logger.error("GROQ_API_KEY ei ole asetettu!")
        return ""

    # Groq API URL
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Request body
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "system",
                "content": lue_txt_tiedosto(system_instruction)
            },
            {
                "role": "user",
                "content": f"Tässä on teksti: \n{input_text}\n\nToimi ohjeen mukaan."
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }

    logger.info("Groq API konfiguroitu onnistuneesti!")

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        if result and "choices" in result and len(result["choices"]) > 0:
            logger.info("API-vastaus saatu")
            return result["choices"][0]["message"]["content"]
        else:
            logger.warning("API-vastaus puuttuu tai on tyhjä")
            return ""
    except Exception as e:
        logger.error(f"Odottamaton virhe: {e}")
        return ""

#==================================== api_kysely_nelja_parametria()
def api_kysely_nelja_parametria(generation_config, system_instruction, input_text_1, input_text_2) -> str:
    """Geneerinen API-kysely aihio, joka saa parametreina asetukset, system instructions ja syöte tekstin.
        Palauttaa API-kysely vastauksen string-muodossa."""
    
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        logger.error("GROQ_API_KEY ei ole asetettu!")
        return '{"tunnistukset": []}'

    system_instruction = lue_txt_tiedosto(system_instruction)
    system_instruction_2 = system_instruction + input_text_2

    # Groq API URL
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Request body
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "system",
                "content": system_instruction_2
            },
            {
                "role": "user",
                "content": f"Tässä on teksti: \n{input_text_1}\n\nToimi ohjeen mukaan."
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }

    logger.info("Groq API konfiguroitu onnistuneesti!")

    try:
        import time
        start_time = time.time()
        logger.info(f"Lähetetään API-kysely...")
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        elapsed_time = time.time() - start_time
        logger.info(f"API-kysely valmis {elapsed_time:.2f} sekunnissa")
        
        result = response.json()
        if result and "choices" in result and len(result["choices"]) > 0:
            logger.info("API-vastaus saatu")
            return result["choices"][0]["message"]["content"]
        else:
            logger.warning("API-vastaus puuttuu tai on tyhjä")
            return '{"tunnistukset": []}'  # Palauta tyhjä mutta kelvollinen JSON
    except Exception as e:
        logger.error(f"Odottamaton virhe: {e}")
        # Tarkista onko kyse kvootti-virheestä
        if "429" in str(e) or "quota" in str(e).lower():
            logger.warning("API-kvootti ylitetty, odota hetki ennen uudelleenyritystä")
            import time
            time.sleep(5)  # Odota 5 sekuntia
        return '{"tunnistukset": []}'  # Palauta tyhjä mutta kelvollinen JSON


    
#============== API-KYSELY ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#





def api_kysely_kirjoitus_json(system_instruction, generation_config, input_text, output_text):
    #genai.configure(api_key=GEMINI_API_KEY) 
    #tiedostopolku = "data/s/puhdistettu_toimitussisalto.txt"

    # model = genai.GenerativeModel(
    #     model_name="gemini-2.0-flash-exp",
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
            model_name="gemini-2.0-flash-exp",
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


#============== GROQ API-KYSELY ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#

def groq_api_kysely(system_instruction, input_text, model_name=None) -> str:
    """Groq API-kysely funktio, joka lähettää kyselyn Groq-palveluun.
    
    Args:
        system_instruction: System instruction teksti
        input_text: Syöte teksti
        model_name: Käytettävä malli (valinnainen, käyttää oletusmallia jos ei määritelty)
    
    Returns:
        str: API-vastaus tekstinä
    """
    # Käytä ympäristömuuttujasta tulevaa API-avainta
    api_key = GROQ_API_KEY
    if not api_key:
        logger.error("api_key ei ole määritelty ympäristömuuttujissa")
        return ""
    
    if model_name is None:
        model_name = GROQ_MODEL
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Lue system instruction tiedostosta jos se on polku
    if isinstance(system_instruction, (str, Path)) and str(system_instruction).endswith('.txt'):
        system_instruction = lue_txt_tiedosto(system_instruction)
    
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": system_instruction
            },
            {
                "role": "user", 
                "content": f"Tässä on teksti: \n{input_text}\n\nToimi ohjeen mukaan."
            }
        ],
        "temperature": 0.1,
        "max_tokens": 4000
    }
    
    try:
        import time
        start_time = time.time()
        logger.info(f"Lähetetään Groq API-kysely mallilla {model_name}...")
        
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Groq API-kysely valmis {elapsed_time:.2f} sekunnissa")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                logger.info("Groq API-vastaus saatu")
                return content
            else:
                logger.warning("Groq API-vastaus ei sisällä choices-kenttää")
                return ""
        else:
            logger.error(f"Groq API-virhe: {response.status_code} - {response.text}")
            return ""
            
    except requests.exceptions.Timeout:
        logger.error("Groq API-kysely aikakatkaistu")
        return ""
    except requests.exceptions.RequestException as e:
        logger.error(f"Groq API-kysely epäonnistui: {e}")
        return ""
    except Exception as e:
        logger.error(f"Odottamaton virhe Groq API-kyselyssä: {e}")
        return ""


def groq_api_kysely_nelja_parametria(system_instruction, input_text_1, input_text_2, model_name=None) -> str:
    """Groq API-kysely funktio neljällä parametrilla.
    
    Args:
        system_instruction: System instruction teksti
        input_text_1: Ensimmäinen syöte teksti
        input_text_2: Toinen syöte teksti (lisätään system instructioniin)
        model_name: Käytettävä malli (valinnainen)
    
    Returns:
        str: API-vastaus tekstinä
    """
    # Käytä ympäristömuuttujasta tulevaa API-avainta
    api_key = GROQ_API_KEY
    if not api_key:
        logger.error("api_key ei ole määritelty ympäristömuuttujissa")
        return '{"tunnistukset": []}'
    
    if model_name is None:
        model_name = GROQ_MODEL
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Lue system instruction tiedostosta jos se on polku
    if isinstance(system_instruction, (str, Path)) and str(system_instruction).endswith('.txt'):
        system_instruction = lue_txt_tiedosto(system_instruction)
    
    # Yhdistä system instruction ja input_text_2
    system_instruction_2 = system_instruction + input_text_2
    
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": system_instruction_2
            },
            {
                "role": "user",
                "content": f"Tässä on teksti: \n{input_text_1}\n\nToimi ohjeen mukaan."
            }
        ],
        "temperature": 0.1,
        "max_tokens": 4000
    }
    
    try:
        import time
        start_time = time.time()
        logger.info(f"Lähetetään Groq API-kysely (4 param) mallilla {model_name}...")
        
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Groq API-kysely (4 param) valmis {elapsed_time:.2f} sekunnissa")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                logger.info("Groq API-vastaus saatu")
                return content
            else:
                logger.warning("Groq API-vastaus ei sisällä choices-kenttää")
                return '{"tunnistukset": []}'
        else:
            logger.error(f"Groq API-virhe: {response.status_code} - {response.text}")
            return '{"tunnistukset": []}'
            
    except requests.exceptions.Timeout:
        logger.error("Groq API-kysely aikakatkaistu")
        return '{"tunnistukset": []}'
    except requests.exceptions.RequestException as e:
        logger.error(f"Groq API-kysely epäonnistui: {e}")
        return '{"tunnistukset": []}'
    except Exception as e:
        logger.error(f"Odottamaton virhe Groq API-kyselyssä: {e}")
        return '{"tunnistukset": []}'


def groq_api_kysely_ulko_ovet(system_instruction, input_text, model_name=None):
    """Groq API-kysely ulko-oville, palauttaa UlkoOvi-olioita listana.
    
    Args:
        system_instruction: System instruction teksti
        input_text: Syöte teksti
        model_name: Käytettävä malli (valinnainen)
    
    Returns:
        list: UlkoOvi-olioita listana
    """
    # Käytä ympäristömuuttujasta tulevaa API-avainta
    api_key = GROQ_API_KEY
    if not api_key:
        logger.error("api_key ei ole määritelty ympäristömuuttujissa")
        return []
    
    if model_name is None:
        model_name = GROQ_MODEL
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Lue system instruction tiedostosta jos se on polku
    if isinstance(system_instruction, (str, Path)) and str(system_instruction).endswith('.txt'):
        system_instruction = lue_txt_tiedosto(system_instruction)
    
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": system_instruction
            },
            {
                "role": "user",
                "content": f"Tässä on teksti: \n{input_text}\n\nToimi ohjeen mukaan."
            }
        ],
        "temperature": 0.1,
        "max_tokens": 4000
    }
    
    try:
        import time
        start_time = time.time()
        logger.info(f"Lähetetään Groq API-kysely ulko-oville mallilla {model_name}...")
        
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Groq API-kysely ulko-oville valmis {elapsed_time:.2f} sekunnissa")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                if not content:
                    logger.warning("❌ Groq API-kutsu palautti tyhjän vastauksen")
                    return []
                
                # Puhdista content ```json-merkinnöistä
                json_text = content.replace("```json", "").replace("```", "").strip()
                
                # Debug: tulosta vastaus
                logger.info(f"🔍 Groq API vastaus ulko-oville: {content[:200]}...")
                
                # Muunna vastaus UlkoOvi-olioiksi
                try:
                    ovet_data = json.loads(json_text)
                    
                    # Tarkista että ovet_data on lista
                    if not isinstance(ovet_data, list):
                        logger.warning("❌ API-vastaus ei ole lista")
                        return []
                    
                    ovet = []
                    for ovi_data in ovet_data:
                        ovi = UlkoOvi(
                            malli=ovi_data["malli"],
                            paloluokitus_EI_15=ovi_data["paloluokitus_EI_15"],
                            lukko=ovi_data["lukko"],
                            maara=ovi_data["maara"]
                        )
                        ovet.append(ovi)
                        logging.info(f"✅ Luotu ulko-ovi: {vars(ovi)}")
                        
                    logger.info(f"✅ Yhteensä {len(ovet)} ulko-ovea luotu")
                    return ovet
                except json.JSONDecodeError as e:
                    logging.error(f"❌ JSON-parsinta epäonnistui: {str(e)}")
                    logging.error(f"❌ Raw vastaus: {content[:500]}...")
                    return []
                except Exception as e:
                    logging.error(f"❌ Muu virhe: {str(e)}")
                    return []
            else:
                logger.warning("Groq API-vastaus ei sisällä choices-kenttää")
                return []
        else:
            logger.error(f"Groq API-virhe: {response.status_code} - {response.text}")
            return []
            
    except requests.exceptions.Timeout:
        logger.error("Groq API-kysely aikakatkaistu")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Groq API-kysely epäonnistui: {e}")
        return []
    except Exception as e:
        logger.error(f"Odottamaton virhe Groq API-kyselyssä: {e}")
        return []





