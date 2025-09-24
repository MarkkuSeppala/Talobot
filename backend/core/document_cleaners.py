"""
Toimittajakohtaiset dokumenttien puhdistusluokat
"""
import re
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path

# Tuodaan yhteiset funktiot
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from shared.tietosissallon_kasittely import muuta_pdf_ja_puhdista_teksti_docling

logger = logging.getLogger(__name__)


class DocumentCleaner(ABC):
    """Abstrakti puhdistusluokka toimittajille"""
    
    @abstractmethod
    def clean_document(self, pdf_path: str) -> str:
        """Puhdistaa dokumentin toimittajakohtaisesti"""
        pass
    
    @abstractmethod
    def get_supplier_name(self) -> str:
        """Palauttaa toimittajan nimen"""
        pass
    
    def _add_markers(self, text: str) -> str:
        """Lisää toimitussisältö-tunnisteet"""
        return f"**TOIMITUSSISÄLTÖ START**\n{text}\n**TOIMITUSSISÄLTÖ END**"


class SievitaloCleaner(DocumentCleaner):
    """Sievitalo-kohtainen puhdistus"""
    
    def clean_document(self, pdf_path: str) -> str:
        """Puhdistaa Sievitalo-dokumentin"""
        logger.info("Puhdistetaan Sievitalo-dokumentti...")
        
        # Muunna PDF tekstiksi
        text = muuta_pdf_ja_puhdista_teksti_docling(pdf_path)
        
        # Sievitalo-kohtaiset puhdistukset
        text = self._remove_sievitalo_specific_content(text)
        text = self._format_sievitalo_structure(text)
        text = self._clean_common_issues(text)
        
        return self._add_markers(text)
    
    def _remove_sievitalo_specific_content(self, text: str) -> str:
        """Poistaa Sievitalo-kohtaisia elementtejä"""
        sievitalo_patterns = [
            r"Sievitalo Oy.*?Y-tunnus: \d+-\d+",
            r"TOIMITUSTAPASELOSTE\s+\d+",
            r"Mestarintie 6.*?www\.sievitalo\.fi",
            r"Puh\. 06 822 1111.*?Fax 06 822 1112",
            r"67101 KOKKOLA"
        ]
        
        for pattern in sievitalo_patterns:
            text = re.sub(pattern, "", text, flags=re.DOTALL)
        
        return text
    
    def _format_sievitalo_structure(self, text: str) -> str:
        """Muotoilee Sievitalo-kohtaisen rakenteen"""
        # Korjaa Sievitalo-kohtaisia muotoiluja
        text = re.sub(r'•', '-', text)  # Listapallot viivoiksi
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Poista ylimääräiset rivit
        return text
    
    def _clean_common_issues(self, text: str) -> str:
        """Puhdistaa yleisiä ongelmia"""
        # Poista ylimääräiset välilyönnit
        text = re.sub(r'\s+', ' ', text)
        # Korjaa hajonneet numerot
        text = re.sub(r'(\d{1,3})\s(\d{3})', r'\1\2', text)
        return text.strip()
    
    def get_supplier_name(self) -> str:
        return "Sievitalo"


class KastelliCleaner(DocumentCleaner):
    """Kastelli-kohtainen puhdistus - perusversio"""
    
    def clean_document(self, pdf_path: str) -> str:
        """Puhdistaa Kastelli-dokumentin"""
        logger.info("Puhdistetaan Kastelli-dokumentti...")
        
        # Muunna PDF tekstiksi
        text = muuta_pdf_ja_puhdista_teksti_docling(pdf_path)
        
        # Erota ja puhdista ikkunatiedot
        text = self._extract_and_clean_window_section(text)
        
        # Kastelli-kohtaiset puhdistukset
        text = self._remove_kastelli_specific_content(text)
        text = self._format_kastelli_structure(text)
        text = self._clean_common_issues(text)
        
        return self._add_markers(text)
    
    def _extract_and_clean_window_section(self, text: str) -> str:
        """Erottaa ja puhdistaa ikkunatietojen osan"""
        logger.info("Erotetaan ja puhdistetaan ikkunatiedot...")

        # Etsi kaikki ikkunatiedot
        window_matches = list(re.finditer(r'Nro:\s*\n?\s*\d+', text))
        if not window_matches:
            logger.warning("Ikkunatietoja ei löytynyt")
            return text

        logger.info(f"Löytyi {len(window_matches)} ikkunatietoa")

        # Poista yleiset ohjeet koko dokumentista ensin
        text = self._remove_general_instructions(text)

        # Erota ikkunatiedot omiksi riveikseen
        text = self._extract_window_section_from_text(text)

        return text
    
    def _format_window_entries(self, text: str) -> str:
        """Muotoilee ikkunatiedot omiksi riveikseen"""
        logger.info("Muotoillaan ikkunatiedot omiksi riveikseen...")
        
        # Etsi ikkunatietojen osa
        window_start = re.search(r'Nro:\s*\d+', text)
        if not window_start:
            return text
        
        # Etsi ikkunatietojen loppu
        window_end = None
        for match in re.finditer(r'Nro:\s*\d+', text):
            window_end = match.end()
        
        if not window_end:
            return text
        
        # Erota ikkunatiedot
        before_windows = text[:window_start.start()]
        window_section = text[window_start.start():window_end]
        after_windows = text[window_end:]
        
        # Muotoile ikkunatiedot
        formatted_windows = self._format_individual_windows(window_section)
        
        return before_windows + formatted_windows + after_windows
    
    def _format_individual_windows(self, window_section: str) -> str:
        """Muotoilee yksittäiset ikkunatiedot"""
        # Etsi kaikki ikkunatiedot
        windows = []

        # Etsi ikkunatiedot regex:llä (myös rivinvaihdon kanssa)
        window_pattern = r'Nro:\s*\n?\s*(\d+).*?(?=Nro:\s*\n?\s*\d+|$)'
        matches = re.finditer(window_pattern, window_section, re.DOTALL)

        for match in matches:
            window_text = match.group(0).strip()
            if window_text:
                # Muotoile ikkunatiedot ilman yleisohjeiden poistamista
                formatted_window = self._format_single_window(window_text)
                windows.append(formatted_window)

        return '\n\n'.join(windows)
    
    def _extract_window_section_from_text(self, text: str) -> str:
        """Erottaa ikkunatietojen osan tekstistä"""
        # Etsi kaikki ikkunatiedot
        window_matches = list(re.finditer(r'Nro:\s*\n?\s*\d+', text))
        if not window_matches:
            return text

        logger.info(f"Löytyi {len(window_matches)} ikkunatietoa")

        # Erota ikkunatiedot omiksi riveikseen
        formatted_windows = self._format_individual_windows(text)

        return formatted_windows
    
    def _format_single_window(self, window_text: str) -> str:
        """Muotoilee yksittäisen ikkunan tiedot"""
        # Etsi Nro ja Tyyppi
        nro_match = re.search(r'Nro:\s*(\d+)', window_text)
        tyyppi_match = re.search(r'Tyyppi:\s*([^\n]+)', window_text)
        
        if not nro_match:
            return window_text
        
        nro = nro_match.group(1)
        tyyppi = tyyppi_match.group(1).strip() if tyyppi_match else ""
        
        # Muotoile ikkunatiedot
        formatted = f"Nro: {nro}"
        if tyyppi:
            formatted += f"\nTyyppi: {tyyppi}"
        
        # Lisää muut tiedot
        remaining_text = window_text[nro_match.end():]
        if tyyppi_match:
            remaining_text = remaining_text[tyyppi_match.end():]
        
        # Puhdista ja lisää muut tiedot
        remaining_text = re.sub(r'\s+', ' ', remaining_text).strip()
        if remaining_text:
            formatted += f"\n{remaining_text}"
        
        return formatted
    
    def _remove_general_instructions(self, text: str) -> str:
        """Poistaa yleiset ohjeet ikkunatietojen keskeltä"""
        logger.info("Poistetaan yleiset ohjeet ikkunatietojen keskeltä...")
        
        # Poista yleiset ohjeet yksinkertaisilla regex-käännöksillä
        general_patterns = [
            # Pitkä yleisohje-kappale (korjattu regex)
            r'Toimittamamme ikkunat ovat viranomaismääräysten mukaiset.*?aikatauluun\.',
            # Lyhyemmät ohjeet
            r'o Kätisyydet määräytyvät sisäpuolelta katsottuna\.',
            r'o Ikkunoiden ominaisuuksiin saattaa liittyä huurtumista tietyissä olosuhteissa\.',
            r'o Ikkunan lämmöneristävyyden parantuessa huurtumisriski kasvaa\.',
            r'o Sälekaihtimia ei ole saatavilla palo-, vino- ja muihin erikoisikkunoihin\.',
            r'o Laatupalaveri 1:n jälkeen tehtävistä muutoksista veloitamme käsittelymaksun 300 e.*?aikatauluun\.',
            # Muut yleiset ohjeet
            r'saranat hyttyspuite H - sälekaihdin S - tuuletusluukku TL - tuuletusheloitu pitkäsuljin T -',
            # Yhdistetty pitkä rivi (korjattu)
            r'Toimittamamme ikkunat ovat viranomaismääräysten mukaiset.*?aikatauluun\.',
            r'Kätisyydet määräytyvät sisäpuolelta katsottuna\.',
            r'Ikkunoiden ominaisuuksiin saattaa liittyä huurtumista tietyissä olosuhteissa\.',
            r'Ikkunan lämmöneristävyyden parantuessa huurtumisriski kasvaa\.',
            r'Sälekaihtimia ei ole saatavilla palo-, vino- ja muihin erikoisikkunoihin\.',
            r'Laatupalaveri 1:n jälkeen tehtävistä muutoksista veloitamme käsittelymaksun 300 e.*?aikatauluun\.',
            # Lisää yleisiä ohjeita
            r'o.*?määräytyvät.*?katsottuna\.',
            r'o.*?huurtumista.*?olosuhteissa\.',
            r'o.*?lämmöneristävyyden.*?kasvaa\.',
            r'o.*?sälekaihtimia.*?erikoisikkunoihin\.',
            r'o.*?laatupalaveri.*?aikatauluun\.',
        ]
        
        for pattern in general_patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL | re.MULTILINE)
        
        # Poista ylimääräiset tyhjät rivit
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        return text
    
    def _remove_kastelli_specific_content(self, text: str) -> str:
        """Poistaa Kastelli-kohtaisia elementtejä"""
        kastelli_patterns = [
            r"Kastelli.*?Y-tunnus: \d+-\d+",
        ]
        
        for pattern in kastelli_patterns:
            text = re.sub(pattern, "", text, flags=re.DOTALL)
        
        return text
    
    def _format_kastelli_structure(self, text: str) -> str:
        """Muotoilee Kastelli-kohtaisen rakenteen"""
        # Kastelli-kohtaiset muotoilut
        text = re.sub(r'•', '-', text)  # Listapallot viivoiksi
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Poista ylimääräiset rivit
        return text
    
    def _clean_common_issues(self, text: str) -> str:
        """Puhdistaa yleisiä ongelmia"""
        # Poista ylimääräiset välilyönnit
        text = re.sub(r'\s+', ' ', text)
        # Korjaa hajonneet numerot
        text = re.sub(r'(\d{1,3})\s(\d{3})', r'\1\2', text)
        return text.strip()
    
    def get_supplier_name(self) -> str:
        return "Kastelli"


class DesigntaloCleaner(DocumentCleaner):
    """Designtalo-kohtainen puhdistus"""
    
    def clean_document(self, pdf_path: str) -> str:
        """Puhdistaa Designtalo-dokumentin"""
        logger.info("Puhdistetaan Designtalo-dokumentti...")
        
        # Muunna PDF tekstiksi
        text = muuta_pdf_ja_puhdista_teksti_docling(pdf_path)
        
        # Designtalo-kohtaiset puhdistukset
        text = self._remove_designtalo_specific_content(text)
        text = self._format_designtalo_structure(text)
        text = self._clean_common_issues(text)
        
        return self._add_markers(text)
    
    def _remove_designtalo_specific_content(self, text: str) -> str:
        """Poistaa Designtalo-kohtaisia elementtejä"""
        designtalo_patterns = [
            r"Designtalo.*?Y-tunnus: \d+-\d+",
            # Lisää Designtalo-kohtaisia poistettavia elementtejä tarvittaessa
        ]
        
        for pattern in designtalo_patterns:
            text = re.sub(pattern, "", text, flags=re.DOTALL)
        
        return text
    
    def _format_designtalo_structure(self, text: str) -> str:
        """Muotoilee Designtalo-kohtaisen rakenteen"""
        # Designtalo-kohtaiset muotoilut
        text = re.sub(r'•', '-', text)  # Listapallot viivoiksi
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Poista ylimääräiset rivit
        return text
    
    def _clean_common_issues(self, text: str) -> str:
        """Puhdistaa yleisiä ongelmia"""
        # Poista ylimääräiset välilyönnit
        text = re.sub(r'\s+', ' ', text)
        # Korjaa hajonneet numerot
        text = re.sub(r'(\d{1,3})\s(\d{3})', r'\1\2', text)
        return text.strip()
    
    def get_supplier_name(self) -> str:
        return "Designtalo"