"""
Konfiguraatiotiedosto toimittajakohtaisille puhdistussäännöille
"""
import re
from typing import Dict, List, Any

# Toimittajakohtaiset puhdistuskonfiguraatiot
CLEANER_CONFIGS = {
    "Sievitalo": {
        "remove_patterns": [
            r"Sievitalo Oy.*?Y-tunnus: \d+-\d+",
            r"TOIMITUSTAPASELOSTE\s+\d+",
            r"Mestarintie 6.*?www\.sievitalo\.fi",
            r"Puh\. 06 822 1111.*?Fax 06 822 1112",
            r"67101 KOKKOLA",
            r"RAKENNE- JA.*?Y-tunnus: 2988131-5"
        ],
        "format_rules": {
            "section_headers": True,
            "bullet_points": True,
            "remove_extra_newlines": True,
            "fix_broken_numbers": True
        },
        "specific_replacements": {
            "•": "-",  # Listapallot viivoiksi
            "€": "€",  # Säilytä euro-merkki
        }
    },
    "Kastelli": {
        "remove_patterns": [
            r"Kastelli.*?Y-tunnus: \d+-\d+",
            # Lisää Kastelli-kohtaisia poistettavia elementtejä tarvittaessa
        ],
        "format_rules": {
            "section_headers": False,
            "bullet_points": True,
            "remove_extra_newlines": True,
            "fix_broken_numbers": True
        },
        "specific_replacements": {
            "•": "-",  # Listapallot viivoiksi
        }
    },
    "Designtalo": {
        "remove_patterns": [
            r"Designtalo.*?Y-tunnus: \d+-\d+",
            # Lisää Designtalo-kohtaisia poistettavia elementtejä tarvittaessa
        ],
        "format_rules": {
            "section_headers": True,
            "bullet_points": True,
            "remove_extra_newlines": True,
            "fix_broken_numbers": True
        },
        "specific_replacements": {
            "•": "-",  # Listapallot viivoiksi
        }
    }
}

# Yleiset puhdistussäännöt
COMMON_CLEANING_RULES = {
    "remove_extra_whitespace": True,
    "fix_broken_numbers": True,
    "normalize_bullet_points": True,
    "remove_empty_lines": True
}

# Yleiset regex-kuviot
COMMON_PATTERNS = {
    "extra_whitespace": r'\s+',
    "broken_numbers": r'(\d{1,3})\s(\d{3})',
    "multiple_newlines": r'\n\s*\n\s*\n',
    "bullet_points": r'•',
    "email_pattern": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone_pattern": r'(\+358|0)\s?\d{2,3}\s?\d{3,4}\s?\d{3,4}',
    "y_tunnus_pattern": r'Y-tunnus:\s?\d{7}-\d'
}

def get_cleaner_config(supplier_name: str) -> Dict[str, Any]:
    """
    Hakee toimittajakohtaisen puhdistuskonfiguraation
    
    Args:
        supplier_name: Toimittajan nimi
        
    Returns:
        Puhdistuskonfiguraatio sanakirjana
        
    Raises:
        ValueError: Jos toimittaja ei ole tuettu
    """
    if supplier_name not in CLEANER_CONFIGS:
        available = ", ".join(CLEANER_CONFIGS.keys())
        raise ValueError(f"Tuntematon toimittaja: {supplier_name}. Tuetut toimittajat: {available}")
    
    return CLEANER_CONFIGS[supplier_name]

def get_common_patterns() -> Dict[str, str]:
    """
    Hakee yleiset regex-kuviot
    
    Returns:
        Sanakirja regex-kuvioista
    """
    return COMMON_PATTERNS

def get_common_rules() -> Dict[str, bool]:
    """
    Hakee yleiset puhdistussäännöt
    
    Returns:
        Sanakirja yleisistä säännöistä
    """
    return COMMON_CLEANING_RULES

def is_supplier_configured(supplier_name: str) -> bool:
    """
    Tarkistaa onko toimittaja konfiguroitu
    
    Args:
        supplier_name: Toimittajan nimi
        
    Returns:
        True jos toimittaja on konfiguroitu, muuten False
    """
    return supplier_name in CLEANER_CONFIGS

def get_available_suppliers() -> List[str]:
    """
    Palauttaa listan konfiguroiduista toimittajista
    
    Returns:
        Lista toimittajien nimistä
    """
    return list(CLEANER_CONFIGS.keys())


