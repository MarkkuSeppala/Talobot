#!/usr/bin/env python3
"""
Debug Kastelli PDF-käsittelyä
"""

import sys
import os
sys.path.append(os.path.abspath("."))

from utils.tietosissallon_kasittely import muuta_pdf_ja_puhdista_teksti_docling

def debug_kastelli_pdf():
    """Debug Kastelli PDF-käsittelyä"""
    
    # Käytä samaa PDF-tiedostoa kuin uusimmissa testeissä
    test_pdf = "data/ladatut_toimitussisallot/f572356a-f993-420f-a6cf-e22d2b408b25.pdf"
    
    print(f"🧪 Debug Kastelli PDF-käsittelyä...")
    print(f"📄 PDF-tiedosto: {test_pdf}")
    
    try:
        # Testaa muuta_pdf_ja_puhdista_teksti_docling funktiota
        result = muuta_pdf_ja_puhdista_teksti_docling(test_pdf)
        
        print(f"📝 Tulos tyyppi: {type(result)}")
        print(f"📝 Tulos pituus: {len(result) if result else 0}")
        print(f"📝 Tulos alku (100 merkkiä): {result[:100] if result else 'None'}")
        
        if result and len(result) < 200:
            print(f"📝 Koko tulos: {result}")
        
        return result
        
    except Exception as e:
        print(f"❌ Virhe PDF-käsittelyssä: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = debug_kastelli_pdf()
    if result:
        print("\n✅ PDF-käsittely onnistui!")
    else:
        print("\n💥 PDF-käsittely epäonnistui!")






