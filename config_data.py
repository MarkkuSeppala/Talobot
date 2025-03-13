#from pathlib import Path
import sys
import os
from pathlib import Path

#Lisää juurikansio Pythonin moduulihakemistoon
sys.path.append(os.path.abspath("."))
#sys.path.append(os.path.abspath("utils"))
#sys.path.append(os.path.abspath("api_kyselyt"))



# Määritä peruskansio, jossa data sijaitsee
BASE_DIR = Path(__file__).parent  # Tämä varmistaa, että polut ovat suhteellisia skriptiin

# Data-kansio
S_DIR = BASE_DIR / "data" / "s"
K_DIR = BASE_DIR / "data" / "k"
DATA_DIR = BASE_DIR / "data"
GEMINI_API_KEY = "AIzaSyADY6K_HFjgeyjr3IHHoY5UmK6hSoG_RYg"
TOIMITUSSISALTO_TXT = DATA_DIR / "toimitussisalto.txt"






#===============  SIEVITALO  polut ================#
TOIMITUSSISALTO_SIEVITALO_TXT = S_DIR / "toimitussisalto_sievitalo.txt"
PUHDISTETTU_TOIMITUSSISALTO_TXT = S_DIR / "puhdistettu_toimitussisalto.txt"
IKKUNATIEDOT_KOKONAISUUDESSA_TXT = S_DIR / "ikkunatiedot_kokonaisuudessa.txt"
IKKUNA_JSON = S_DIR / "ikkuna.json"
IKKUNA2_JSON = S_DIR / "ikkuna2.json"
ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT = S_DIR / "ulko_ovi_tiedot_kokonaisuudessa.txt"
ULKO_OVI_TIEDOT_2_JSON = S_DIR / "ulko_ovi_tiedot_2.json"
VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT = S_DIR / "valiovi_tiedot_kokonaisuudessa.txt"
#VALIOVITYYPIT_TXT = S_DIR / "valiovityypit.txt"
VALIOVITYYPIT_SIEVITALO_JSON = S_DIR / "valiovityypit_sievitalo.json"
TOIMITUSSISALTO_KOKONAISUUDESSA_TXT = S_DIR / "toimitussisalto_kokonaisuudessa_tekstina.txt"


#============== S I E V I T A L O promptit============#
PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT = S_DIR / "PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT.txt"
PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON = S_DIR / "PROMPT_SIEVITALO_RYHMITTELE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON.txt"
PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT = S_DIR / "PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT.txt"
PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT = S_DIR / "PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT.txt"
PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT = S_DIR / "PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT.txt"
PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON = S_DIR / "PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_JSON_MUOTOON.txt"









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
#VALIOVITYYPIT_KASTELLI_TXT = K_DIR / "valiovityypit_kastelli.txt"


#============== K A S T E L L I  promptit ============#
PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT = K_DIR / "PROMPT_KASTELLI_POIMI_IKKUNATIEDOT.txt"
PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON = K_DIR / "PROMPT_KASTELLI_RYHMITTELE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON.txt"
PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT = K_DIR / "PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT.txt"
PROMPT_KASTELLI_ULKO_OVI_TIEDOT_JSON_MUOTOON = K_DIR / "PROMPT_KASTELLI_ULKO_OVI_TIEDOT_JSON_MUOTOON.txt"
PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT = K_DIR / "PROMPT_KASTELLI_POIMI_VALIOVITIEDOT.txt"
PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT = K_DIR / "PROMPT_KASTELLI_ANNA_VALIOVIMALLIT.txt"



