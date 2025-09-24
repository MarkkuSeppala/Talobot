#!/usr/bin/env python3
"""
Testi perus Kastelli-puhdistukselle ilman ikkunoita koskevia toimintoja
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.core.document_cleaners import KastelliCleaner
import logging

# Konfiguroi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_basic_kastelli_cleaning():
    """Testaa perus Kastelli-puhdistusta"""
    
    pdf_path = "Kastelli Oravala & Salmi Mv13.12.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF-tiedostoa ei löytynyt: {pdf_path}")
        return
    
    print("🚀 Testataan perus Kastelli-puhdistus...")
    
    try:
        cleaner = KastelliCleaner()
        cleaned_text = cleaner.clean_document(pdf_path)
        
        print("✅ PDF puhdistettu onnistuneesti")
        
        # Tallenna tulos
        output_file = "test_kastelli_basic_cleaned.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(f"✅ Puhdistettu teksti tallennettu: {output_file}")
        
        # Analysoi ikkunatiedot
        print("\n📊 Analyysi ikkunatiedoista:")
        
        # Etsi Nro: -rivit
        import re
        nro_matches = re.findall(r'Nro:\s*(\d+)', cleaned_text)
        print(f"Löytyi {len(nro_matches)} Nro: -riviä")
        
        # Etsi Tyyppi: -rivit
        tyyppi_matches = re.findall(r'Tyyppi:\s*([^\\n]*)', cleaned_text)
        print(f"Löytyi {len(tyyppi_matches)} Tyyppi: -riviä")
        
        # Näytä ensimmäiset ikkunatiedot
        print("\n🔍 Ensimmäiset ikkunatiedot:")
        lines = cleaned_text.split('\\n')
        for i, line in enumerate(lines):
            if 'Nro:' in line or 'Tyyppi:' in line:
                print(f"  {i+1:3d}: {line}")
                if i > 20:  # Rajoita tulostus
                    print("  ...")
                    break
        
    except Exception as e:
        print(f"❌ Virhe PDF:n käsittelyssä: {e}")

if __name__ == "__main__":
    test_basic_kastelli_cleaning()

