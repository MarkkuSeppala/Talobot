"""
Esimerkki toimittajakohtaisesta puhdistuksesta
"""

import os
import sys

# Lisää polut
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("utils"))

from backend.core.cleaner_factory import CleanerFactory
from backend.core.document_processor import DocumentProcessor
from backend.services.sievitalo_service import SievitaloService
from backend.services.kastelli_service import KastelliService
from backend.services.designtalo_service import DesigntaloService

def example_supplier_specific_cleaning():
    """Esimerkki toimittajakohtaisesta puhdistuksesta"""
    
    print("=== Toimittajakohtainen puhdistus - Esimerkki ===\n")
    
    # 1. Käytä factorya luomaan puhdistajia
    print("1. Luodaan puhdistajia factorylla:")
    
    try:
        sievitalo_cleaner = CleanerFactory.create_cleaner("Sievitalo")
        kastelli_cleaner = CleanerFactory.create_cleaner("Kastelli")
        designtalo_cleaner = CleanerFactory.create_cleaner("Designtalo")
        
        print(f"   ✅ Sievitalo-puhdistaja: {sievitalo_cleaner.get_supplier_name()}")
        print(f"   ✅ Kastelli-puhdistaja: {kastelli_cleaner.get_supplier_name()}")
        print(f"   ✅ Designtalo-puhdistaja: {designtalo_cleaner.get_supplier_name()}")
        
    except ValueError as e:
        print(f"   ❌ Virhe: {e}")
    
    # 2. Näytä tuetut toimittajat
    print(f"\n2. Tuetut toimittajat: {CleanerFactory.get_available_suppliers()}")
    
    # 3. Tarkista toimittajan tuki
    print(f"\n3. Toimittajien tuki:")
    for supplier in ["Sievitalo", "Kastelli", "Designtalo", "Tuntematon"]:
        supported = CleanerFactory.is_supplier_supported(supplier)
        print(f"   {supplier}: {'✅' if supported else '❌'}")
    
    # 4. Esimerkki DocumentProcessor:n käytöstä
    print(f"\n4. DocumentProcessor esimerkki:")
    processor = DocumentProcessor()
    
    # Simuloi PDF-käsittelyä (ei todellista PDF:ää)
    print("   📄 DocumentProcessor käyttää nyt toimittajakohtaisia puhdistajia")
    print("   📄 process_pdf(pdf_path, supplier='Sievitalo')")
    print("   📄 process_pdf(pdf_path, supplier='Kastelli')")
    print("   📄 process_pdf(pdf_path)  # Tunnistaa automaattisesti")
    
    # 5. Esimerkki palveluiden käytöstä
    print(f"\n5. Palveluiden käyttö:")
    
    sievitalo_service = SievitaloService()
    kastelli_service = KastelliService()
    designtalo_service = DesigntaloService()
    
    print("   ✅ SievitaloService käyttää Sievitalo-puhdistajaa")
    print("   ✅ KastelliService käyttää Kastelli-puhdistajaa")
    print("   ✅ DesigntaloService käyttää Designtalo-puhdistajaa")
    
    print(f"\n=== Esimerkki valmis ===")

def example_cleaner_configuration():
    """Esimerkki puhdistuskonfiguraation käytöstä"""
    
    print("\n=== Puhdistuskonfiguraatio - Esimerkki ===\n")
    
    from backend.core.cleaner_config import get_cleaner_config, get_available_suppliers
    
    # Näytä konfiguraatiot
    for supplier in get_available_suppliers():
        print(f"📋 {supplier} konfiguraatio:")
        config = get_cleaner_config(supplier)
        
        print(f"   Poistettavat kuviot: {len(config['remove_patterns'])}")
        for pattern in config['remove_patterns'][:2]:  # Näytä vain 2 ensimmäistä
            print(f"     - {pattern}")
        if len(config['remove_patterns']) > 2:
            print(f"     - ... ja {len(config['remove_patterns']) - 2} muuta")
        
        print(f"   Muotoilusäännöt: {config['format_rules']}")
        print()

if __name__ == "__main__":
    example_supplier_specific_cleaning()
    example_cleaner_configuration()




