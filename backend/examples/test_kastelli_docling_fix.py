#!/usr/bin/env python3
"""
Testi korjatulle Kastelli-puhdistukselle
Testaa Docling-ongelmien korjaamista
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.core.document_cleaners import KastelliCleaner
import logging

# Konfiguroi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_docling_fix():
    """Testaa Docling-ongelmien korjaamista"""
    
    # Simuloi Docling-kirjaston tuottamaa tekstiä (ongelmatilanne)
    docling_problematic_text = """
Nro:
30

## Tyyppi: B4 /13.4x13.5

<!-- image -->

Karmimitat: 1330x1340
KARMITYYPPI: MSEL, avattava, karmisyvyys 170 mm
SISÄPUITTEEN LASITUS: 2-kertainen eristyslasielementti, U=1,0
ULKOPUITTEEN LASITUS: 1-kertainen tasolasi
PUUOSIEN PINTAKÄSITTELY: valkoinen
ALUMIINIOSIEN VÄRI: valkoinen
KARMI-/PUITEMATER: ulkopuite ja karmin ulkopuoli alumiinia
HELOITUKSEN VÄRI: valkoinen
SÄLEKAIHDIN: matta valkoinen P2
TUULETUSIKKUNA: tuuletusikkunaheloitus (tunnus T)
HYÖNTEISPUITE: (tunnus H) HUOM! Hyttyspuite samassa kehässä mahdollisen
irtoristikon kanssa.
HUONETILA: MH1 ja keittiö

Nro:
40

## Tyyppi: A /14.4x19

<!-- image -->

Karmimitat: 1430x1890
KARMITYYPPI: MSEL, avattava, karmisyvyys 170 mm
SISÄPUITTEEN LASITUS: 2-kertainen eristyslasielementti, U=1,0, sisin lasi karkaistu
ULKOPUITTEEN LASITUS: 1-kertainen tasolasi
PUUOSIEN PINTAKÄSITTELY: valkoinen
ALUMIINIOSIEN VÄRI: valkoinen
KARMI-/PUITEMATER: ulkopuite ja karmin ulkopuoli alumiinia
HELOITUKSEN VÄRI:
SÄLEKAIHDIN: matta valkoinen P2
HUONETILA: Oh
"""

    print("=== ENNEN KORJAUSTA (Docling-ongelmat) ===")
    print(docling_problematic_text[:500] + "...")
    print()
    
    # Luo KastelliCleaner ja testaa korjauksia
    cleaner = KastelliCleaner()
    
    # Testaa _fix_docling_issues metodia
    fixed_text = cleaner._fix_docling_issues(docling_problematic_text)
    
    print("=== KORJAUKSEN JÄLKEEN ===")
    print(fixed_text[:1000] + "...")
    print()
    
    # Tarkista että korjaukset toimivat
    print("=== TARKISTUKSET ===")
    
    # 1. Tarkista että "Nro:" ja numero on yhdessä
    if "Nro: 30" in fixed_text and "Nro: 40" in fixed_text:
        print("✅ Nro: ja numero korjattu yhdessä")
    else:
        print("❌ Nro: ja numero ei ole yhdessä")
    
    # 2. Tarkista että "## Tyyppi:" on muutettu "Tyyppi:"
    if "## Tyyppi:" not in fixed_text and "Tyyppi: B4 /13.4x13.5" in fixed_text:
        print("✅ ## Tyyppi: korjattu Tyyppi:")
    else:
        print("❌ ## Tyyppi: ei korjattu")
    
    # 3. Tarkista että kuvat on poistettu
    if "<!-- image -->" not in fixed_text:
        print("✅ Kuvat poistettu")
    else:
        print("❌ Kuvat eivät ole poistettu")
    
    # 4. Tarkista että ikkunatiedot on ryhmitelty
    window_30_section = fixed_text.split("Nro: 30")[1].split("Nro: 40")[0] if "Nro: 40" in fixed_text else fixed_text.split("Nro: 30")[1]
    if "Tyyppi: B4 /13.4x13.5" in window_30_section and "Karmimitat: 1330x1340" in window_30_section:
        print("✅ Ikkunatiedot ryhmitelty yhdessä")
    else:
        print("❌ Ikkunatiedot eivät ole ryhmitelty yhdessä")
    
    print()
    print("=== KORJATTU TEKSTI (Nro: 30 ikkuna) ===")
    if "Nro: 40" in fixed_text:
        window_30 = fixed_text.split("Nro: 30")[1].split("Nro: 40")[0]
    else:
        window_30 = fixed_text.split("Nro: 30")[1]
    print(window_30.strip())

def test_real_pdf():
    """Testaa todellisella PDF-tiedostolla"""
    pdf_path = "Kastelli Oravala & Salmi Mv13.12.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF-tiedostoa ei löytynyt: {pdf_path}")
        return
    
    print(f"=== TESTATAAN TODELLISELLA PDF:LLÄ ===")
    print(f"Tiedosto: {pdf_path}")
    
    try:
        cleaner = KastelliCleaner()
        cleaned_text = cleaner.clean_document(pdf_path)
        
        print("✅ PDF puhdistettu onnistuneesti")
        
        # Etsi ikkunatiedot
        if "Nro: 30" in cleaned_text:
            print("\n=== LÖYTYI ikkuna Nro: 30 ===")
            window_30_section = cleaned_text.split("Nro: 30")[1]
            if "Nro: 40" in window_30_section:
                window_30_section = window_30_section.split("Nro: 40")[0]
            print(window_30_section[:500] + "...")
        
        # Tallenna tulos
        output_file = "test_kastelli_cleaned_output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(f"✅ Puhdistettu teksti tallennettu: {output_file}")
        
    except Exception as e:
        print(f"❌ Virhe PDF:n käsittelyssä: {e}")

if __name__ == "__main__":
    print("Kastelli Docling-korjauksen testi")
    print("=" * 50)
    
    # Testaa simuloidulla tekstillä
    test_docling_fix()
    
    print("\n" + "=" * 50)
    
    # Testaa todellisella PDF:llä
    test_real_pdf()



