"""
Testi Kastelli-ikkunatietojen säilyttämiselle
"""

import os
import sys

# Lisää polut
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("utils"))

from backend.core.document_cleaners import KastelliCleaner

def test_kastelli_window_preservation():
    """Testaa että Kastelli-puhdistus säilyttää ikkunatiedot yhdessä"""
    
    print("=== Kastelli-ikkunatietojen säilyttämistesti ===\n")
    
    # Simuloi alkuperäistä tekstiä (kuten PDF:stä tuleva)
    original_text = """
Nro: 30
Tyyppi: B4/13.4x13.5
[kuvio]
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
HYÖNTEISPUITE: (tunnus H) HUOM! Hyttyspuite samassa kehässä mahdollisen irtoristikon kanssa.
HUONETILA: MH1 ja keittiö

Nro: 40
Tyyppi: A/14.4x19
[kuvio]
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
    
    print("1. Alkuperäinen teksti:")
    print(original_text[:200] + "...")
    
    # Luo Kastelli-puhdistaja
    cleaner = KastelliCleaner()
    
    # Testaa ikkunatietojen säilyttämistä
    print("\n2. Testataan ikkunatietojen säilyttämistä...")
    
    # Simuloi PDF-käsittelyä (käytä tekstiä suoraan)
    cleaned_text = cleaner._preserve_kastelli_window_data(original_text)
    
    print("\n3. Puhdistettu teksti:")
    print(cleaned_text[:300] + "...")
    
    # Tarkista että ikkunatiedot säilyvät yhdessä
    print("\n4. Tarkistetaan ikkunatietojen säilyttäminen:")
    
    # Etsi ikkunatiedot
    window_blocks = re.findall(r'Nro:\s*(\d+).*?(?=Nro:\s*\d+|$)', cleaned_text, re.DOTALL)
    
    print(f"   Löydetty {len(window_blocks)} ikkunatietoryhmää")
    
    for i, block in enumerate(window_blocks[:2]):  # Näytä 2 ensimmäistä
        print(f"\n   Ikkuna {i+1}:")
        print(f"   {block[:100]}...")
        
        # Tarkista että Nro ja Tyyppi ovat lähellä toisiaan
        if 'Nro:' in block and 'Tyyppi:' in block:
            print("   ✅ Nro ja Tyyppi löytyvät samasta ryhmästä")
        else:
            print("   ❌ Nro ja Tyyppi eivät ole samassa ryhmässä")
    
    print("\n5. Testi valmis!")

def test_window_data_grouping():
    """Testaa ikkunatietojen ryhmittelyä"""
    
    print("\n=== Ikkunatietojen ryhmittelytesti ===\n")
    
    # Testaa regex-ryhmittelyä
    test_text = """
Nro: 30
Tyyppi: B4/13.4x13.5
Karmimitat: 1330x1340
KARMITYYPPI: MSEL

Nro: 40  
Tyyppi: A/14.4x19
Karmimitat: 1430x1890
KARMITYYPPI: MSEL
"""
    
    # Ryhmittele ikkunatiedot
    def group_window_data(match):
        window_number = match.group(1)
        window_content = match.group(2)
        return f"Nro: {window_number}\n{window_content.strip()}"
    
    grouped_text = re.sub(
        r'Nro:\s*(\d+)(.*?)(?=Nro:\s*\d+|$)',
        group_window_data,
        test_text,
        flags=re.DOTALL
    )
    
    print("Ryhmitelty teksti:")
    print(grouped_text)
    
    # Tarkista ryhmittely
    lines = grouped_text.split('\n')
    current_window = None
    
    for line in lines:
        if line.startswith('Nro:'):
            current_window = line
            print(f"\n✅ Uusi ikkuna: {current_window}")
        elif line.startswith('Tyyppi:'):
            if current_window:
                print(f"   ✅ Tyyppi löytyy samasta ikkunasta: {line}")
            else:
                print(f"   ❌ Tyyppi ilman ikkunan numeroa: {line}")

if __name__ == "__main__":
    import re
    test_kastelli_window_preservation()
    test_window_data_grouping()




