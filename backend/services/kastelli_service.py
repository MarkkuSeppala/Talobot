"""
Kastelli-palvelu
"""

import os
import sys

# Lisää polut
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("utils"))

from backend.core.document_processor import DocumentProcessor
from backend.core.ai_analyzer import AIAnalyzer
from SQL_kyselyt import (
    lisaa_ikkunat_kantaan,
    lisaa_ulko_ovet_kantaan,
    lisaa_valiovet_kantaan,
    lisaa_toimitussisalto_tuotteet_kantaan
)
from utils.tietosissallon_kasittely import poista_json_merkinta
from logger_config import configure_logging
import logging

# Loggerin alustus
configure_logging()
logger = logging.getLogger(__name__)

class KastelliService:
    """Kastelli-palvelu"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.document_processor = DocumentProcessor()
        self.ai_analyzer = AIAnalyzer()
    
    def process_document(self, pdf_path: str, toimitussisalto_id: int) -> dict:
        """
        Käsittele Kastelli-dokumentti
        
        Args:
            pdf_path: PDF-tiedoston polku
            toimitussisalto_id: Toimitussisallon ID
            
        Returns:
            Käsittelytulokset sanakirjana
        """
        try:
            self.logger.info(f"Käsitellään Kastelli-dokumentti: {pdf_path}")
            
            # Käsittele PDF
            doc_result = self.document_processor.process_pdf(pdf_path)
            
            # Analysoi AI:lla
            analysis_result = self.ai_analyzer.analyze_kastelli(doc_result['cleaned_text'])
            
            # Tallenna tietokantaan
            self.logger.info("Tallennetaan tulokset tietokantaan...")
            
            # Ikkunat
            if analysis_result.get('ikkunat'):
                lisaa_ikkunat_kantaan(analysis_result['ikkunat'], toimitussisalto_id)
                self.logger.info(f"Tallennettu {len(analysis_result['ikkunat'])} ikkunaa")
            
            # Ulko-ovet
            if analysis_result.get('ulko_ovet'):
                lisaa_ulko_ovet_kantaan(analysis_result['ulko_ovet'], toimitussisalto_id)
                self.logger.info(f"Tallennettu {len(analysis_result['ulko_ovet'])} ulko-ovea")
            
            # Väliovet
            if analysis_result.get('valiovet'):
                lisaa_valiovet_kantaan(analysis_result['valiovet'], toimitussisalto_id)
                self.logger.info(f"Tallennettu {len(analysis_result['valiovet'])} väliovia")
            
            # Tuotteet
            if analysis_result.get('tuotteet'):
                tuotteet_puhdistettu = poista_json_merkinta(analysis_result['tuotteet'])
                lisaa_toimitussisalto_tuotteet_kantaan(tuotteet_puhdistettu, toimitussisalto_id)
                self.logger.info("Tuotteet tallennettu")
            
            return {
                "success": True,
                "supplier": "Kastelli",
                "toimitussisalto_id": toimitussisalto_id,
                "ikkunat_count": len(analysis_result.get('ikkunat', [])),
                "ulko_ovet_count": len(analysis_result.get('ulko_ovet', [])),
                "valiovet_count": len(analysis_result.get('valiovet', [])),
                "tuotteet_analyzed": bool(analysis_result.get('tuotteet'))
            }
            
        except Exception as e:
            self.logger.error(f"Virhe Kastelli-dokumentin käsittelyssä: {e}")
            raise



