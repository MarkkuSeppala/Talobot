import os
import sys
import re
import fitz  # PyMuPDF
import google.generativeai as genais
from datetime import datetime
#from utils.file_handler import tallenna_pdf_tiedosto, muuta_pdf_tekstiksi, lue_txt_tiedosto, lue_json_tiedosto, kirjoita_txt_tiedostoon, normalisoi_ulko_ovet, kirjoita_json_tiedostoon
import json
from logger_config import configure_logging
import logging
from docling.document_converter import DocumentConverter




sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

sys.path.append("C:/Talobot")
sys.path.append(os.path.abspath("utils"))  # Lisää utils-kansion polku moduulihakemistoksi
sys.path.append(os.path.abspath("data"))  # Lisää utils-kansion polku moduulihakemistoksi


#from config_data import TOIMITUSSISALTO_TXT


# Logger alustus
configure_logging()
logger = logging.getLogger(__name__)


def muuta_pdf_ja_puhdista_teksti_docling(pdf_file):
    print("tietosissallon_kasittely.py 30")
    source = pdf_file  # document per local path or URL
    converter = DocumentConverter()
    result = converter.convert(source)
    text = result.document.export_to_markdown()
    print("tietosissallon_kasittely.py 35")
    text = str(text)
    print("tietosissallon_kasittely.py 37")
    return text

# Puhdistaa tekoälyn palauttaman tekstin (poistaa markdown ```json -merkinnät)
def puhdista_tekoalyn_palauttama_json_response_json(response_text: str):
    """
    Puhdistaa tekoälyn palauttaman tekstin (poistaa markdown ```json -merkinnät)
    ja muuntaa sen Python-objektiksi.

    :param response_text: Tekoälyn vastaus merkkijonona.
    :return: Python-objekti (esim. dict tai list), joka vastaa JSON-rakennetta.
    :raises json.JSONDecodeError: Jos sisältö ei ole kelvollista JSON:ia.
    """
    # Poistetaan kaikki mahdolliset markdown-merkinnät ja tyhjät rivit
    cleaned = re.sub(r"```(?:json)?\s*|\s*```", "", response_text).strip()

    # Tulostetaan puhdistettu JSON-testi (debuggausta varten)
    print("Puhdistettu JSON-teksti:\n", cleaned)

    # Muunnetaan JSONiksi
    return json.loads(cleaned)

def muuta_tekstiksi(pdf_file, tiedostopolku):
    """
    Muuntaa PDF:n tekstiksi ja tallentaa annetulle tiedostopolulle.
    
    :param pdf_file: PDF-tiedosto, joka muunnetaan tekstiksi.
    :param tiedostopolku: Polku, johon muunnettu teksti tallennetaan.
    """
    def pdf_to_text(pdf):
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            return "".join(page.get_text() for page in doc)

    teksti = pdf_to_text(pdf_file)

    # Varmista, että kohdekansion olemassaolo
    os.makedirs(os.path.dirname(tiedostopolku), exist_ok=True)
    
    # Kirjoita teksti tiedostoon
    with open(tiedostopolku, "w", encoding="utf-8") as tiedosto:
        tiedosto.write(teksti)

    return tiedostopolku  # Palauttaa polun onnistuneen tallennuksen jälkeen

#==================================================================================================#

#clean_text poistaa turhat erikoismerkit, korjaa numeromuodot ja selkeyttää tekstiä. Lukee tiedoston ja kirjoittaa sen uudelleen.

def puhdista_ja_kirjoita_tiedosto(input_tiedostopolku, output_tiedostopolku):
    """
    Lukee tekstin annetusta tiedostosta, puhdistaa sen ja tallentaa puhdistetun version.
    
    :param input_tiedostopolku: Polku, josta alkuperäinen teksti luetaan.
    :param output_tiedostopolku: Polku, johon puhdistettu teksti tallennetaan.
    """
    # Lue alkuperäinen teksti tiedostosta
    with open(input_tiedostopolku, "r", encoding="utf-8") as tiedosto:
        teksti = tiedosto.read()
    
    text = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s@._,-:/]', '', sisalto)  # Poistetaan erikoismerkit (paitsi @, ., _ ja ,)
    text = re.sub(r'\s+', ' ', text).strip()  # Poistetaan ylimääräiset välilyönnit
    text = re.sub(r'(\d{1,3})\s(\d{3})', r'\1\2', text)  # Korjataan hajonneet numerot, esim. 173 500 € -> 173500 €
    text = text.replace("•", "-")  # Korvataan listapallot viivoilla
    
    # Varmista, että kohdekansion olemassaolo
    os.makedirs(os.path.dirname(output_tiedostopolku), exist_ok=True)
    
    # Kirjoita puhdistettu teksti tiedostoon
    with open(output_tiedostopolku, "w", encoding="utf-8") as tiedosto:
        tiedosto.write(puhdistettu_teksti)
    
    return output_tiedostopolku  # Palauttaa polun onnistuneen tallennuksen jälkeen

#==================================================================================================#

def puhdista_teksti(text) -> str:
    """Poistaa turhat erikoismerkit, korjaa numeromuodot ja selkeyttää tekstiä."""

    if not isinstance(text, str):
        logging.warning(f"Varoitus: Teksti ei ole string-muodossa vaan {type(text)}")
        text = str(text) if text is not None else ""
   
    # Säilytetään kaikki kirjaimet (mukaan lukien skandit), numerot ja tietyt erikoismerkit
    text = re.sub(r'[^a-zA-ZåäöÅÄÖüÜß\d\s@._,\-:/]', '', text)  # Huomaa \- viivan edessä
    
    # Poistetaan ylimääräiset välilyönnit
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Korjataan hajonneet numerot, esim. 173 500 € -> 173500 €
    text = re.sub(r'(\d{1,3})\s(\d{3})', r'\1\2', text)
    
    # Korvataan listapallot viivoilla
    text = text.replace("•", "-")

    logger.info("Teksti puhdistettu")
    return text

#==================================================================================================#

#clean_text poistaa turhat erikoismerkit, korjaa numeromuodot ja selkeyttää tekstiä.
#Saa tekstin, kirjoittaa annettuun polkuun
# def clean_text2(text, korjattu_tiedosto):
 
    
#     #if os.path.exists(tiedostopolku):
#     #    with open(tiedostopolku, 'r', encoding='utf-8') as tiedosto:
#     #        sisalto = tiedosto.read()

#     text = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß\s@._,-:/]', '', text)  # Poistetaan erikoismerkit (paitsi @, ., _ ja ,)
#     text = re.sub(r'\s+', ' ', text).strip()  # Poistetaan ylimääräiset välilyönnit
#     text = re.sub(r'(\d{1,3})\s(\d{3})', r'\1\2', text)  # Korjataan hajonneet numerot, esim. 173 500 € -> 173500 €
#     text = text.replace("•", "-")  # Korvataan listapallot viivoilla
    

#     with open(korjattu_tiedosto, "w", encoding="utf-8") as tiedosto:
#         tiedosto.write(text)




# ------- Tunnistaa toimittajan nimen toimitussisällöstä -------

def tunnista_toimittaja(teksti):
    """Etsii toimittajan nimen toimitussisällöstä"""
    #toimittajat = ["Sievitalo", "Kastelli"]
    toimittajat = ["Sievitalo", "Kastelli", "Designtalo"]
    for nimi in toimittajat:
        if nimi in teksti:
            return nimi
    return None





# **Poista sanat tekstistä**
def poista_sanat_tekstista(toimitussisältö_kokonaisuudessa_tekstina):
    #tiedostopolku = "data/s/toimitussisältö_kokonaisuudessa_tekstina.txt"
    #korjattu_tiedosto = "data/s/puhdistettu_toimitussisalto.txt"
   
    #print(toimitussisältö_kokonaisuudessa_tekstina)
    
    poistettavat_sanat = [
        "Sievitalo Oy", "Mestarintie 6", "TOIMITUSTAPASELOSTE", "67101 KOKKOLA",
        "Puh. 06 822 1111", "Fax 06 822 1112", "www.sievitalo.fi", "Y-tunnus: 2988131-5", "RAKENNE- JA"
    ]

    if os.path.exists(toimitussisältö_kokonaisuudessa_tekstina):
        with open(toimitussisältö_kokonaisuudessa_tekstina, 'r', encoding='utf-8') as tiedosto:
            sisalto = tiedosto.read()

        puhdistettu_sisalto = poista_sanat_tekstista2(sisalto, poistettavat_sanat)

    return puhdistettu_sisalto


def poista_sanat_tekstista2(teksti, poistettavat_sanat):
    for sana in poistettavat_sanat:
        teksti = teksti.replace(sana, "")
    teksti = re.sub(r'TOIMITUSTAPASELOSTE\s+\d+', '', teksti)
    teksti = re.sub(r'^\d{1,2}$', '', teksti, flags=re.MULTILINE)
    return teksti



# Avaa ikkuna_json.txt -tiedostoon., asettaa jokaisen ikkunan omalle riville ja muuttaa ikkunamitat millimetreiksi.
# Tallettaa lopuksi ikkuna_json_2.txt -tiedostoon.

def sievitalo_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(ikkuna_json, ikkuna2_json):
    print("Käsitellään Sievitalon ikkunat")
    print("Input ikkuna_json:", ikkuna_json)
    print("Output polku:", ikkuna2_json)
    return _kasittele_ikkunat(ikkuna_json, ikkuna2_json, kerroin=100)

def kastelli_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(ikkuna_json, ikkuna2_json):
    print("Käsitellään Kastellin ikkunat")
    return _kasittele_ikkunat(ikkuna_json, ikkuna2_json, kerroin=1)  # Kastelli käyttää millimetrejä

def designtalo_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(ikkuna_json, ikkuna2_json):
    print("Käsitellään Designtalon ikkunat")
    return _kasittele_ikkunat(ikkuna_json, ikkuna2_json, kerroin=1)  # Designtalo käyttää millimetrejä


def _kasittele_ikkunat(ikkuna_json, ikkuna2_json, kerroin):
    """Yhteinen käsittelyfunktio kaikille ikkunoille"""
    try:
        # Jos ikkuna_json on merkkijono, muunnetaan se Python-objektiksi
        if isinstance(ikkuna_json, str):
            try:
                ikkuna_json = json.loads(ikkuna_json)
                print("JSON parsittu onnistuneesti")
            except json.JSONDecodeError as e:
                print(f"Virhe JSON:in jäsentämisessä: {e}")
                return []

        output_json = []
        print("ikkuna_json tyyppi:", type(ikkuna_json))
        print("ikkuna_json sisältö:", ikkuna_json)
        
        if not ikkuna_json:
            print("Varoitus: ikkuna_json on tyhjä")
            return []

        for item in ikkuna_json:
            try:
                print("Käsitellään item:", item)
                leveys, korkeus = map(int, item["koko"].split("x"))
                print(f"Leveys: {leveys}, Korkeus: {korkeus}")
                
                leveys_mm = leveys * kerroin
                korkeus_mm = korkeus * kerroin
                mm_koko = f"{leveys_mm}x{korkeus_mm}"

                for _ in range(item["kpl"]):
                    output_json.append({
                        "koko": item["koko"],
                        "mm_koko": mm_koko,
                        "leveys_mm": leveys_mm,
                        "turvalasi": item["turvalasi"],
                        "välikarmi": item["välikarmi"],
                        "sälekaihtimet": item["sälekaihtimet"]
                    })
            except Exception as e:
                print(f"Virhe käsiteltäessä ikkunaa {item}: {e}")
                continue

        print("output_json 231", output_json)
        output_json = sorted(output_json, key=lambda x: x["leveys_mm"])
        
        for item in output_json:
            del item["leveys_mm"]
            
        print("output_json 232", output_json)
        kirjoita_json_tiedostoon(output_json, ikkuna2_json)
        return output_json
        
    except Exception as e:
        print(f"Virhe _kasittele_ikkunat-funktiossa: {e}")
        return []


#============== K A S T E L L I ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


def  kastelli_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(ikkuna_json, ikkuna2_json):
    output_json = []

    ikkuna_json = lue_json_tiedosto(ikkuna_json)
    for item in ikkuna_json:
        leveys, korkeus = map(int, item["koko"].split("x"))  # Muutetaan mitat kokonaisluvuiksi (dm)
        
        # Muunnetaan mitat millimetreiksi
        leveys_mm = leveys * 1
        korkeus_mm = korkeus * 1
        mm_koko = f"{leveys_mm}x{korkeus_mm}"

        for _ in range(item["kpl"]):
            output_json.append({
                "koko": item["koko"],  # Alkuperäinen koko dm
                "mm_koko": mm_koko,  # Muunnettu mm
                "leveys_mm": leveys_mm,  # Tarvitaan lajittelua varten
                "turvalasi": item["turvalasi"],
                "välikarmi": item["välikarmi"],
                "sälekaihtimet": item["sälekaihtimet"]
            })

    # **Lajitellaan lista leveyden mukaan pienimmästä suurimpaan**
    output_json = sorted(output_json, key=lambda x: x["leveys_mm"])

    # Poistetaan lajittelua varten lisätty "leveys_mm" ennen tallennusta
    for item in output_json:
        del item["leveys_mm"]

    #print(output_json)
    kirjoita_json_tiedostoon(output_json, ikkuna2_json)
    # Tallennetaan JSON-tiedostoon
    #with open("data/s/ikkuna_json_2.txt", "w", encoding="utf-8") as tiedosto:
    #    json.dump(output_json, tiedosto, ensure_ascii=False, indent=4)




#============== D E S I G N T A L O ============#
#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


def  designtalo_jokainen_ikkuna_omalle_riveille_ja_koko_millimetreiksi(ikkuna_json, ikkuna2_json):
    output_json = []

    ikkuna_json = lue_json_tiedosto(ikkuna_json)
    for item in ikkuna_json:
        leveys, korkeus = map(int, item["koko"].split("x"))  # Muutetaan mitat kokonaisluvuiksi (dm)
        
        # Muunnetaan mitat millimetreiksi
        leveys_mm = leveys * 1
        korkeus_mm = korkeus * 1
        mm_koko = f"{leveys_mm}x{korkeus_mm}"

        for _ in range(item["kpl"]):
            output_json.append({
                "koko": item["koko"],  # Alkuperäinen koko dm
                "mm_koko": mm_koko,  # Muunnettu mm
                "leveys_mm": leveys_mm,  # Tarvitaan lajittelua varten
                "turvalasi": item["turvalasi"],
                "välikarmi": item["välikarmi"],
                "sälekaihtimet": item["sälekaihtimet"]
            })

    # **Lajitellaan lista leveyden mukaan pienimmästä suurimpaan**
    output_json = sorted(output_json, key=lambda x: x["leveys_mm"])

    # Poistetaan lajittelua varten lisätty "leveys_mm" ennen tallennusta
    for item in output_json:
        del item["leveys_mm"]

    #print(output_json)
    kirjoita_json_tiedostoon(output_json, ikkuna2_json)
    # Tallennetaan JSON-tiedostoon
    #with open("data/s/ikkuna_json_2.txt", "w", encoding="utf-8") as tiedosto:
    #    json.dump(output_json, tiedosto, ensure_ascii=False, indent=4)

#--------- lisaa_toimitussisalto_merkinta()
# def lisaa_toimitussisalto_merkinta(text: str) -> str:
#     """
#     Lisää toimitussisältö-merkinnät puhdistetun tekstin ympärille.
    
#     Args:
#         text (str): Puhdistettu teksti puhdista_teksti-funktiosta
        
#     Returns:
#         str: Teksti merkintöjen kanssa
#     """
   
#     return f"**TOIMITUSSISÄLTÖ START**\n{text}\n**TOIMITUSSISÄLTÖ END**"



#------------------ poista_json_merkinta()
def poista_json_merkinta(text: str) -> str:
    """
    Poistaa tekstistä ```json merkinnän alusta ja ``` merkinnän lopusta.
    
    Args:
        text (str): Teksti, josta merkinnät poistetaan
        
    Returns:
        str: Teksti ilman json-merkintöjä
    """
    # Poistetaan ```json alusta
    if text.startswith("```json"):
        text = text[7:]  # 7 merkkiä: ```json
        
    # Poistetaan ``` lopusta - käytetään replace() metodia
    text = text.replace("```", "")
        
    return text.strip()  # Poistetaan myös mahdolliset ylimääräiset välilyönnit

#
def parsi_tuote_json(input_json):
    """
    Suodattaa JSON-tiedostosta vain id, tuote, tarkenne_yleinen ja tarkenne_sievitalo -kentät.
    """
    try:
        # Muunna JSON-merkkijono listaksi
        data_list = json.loads(input_json)
        
        tulos = []
        for item in data_list:
            suodatettu_item = {
                "id": item["id"],
                "tuote": item["tuote"],
                "tarkenne_yleinen": item["tarkenne_yleinen"],
                "tarkenne_sievitalo": item["tarkenne_sievitalo"]
            }
            tulos.append(suodatettu_item)
        
        # Muunna suodatettu data takaisin JSON-muotoon
        suodatettu_json = json.dumps(tulos, ensure_ascii=False, indent=4)
        
        return suodatettu_json

    except Exception as e:
        print(f"Virhe JSON-tiedoston käsittelyssä: {str(e)}")
        return None

#----------- minka_muotoinen_parametri()
def minka_muotoinen_parametri(parametri):
    if isinstance(parametri, dict):
        print("Sain sanakirjan (dict).")
    elif isinstance(parametri, str):
        print("Sain merkkijonon (str).")
    elif isinstance(parametri, list):
        print("Sain listan.")
    else:
        print("Sain jotain muuta:", type(parametri))

# """Puhdistaa tekstin tiedostokirjoitusta varten poistamalla tai korvaamalla virheelliset merkit."""
def puhdista_teksti_tiedostokirjoitusta_varten(text):
   
    if not isinstance(text, str):
        return str(text) if text is not None else ""
    
    # Poista mahdolliset control-merkit jotka voivat häiritä tiedostokirjoitusta
    import re
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    return text