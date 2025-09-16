#!/usr/bin/env python3
"""
Testi run_kastelli funktiota suoraan toisella PDF-tiedostolla
"""

import sys
import os
sys.path.append(os.path.abspath("."))

from run import run_kastelli

def test_run_kastelli_2():
    """Testaa run_kastelli funktiota suoraan toisella PDF-tiedostolla"""
    
    # Käytä toista PDF-tiedostoa kuin selaimen kautta ajettu versio
    test_pdf = "data/ladatut_toimitussisallot/fcc2f5d5-991e-4e3d-a520-604369726435.pdf"
    test_id = 1133  # Testi-ID
    
    print(f"🧪 Testataan run_kastelli funktiota toisella PDF-tiedostolla...")
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
    success = test_run_kastelli_2()
    if success:
        print("\n🎉 Testi onnistui!")
    else:
        print("\n💥 Testi epäonnistui!")