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
DATA_DIR = BASE_DIR / "data"


# TXT- JA JSON-tiedostojen polut
IKKUNA2_JSON = S_DIR / "ikkuna2.json"
VALIOVITYYPIT_TXT = S_DIR / "valiovityypit.txt"
TOIMITUSSISALTO_KOKONAISUUDESSA_TXT = S_DIR / "toimitussisalto_kokonaisuudessa_tekstina.txt"
ULKO_OVI_TIEDOT_KOKONAISUUDESSA_TXT = S_DIR / "ulko_ovi_tiedot_kokonaisuudessa.txt"
VALIOVI_TIEDOT_KOKONAISUUDESSA_TXT = S_DIR / "valiovi_tiedot_kokonaisuudessa.txt"
IKKUNATIEDOT_KOKONAISUUDESSA_TXT = S_DIR / "ikkunatiedot_kokonaisuudessa.txt"
IKKUNA_JSON = S_DIR / "ikkuna.json"
PUHDISTETTU_TOIMITUSSISALTO_TXT = S_DIR / "puhdistettu_toimitussisalto.txt"
ULKO_OVI_TIEDOT_2_JSON = S_DIR / "ulko_ovi_tiedot_2.json"
ULKO_OVI_TIEDOT_JSON = S_DIR / "ulko_ovi_tiedot.json"
TEMP_1_TXT = S_DIR / "temp_1.txt"
TOIMITUSSISALTO_TXT = DATA_DIR / "toimitussisalto.txt"
