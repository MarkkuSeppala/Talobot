#!/usr/bin/env python3
"""
Testi run_kastelli funktiota suoraan
"""

import sys
import os
sys.path.append(os.path.abspath("."))

from run import run_kastelli

def test_run_kastelli():
    """Testaa run_kastelli funktiota suoraan"""
    
    # Käytä samaa PDF-tiedostoa kuin selaimen kautta ajettu versio
    test_pdf = "data/ladatut_toimitussisallot/f572356a-f993-420f-a6cf-e22d2b408b25.pdf"
    test_id = 1132  # Testi-ID
    
    print(f"🧪 Testataan run_kastelli funktiota...")
    print(f"📄 PDF-tiedosto: {test_pdf}")
    print(f"🆔 Testi-ID: {test_id}")
    
    try:
        # Testaa run_kastelli funktiota
        result = run_kastelli(test_pdf, test_id)
        print("✅ run_kastelli funktio onnistui!")
        return True
        
    except Exception as e:
        print(f"❌ Virhe run_kastelli funktiossa: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_run_kastelli()
    if success:
        print("\n🎉 Testi onnistui!")
    else:
        print("\n💥 Testi epäonnistui!")






