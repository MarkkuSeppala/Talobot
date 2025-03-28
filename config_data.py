#from pathlib import Path
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Ladataan ympäristömuuttujat .env-tiedostosta
load_dotenv()


#Lisää juurikansio Pythonin moduulihakemistoon
sys.path.append(os.path.abspath("."))

print(" jos seuraava true, sitten väärin")
print(os.path.exists("/persistent_data"))

# Määritä peruskansio, jossa data sijaitsee
BASE_DIR = Path(__file__).parent  # Tämä varmistaa, että polut ovat suhteellisia skriptiin
#BASE_DIR = Path("C:/Users/Public/testibot/Talobot")

# Hae juurihakemisto riippuen ympäristöstä
if os.path.exists("/persistent_data") and not os.path.exists("C:/persistent_data"):  # 🔹 Renderin polku
    PERSISTENT_DISK = Path("/persistent_data")
    DATA_DIR = PERSISTENT_DISK / "data"
    print("📌 PERSISTENT_DISK: rivi 20")
else:  # 🔹 Windowsin polku
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    print("📌 BASE_DIR: rivi 24")

S_DIR = DATA_DIR / "s"
K_DIR = DATA_DIR / "k"
D_DIR = DATA_DIR / "d"


# Ladataan ympäristömuuttujat .env-tiedostosta
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



TOIMITUSSISALTO_TXT = DATA_DIR / "toimitussisalto.txt"
UPLOAD_FOLDER_DATA = DATA_DIR / "ladatut_toimitussisallot"

print("📌 BASE_DIR:", BASE_DIR.resolve())
#print("📌 PERSISTENT_DISK:", PERSISTENT_DISK.resolve())
print("📌 DATA_DIR:", DATA_DIR.resolve())
print("📌 UPLOAD_FOLDER_DATA:", UPLOAD_FOLDER_DATA.resolve())


#===============  SIEVITALO  polut ================#
TOIMITUSSISALTO_SIEVITALO_TXT = S_DIR / "toimitussisalto_sievitalo.txt"
PUHDISTETTU_TOIMITUSSISALTO_TXT = S_DIR / "puhdistettu_toimitussisalto.txt"
IKKUNATIEDOT_KOKONAISUUDESSA_TXT = S_DIR / "ikkunatiedot_kokonaisuudessa.txt"
IKKUNA_JSON = S_DIR / "ikkuna.json"
IKKUNA2_JSON = S_DIR / "ikkuna2.json"
ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT = S_DIR / "ulko_ovi_tiedot_kokonaisuudessa.txt"
ULKO_OVI_TIEDOT_2_JSON = S_DIR / "ulko_ovi_tiedot_2.json"
VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT = S_DIR / "valiovi_tiedot_kokonaisuudessa.txt"
VALIOVITYYPIT_SIEVITALO_JSON = S_DIR / "valiovityypit_sievitalo.json"



#============== S I E V I T A L O promptit============#
PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT = S_DIR / "prompt_sievitalo_poimi_ikkunatiedot.txt"
PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON = S_DIR / "prompt_sievitalo_ryhmittele_valitut_ikkunatiedot_json_muotoon.txt"
PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT = S_DIR / "prompt_sievitalo_poimi_ulko_ovi_tiedot.txt"
PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT = S_DIR / "prompt_sievitalo_anna_valiovimallit.txt"
PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT = S_DIR / "prompt_sievitalo_poimi_valiovtiedot.txt"
PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON = S_DIR / "prompt_sievitalo_ulko_ovi_tiedot_json_muotoon.txt"









#===============  KASTELLI  polut ================#
TOIMITUSSISALTO_KASTELLI_TXT = K_DIR / "toimitussisalto_kastelli.txt"
PUHDISTETTU_TOIMITUSSISALTO_KASTELLI_TXT = K_DIR / "puhdistettu_toimitussisalto_kastelli.txt"
IKKUNATIEDOT_KASTELLI_KOKONAISUUDESSA_TXT = K_DIR / "ikkunatiedot_kastelli_kokonaisuudessa.txt"
IKKUNA_KASTELLI_JSON = K_DIR / "ikkuna_kastelli.json"
IKKUNA2_KASTELLI_JSON = K_DIR / "ikkuna2_kastelli.json"
ULKO_OVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT = K_DIR / "ulko_ovi_tiedot_kastelli_kokonaisuudessa.txt"
ULKO_OVI_TIEDOT_KASTELLI_2_JSON = K_DIR / "ulko_ovi_tiedot_2_kastelli.json"
VALIOVI_TIEDOT_KASTELLI_KOKONAISUUDESSA_TXT = K_DIR / "valiovi_tiedot_kastelli_kokonaisuudessa.txt"
VALIOVITYYPIT_KASTELLI_JSON = K_DIR / "valiovityypit_kastelli.json"



#============== K A S T E L L I  promptit ============#
PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT = K_DIR / "prompt_kastelli_poimi_ikkunatiedot.txt"
PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON = K_DIR / "prompt_kastelli_ryhmittele_valitut_ikkunatiedot_json_muotoon.txt"
PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT = K_DIR / "prompt_kastelli_poimi_ulko_ovi_tiedot.txt"
PROMPT_KASTELLI_ULKO_OVI_TIEDOT_JSON_MUOTOON = K_DIR / "prompt_kastelli_ulko_ovi_tiedot_json_muotoon.txt"
PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT = K_DIR / "prompt_kastelli_poimi_valiovitiedot.txt"
PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT = K_DIR / "prompt_kastelli_anna_valiovimallit.txt"








#===============  DESIGNTALO  polut ================#
TOIMITUSSISALTO_DESIGNTALO_TXT = D_DIR / "toimitussisalto_designtalo.txt"
PUHDISTETTU_TOIMITUSSISALTO_DESIGNTALO_TXT = D_DIR / "puhdistettu_toimitussisalto_designtalo.txt"
IKKUNATIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT = D_DIR / "ikkunatiedot_designtalo_kokonaisuudessa.txt"
IKKUNA_DESIGNTALO_JSON = D_DIR / "ikkuna_designtalo.json"
IKKUNA2_DESIGNTALO_JSON = D_DIR / "ikkuna2_designtalo.json"
ULKO_OVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT = D_DIR / "ulko_ovi_tiedot_designtalo_kokonaisuudessa.txt"
ULKO_OVI_TIEDOT_DESIGNTALO_2_JSON = D_DIR / "ulko_ovi_tiedot_2_designtalo.json"
VALIOVI_TIEDOT_DESIGNTALO_KOKONAISUUDESSA_TXT = D_DIR / "valiovi_tiedot_designtalo_kokonaisuudessa.txt"
VALIOVITYYPIT_DESIGNTALO_JSON = D_DIR / "valiovityypit_designtalo.json"



#============== DESIGNTALO  promptit ============#
PROMPT_DESIGNTALO_POIMI_IKKUNATIEDOT_TXT = D_DIR / "prompt_designtalo_poimi_ikkunatiedot.txt"
PROMPT_DESIGNTALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON = D_DIR / "prompt_designtalo_ryhmittele_valitut_ikkunatiedot_json_muotoon.txt"
PROMPT_DESIGNTALO_POIMI_ULKO_OVI_TIEDOT_TXT = D_DIR / "prompt_designtalo_poimi_ulko_ovi_tiedot.txt"
PROMPT_DESIGNTALO_ULKO_OVI_TIEDOT_JSON_MUOTOON = D_DIR / "prompt_designtalo_ulko_ovi_tiedot_json_muotoon.txt"
PROMPT_DESIGNTALO_POIMI_VALIOVITIEDOT_TXT = D_DIR / "prompt_designtalo_poimi_valiovitiedot.txt"
PROMPT_DESIGNTALO_ANNA_VALIOVIMALLIT_TXT = D_DIR / "prompt_designtalo_anna_valiovimallit.txt"
