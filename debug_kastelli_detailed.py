#!/usr/bin/env python3
"""
Debug Kastelli PDF-käsittelyä yksityiskohtaisesti
"""

import sys
import os
sys.path.append(os.path.abspath("."))

def debug_kastelli_pdf_detailed():
    """Debug Kastelli PDF-käsittelyä yksityiskohtaisesti"""
    
    # Käytä samaa PDF-tiedostoa kuin uusimmissa testeissä
    test_pdf = "data/ladatut_toimitussisallot/f572356a-f993-420f-a6cf-e22d2b408b25.pdf"
    
    print(f"🧪 Debug Kastelli PDF-käsittelyä yksityiskohtaisesti...")
    print(f"📄 PDF-tiedosto: {test_pdf}")
    
    try:
        from docling.document_converter import DocumentConverter
        
        print("1. Luodaan DocumentConverter...")
        converter = DocumentConverter()
        
        print("2. Kutsutaan converter.convert()...")
        result = converter.convert(test_pdf)
        
        print("3. Kutsutaan result.document.export_to_markdown()...")
        text = result.document.export_to_markdown()
        
        print("4. Muunnetaan str()...")
        text_str = str(text)
        
        print(f"📝 Tulos tyyppi: {type(text_str)}")
        print(f"📝 Tulos pituus: {len(text_str) if text_str else 0}")
        print(f"📝 Tulos alku (200 merkkiä): {text_str[:200] if text_str else 'None'}")
        
        # Tarkista onko tulos vain tiedoston polku
        if text_str == test_pdf:
            print("❌ ONGELMA: Funktio palauttaa vain PDF-tiedoston polun!")
        elif len(text_str) < 1000:
            print("❌ ONGELMA: Tulos on liian lyhyt!")
        else:
            print("✅ Tulos näyttää oikealta!")
        
        return text_str
        
    except Exception as e:
        print(f"❌ Virhe PDF-käsittelyssä: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = debug_kastelli_pdf_detailed()
    if result and len(result) > 1000:
        print("\n✅ PDF-käsittely onnistui!")
    else:
        print("\n💥 PDF-käsittely epäonnistui!")






