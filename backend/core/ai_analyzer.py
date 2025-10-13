"""
AI-analyysi moduuli
"""

import os
import sys
import time
import json

# Lisää polut
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("utils"))

from api_kyselyt import groq_api_kysely, groq_api_kysely_ulko_ovet, groq_api_kysely_nelja_parametria
from config_data import (
    PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT,
    PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON,
    PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT,
    PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_LUOKKAMUOTOON,
    PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT,
    PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT,
    PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT,
    PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON,
    PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT,
    PROMPT_KASTELLI_ULKO_OVI_TIEDOT_LUOKKAMUOTOON,
    PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT,
    PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT,
    PROMPT_POIMI_TUOTTEET_1_TXT,
    PROMPT_KASTELLI_POIMI_TUOTTEET_TXT
)
from logger_config import configure_logging
import logging

# Loggerin alustus
configure_logging()
logger = logging.getLogger(__name__)

class AIAnalyzer:
    """AI-analyysi luokka"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_sievitalo(self, cleaned_text: str) -> dict:
        """
        Analysoi Sievitalo-dokumentti
        
        Args:
            cleaned_text: Puhdistettu teksti
            
        Returns:
            Analyysitulokset sanakirjana
        """
        try:
            self.logger.info("Aloitetaan Sievitalo-analyysi...")
            
            results = {}
            
            # Ikkunat
            self.logger.info("Analysoidaan ikkunat...")
            ikkunatiedot = groq_api_kysely(PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, cleaned_text)
            ikkunat_json = groq_api_kysely(PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, ikkunatiedot)
            results['ikkunat'] = ikkunat_json
            
            # Odota ennen seuraavaa API-kutsua
            self.logger.info("⏳ Odotetaan 30 sekuntia...")
            time.sleep(30)
            
            # Ulko-ovet
            self.logger.info("Analysoidaan ulko-ovet...")
            ulko_ovet_teksti = groq_api_kysely(PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, cleaned_text)
            
            if ulko_ovet_teksti and ulko_ovet_teksti.strip():
                self.logger.info("⏳ Odotetaan 30 sekuntia...")
                time.sleep(30)
                ulko_ovet = groq_api_kysely_ulko_ovet(PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_LUOKKAMUOTOON, ulko_ovet_teksti)
                results['ulko_ovet'] = ulko_ovet
            else:
                self.logger.warning("Ulko-ovien API-kutsu palautti tyhjän vastauksen")
                results['ulko_ovet'] = []
            
            # Odota ennen seuraavaa API-kutsua
            self.logger.info("⏳ Odotetaan 30 sekuntia...")
            time.sleep(30)
            
            # Väliovet
            self.logger.info("Analysoidaan väliovet...")
            valio_ovet = groq_api_kysely(PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, cleaned_text)
            
            if valio_ovet and valio_ovet.strip():
                self.logger.info("⏳ Odotetaan 30 sekuntia...")
                time.sleep(30)
                valio_ovet = groq_api_kysely(PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT, valio_ovet)
                
                # Parsi JSON
                try:
                    json_text = valio_ovet.replace("```json", "").replace("```", "").strip()
                    data = json.loads(json_text)
                    results['valiovet'] = data.get("ovimallit", [])
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Virheellinen JSON-muoto: {e}")
                    results['valiovet'] = []
            else:
                self.logger.warning("Väliovien API-kutsu palautti tyhjän vastauksen")
                results['valiovet'] = []
            
            # Tuotteet
            self.logger.info("⏳ Odotetaan 30 sekuntia...")
            time.sleep(30)
            
            self.logger.info("Analysoidaan tuotteet...")
            from SQL_kyselyt_tuotteet_tauluun import hae_tuotteet_if_prompt_1_true
            tuotteet = hae_tuotteet_if_prompt_1_true()
            tuotteet = f"**TUOTELISTAUS START**\n{tuotteet}\n**TUOTELISTAUS END**"
            
            toimitussisalto_tuotteet = groq_api_kysely_nelja_parametria(
                PROMPT_POIMI_TUOTTEET_1_TXT, 
                cleaned_text, 
                tuotteet
            )
            results['tuotteet'] = toimitussisalto_tuotteet
            
            self.logger.info("Sievitalo-analyysi valmis")
            return results
            
        except Exception as e:
            self.logger.error(f"Virhe Sievitalo-analyysissä: {e}")
            raise
    
    def analyze_kastelli(self, cleaned_text: str) -> dict:
        """
        Analysoi Kastelli-dokumentti
        
        Args:
            cleaned_text: Puhdistettu teksti
            
        Returns:
            Analyysitulokset sanakirjana
        """
        try:
            self.logger.info("Aloitetaan Kastelli-analyysi...")
            
            results = {}
            
            # Ikkunat
            self.logger.info("Analysoidaan ikkunat...")
            ikkunatiedot = groq_api_kysely(PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT, cleaned_text)
            ikkunat_json = groq_api_kysely(PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, ikkunatiedot)
            results['ikkunat'] = ikkunat_json
            
            # Odota ennen seuraavaa API-kutsua
            self.logger.info("⏳ Odotetaan 30 sekuntia...")
            time.sleep(30)
            
            # Ulko-ovet
            self.logger.info("Analysoidaan ulko-ovet...")
            ulko_ovet_teksti = groq_api_kysely(PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT, cleaned_text)
            
            if ulko_ovet_teksti and ulko_ovet_teksti.strip():
                self.logger.info("⏳ Odotetaan 30 sekuntia...")
                time.sleep(30)
                ulko_ovet = groq_api_kysely_ulko_ovet(PROMPT_KASTELLI_ULKO_OVI_TIEDOT_LUOKKAMUOTOON, ulko_ovet_teksti)
                results['ulko_ovet'] = ulko_ovet
            else:
                self.logger.warning("Kastelli ulko-ovien API-kutsu palautti tyhjän vastauksen")
                results['ulko_ovet'] = []
            
            # Odota ennen seuraavaa API-kutsua
            self.logger.info("⏳ Odotetaan 30 sekuntia...")
            time.sleep(30)
            
            # Väliovet
            self.logger.info("Analysoidaan väliovet...")
            valio_ovet = groq_api_kysely(PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT, cleaned_text)
            
            if valio_ovet and valio_ovet.strip():
                self.logger.info("⏳ Odotetaan 30 sekuntia...")
                time.sleep(30)
                valio_ovet = groq_api_kysely(PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, valio_ovet)
                
                # Parsi JSON
                try:
                    json_text = valio_ovet.replace("```json", "").replace("```", "").strip()
                    data = json.loads(json_text)
                    results['valiovet'] = data.get("ovimallit", [])
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Virheellinen JSON-muoto: {e}")
                    results['valiovet'] = []
            else:
                self.logger.warning("Kastelli väliovien API-kutsu palautti tyhjän vastauksen")
                results['valiovet'] = []
            
            # Tuotteet
            self.logger.info("⏳ Odotetaan 30 sekuntia...")
            time.sleep(30)
            
            self.logger.info("Analysoidaan tuotteet...")
            from SQL_kyselyt_tuotteet_tauluun import hae_tuotteet_if_prompt_1_true
            tuotteet = hae_tuotteet_if_prompt_1_true()
            toimitussisalto_tuotteet = groq_api_kysely_nelja_parametria(
                PROMPT_KASTELLI_POIMI_TUOTTEET_TXT, 
                cleaned_text, 
                tuotteet
            )
            results['tuotteet'] = toimitussisalto_tuotteet
            
            self.logger.info("Kastelli-analyysi valmis")
            return results
            
        except Exception as e:
            self.logger.error(f"Virhe Kastelli-analyysissä: {e}")
            raise
    
    def analyze_document(self, cleaned_text: str, supplier: str) -> dict:
        """
        Analysoi dokumentti toimittajan mukaan
        
        Args:
            cleaned_text: Puhdistettu teksti
            supplier: Toimittaja
            
        Returns:
            Analyysitulokset sanakirjana
        """
        if supplier == "Sievitalo":
            return self.analyze_sievitalo(cleaned_text)
        elif supplier == "Kastelli":
            return self.analyze_kastelli(cleaned_text)
        else:
            raise ValueError(f"Tuntematon toimittaja: {supplier}")



