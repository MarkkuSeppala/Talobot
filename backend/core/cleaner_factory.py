"""
Factory luokka puhdistusluokkien luomiseen
"""
import logging
from typing import Dict, Type, List
from .document_cleaners import DocumentCleaner, SievitaloCleaner, KastelliCleaner, DesigntaloCleaner

logger = logging.getLogger(__name__)


class CleanerFactory:
    """Factory luokka puhdistusluokkien luomiseen"""
    
    _cleaners: Dict[str, Type[DocumentCleaner]] = {
        "Sievitalo": SievitaloCleaner,
        "Kastelli": KastelliCleaner,
        "Designtalo": DesigntaloCleaner
    }
    
    @classmethod
    def create_cleaner(cls, supplier_name: str) -> DocumentCleaner:
        """
        Luo puhdistusluokan toimittajan mukaan
        
        Args:
            supplier_name: Toimittajan nimi
            
        Returns:
            DocumentCleaner instanssi
            
        Raises:
            ValueError: Jos toimittaja ei ole tuettu
        """
        if supplier_name not in cls._cleaners:
            available = ", ".join(cls._cleaners.keys())
            raise ValueError(f"Tuntematon toimittaja: {supplier_name}. Tuetut toimittajat: {available}")
        
        cleaner_class = cls._cleaners[supplier_name]
        logger.info(f"Luodaan {supplier_name}-puhdistaja")
        return cleaner_class()
    
    @classmethod
    def get_available_suppliers(cls) -> List[str]:
        """
        Palauttaa listan tuetuista toimittajista
        
        Returns:
            Lista toimittajien nimistä
        """
        return list(cls._cleaners.keys())
    
    @classmethod
    def is_supplier_supported(cls, supplier_name: str) -> bool:
        """
        Tarkistaa onko toimittaja tuettu
        
        Args:
            supplier_name: Toimittajan nimi
            
        Returns:
            True jos toimittaja on tuettu, muuten False
        """
        return supplier_name in cls._cleaners
    
    @classmethod
    def register_cleaner(cls, supplier_name: str, cleaner_class: Type[DocumentCleaner]) -> None:
        """
        Rekisteröi uusi puhdistusluokka
        
        Args:
            supplier_name: Toimittajan nimi
            cleaner_class: Puhdistusluokka joka perii DocumentCleaner:n
        """
        if not issubclass(cleaner_class, DocumentCleaner):
            raise ValueError(f"Puhdistusluokan täytyy periytyä DocumentCleaner:stä")
        
        cls._cleaners[supplier_name] = cleaner_class
        logger.info(f"Rekisteröity uusi puhdistusluokka: {supplier_name}")
    
    @classmethod
    def unregister_cleaner(cls, supplier_name: str) -> None:
        """
        Poistaa puhdistusluokan rekisteristä
        
        Args:
            supplier_name: Toimittajan nimi
        """
        if supplier_name in cls._cleaners:
            del cls._cleaners[supplier_name]
            logger.info(f"Poistettu puhdistusluokka: {supplier_name}")
        else:
            logger.warning(f"Yritetty poistaa olematon puhdistusluokka: {supplier_name}")


