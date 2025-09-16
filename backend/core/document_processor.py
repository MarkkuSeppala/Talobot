"""
PDF-dokumenttien käsittely
"""

import os
import sys
from pathlib import Path

# Lisää polut
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("utils"))

from utils.file_handler import muuta_pdf_ja_puhdista_teksti_docling, kirjoita_txt_tiedosto
from utils.tietosissallon_kasittely import tunnista_toimittaja
from logger_config import configure_logging
import logging

# Loggerin alustus
configure_logging()
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """PDF-dokumenttien käsittelyluokka"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_pdf(self, pdf_path: str) -> dict:
        """
        Käsittele PDF-tiedosto
        
        Args:
            pdf_path: PDF-tiedoston polku
            
        Returns:
            Sanakirja käsitellystä dokumentista
        """
        try:
            self.logger.info(f"Käsitellään PDF: {pdf_path}")
            
            # Tarkista tiedosto
            if not Path(pdf_path).exists():
                raise FileNotFoundError(f"PDF-tiedostoa ei löytynyt: {pdf_path}")
            
            # Muunna PDF tekstiksi
            self.logger.info("Muunnetaan PDF tekstiksi...")
            puhdistettu_teksti = muuta_pdf_ja_puhdista_teksti_docling(pdf_path)
            
            # Lisää viittaukset
            puhdistettu_teksti = f"**TOIMITUSSISÄLTÖ START**\n{puhdistettu_teksti}\n**TOIMITUSSISÄLTÖ END**"
            
            # Tunnista toimittaja
            self.logger.info("Tunnistetaan toimittaja...")
            toimittaja = tunnista_toimittaja(puhdistettu_teksti)
            
            # Tallenna puhdistettu teksti
            output_path = f"data/puhdistettu_toimitussisalto_{Path(pdf_path).stem}.txt"
            kirjoita_txt_tiedosto(puhdistettu_teksti, output_path)
            
            return {
                "pdf_path": pdf_path,
                "cleaned_text": puhdistettu_teksti,
                "supplier": toimittaja,
                "output_path": output_path
            }
            
        except Exception as e:
            self.logger.error(f"Virhe PDF-käsittelyssä: {e}")
            raise
    
    def validate_pdf(self, pdf_path: str) -> bool:
        """
        Tarkista PDF-tiedosto
        
        Args:
            pdf_path: PDF-tiedoston polku
            
        Returns:
            True jos tiedosto on kelvollinen
        """
        try:
            path = Path(pdf_path)
            
            # Tarkista tiedosto
            if not path.exists():
                self.logger.error(f"Tiedostoa ei löytynyt: {pdf_path}")
                return False
            
            # Tarkista tiedostopääte
            if path.suffix.lower() != '.pdf':
                self.logger.error(f"Tiedosto ei ole PDF: {pdf_path}")
                return False
            
            # Tarkista tiedostokoko
            if path.stat().st_size == 0:
                self.logger.error(f"Tiedosto on tyhjä: {pdf_path}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Virhe PDF-tarkistuksessa: {e}")
            return False



