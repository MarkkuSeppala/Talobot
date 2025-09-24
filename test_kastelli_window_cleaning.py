#!/usr/bin/env python3
"""
Testi korjatulle Kastelli-puhdistukselle ikkunatietojen erottamiseksi
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.core.document_cleaners import KastelliCleaner
import logging

# Konfiguroi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_window_cleaning():
    """Testaa ikkunatietojen erottamista ja puhdistusta"""
    
    pdf_path = "Kastelli Oravala & Salmi Mv13.12.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF-tiedostoa ei löytynyt: {pdf_path}")
        return
    
    print("🚀 Testataan korjattu Kastelli-puhdistus ikkunatiedoille...")
    
    try:
        cleaner = KastelliCleaner()
        cleaned_text = cleaner.clean_document(pdf_path)
        
        print("✅ PDF puhdistettu onnistuneesti")
        
        # Tallenna tulos
        output_file = "test_kastelli_window_cleaned.txt"
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
        
        # Tarkista että yleiset ohjeet on poistettu
        general_instructions = [
            "Toimittamamme ikkunat ovat viranomaismääräysten mukaiset",
            "Kätisyydet määräytyvät sisäpuolelta katsottuna",
            "Laatupalaveri 1:n jälkeen tehtävistä muutoksista"
        ]
        
        print("\n🔍 Tarkistetaan yleisten ohjeiden poistaminen:")
        for instruction in general_instructions:
            if instruction in cleaned_text:
                print(f"❌ Yleisohje löytyy vielä: {instruction[:50]}...")
            else:
                print(f"✅ Yleisohje poistettu: {instruction[:50]}...")
        
        # Näytä ensimmäiset ikkunatiedot
        print("\n🔍 Ensimmäiset ikkunatiedot:")
        lines = cleaned_text.split('\\n')
        window_lines = []
        for i, line in enumerate(lines):
            if 'Nro:' in line or 'Tyyppi:' in line:
                window_lines.append(f"{i+1:3d}: {line}")
                if len(window_lines) > 20:  # Rajoita tulostus
                    window_lines.append("  ...")
                    break
        
        for line in window_lines:
            print(line)
        
    except Exception as e:
        print(f"❌ Virhe PDF:n käsittelyssä: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_window_cleaning()

