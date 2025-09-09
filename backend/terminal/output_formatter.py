"""
Terminaalitulostuksen muotoilu
"""

from tabulate import tabulate
from datetime import datetime

def format_analysis_results(results):
    """
    Muotoile analyysitulokset terminaaliin
    
    Args:
        results: Analyysitulokset sanakirjana
    """
    
    # Analyysi 1
    print(f"\n📊 {results['analyysi_1']['toimittaja'].upper()}")
    print("-" * 50)
    
    # Ikkunat
    if results['analyysi_1']['ikkunat']:
        print("🪟 IKKUNAT:")
        ikkunat_data = []
        for ikkuna in results['analyysi_1']['ikkunat']:
            ikkunat_data.append([
                f"{ikkuna.leveys}x{ikkuna.korkeus}",
                "✅" if ikkuna.turvalasi else "❌",
                "✅" if ikkuna.valikarmi else "❌",
                "✅" if ikkuna.salekaihtimet else "❌"
            ])
        
        print(tabulate(
            ikkunat_data,
            headers=["Koko", "Turvalasi", "Välikarmi", "Sälekaihtimet"],
            tablefmt="grid"
        ))
    else:
        print("🪟 Ikkunoita ei löytynyt")
    
    # Ulko-ovet
    if results['analyysi_1']['ulko_ovet']:
        print("\n🚪 ULKO-OVET:")
        ovet_data = []
        for ovi in results['analyysi_1']['ulko_ovet']:
            ovet_data.append([
                ovi.ovimalli or "N/A",
                f"{ovi.leveys}x{ovi.korkeus}" if ovi.leveys and ovi.korkeus else "N/A",
                ovi.materiaali or "N/A"
            ])
        
        print(tabulate(
            ovet_data,
            headers=["Malli", "Koko", "Materiaali"],
            tablefmt="grid"
        ))
    else:
        print("\n🚪 Ulko-ovia ei löytynyt")
    
    # Väliovet
    if results['analyysi_1']['valiovet']:
        print("\n🚪 VÄLIOVET:")
        valiovet_data = []
        for valiovi in results['analyysi_1']['valiovet']:
            valiovet_data.append([valiovi.ovimalli or "N/A"])
        
        print(tabulate(
            valiovet_data,
            headers=["Ovimalli"],
            tablefmt="grid"
        ))
    else:
        print("\n🚪 Väliovia ei löytynyt")
    
    # Analyysi 2
    print(f"\n📊 {results['analyysi_2']['toimittaja'].upper()}")
    print("-" * 50)
    
    # Ikkunat
    if results['analyysi_2']['ikkunat']:
        print("🪟 IKKUNAT:")
        ikkunat_data = []
        for ikkuna in results['analyysi_2']['ikkunat']:
            ikkunat_data.append([
                f"{ikkuna.leveys}x{ikkuna.korkeus}",
                "✅" if ikkuna.turvalasi else "❌",
                "✅" if ikkuna.valikarmi else "❌",
                "✅" if ikkuna.salekaihtimet else "❌"
            ])
        
        print(tabulate(
            ikkunat_data,
            headers=["Koko", "Turvalasi", "Välikarmi", "Sälekaihtimet"],
            tablefmt="grid"
        ))
    else:
        print("🪟 Ikkunoita ei löytynyt")
    
    # Ulko-ovet
    if results['analyysi_2']['ulko_ovet']:
        print("\n🚪 ULKO-OVET:")
        ovet_data = []
        for ovi in results['analyysi_2']['ulko_ovet']:
            ovet_data.append([
                ovi.ovimalli or "N/A",
                f"{ovi.leveys}x{ovi.korkeus}" if ovi.leveys and ovi.korkeus else "N/A",
                ovi.materiaali or "N/A"
            ])
        
        print(tabulate(
            ovet_data,
            headers=["Malli", "Koko", "Materiaali"],
            tablefmt="grid"
        ))
    else:
        print("\n🚪 Ulko-ovia ei löytynyt")
    
    # Väliovet
    if results['analyysi_2']['valiovet']:
        print("\n🚪 VÄLIOVET:")
        valiovet_data = []
        for valiovi in results['analyysi_2']['valiovet']:
            valiovet_data.append([valiovi.ovimalli or "N/A"])
        
        print(tabulate(
            valiovet_data,
            headers=["Ovimalli"],
            tablefmt="grid"
        ))
    else:
        print("\n🚪 Väliovia ei löytynyt")

def format_comparison(comparison):
    """
    Muotoile vertailu terminaaliin
    
    Args:
        comparison: Vertailutulokset sanakirjana
    """
    
    print(f"\n🔄 VERTAILU: Analyysi {comparison['analyysi_1']['id']} vs {comparison['analyysi_2']['id']}")
    print("=" * 80)
    
    # Ikkunat vertailu
    print("\n🪟 IKKUNAT:")
    print("-" * 40)
    
    ikkunat_1 = comparison['analyysi_1']['ikkunat']
    ikkunat_2 = comparison['analyysi_2']['ikkunat']
    
    print(f"Analyysi {comparison['analyysi_1']['id']}: {len(ikkunat_1) if ikkunat_1 else 0} ikkunaa")
    print(f"Analyysi {comparison['analyysi_2']['id']}: {len(ikkunat_2) if ikkunat_2 else 0} ikkunaa")
    
    if ikkunat_1 and ikkunat_2:
        # Yhteiset koot
        koot_1 = set(f"{i.leveys}x{i.korkeus}" for i in ikkunat_1)
        koot_2 = set(f"{i.leveys}x{i.korkeus}" for i in ikkunat_2)
        
        yhteiset = koot_1.intersection(koot_2)
        vain_1 = koot_1 - koot_2
        vain_2 = koot_2 - koot_1
        
        if yhteiset:
            print(f"✅ Yhteiset koot: {', '.join(sorted(yhteiset))}")
        if vain_1:
            print(f"🔵 Vain analyysi {comparison['analyysi_1']['id']}: {', '.join(sorted(vain_1))}")
        if vain_2:
            print(f"🔴 Vain analyysi {comparison['analyysi_2']['id']}: {', '.join(sorted(vain_2))}")
    
    # Ulko-ovet vertailu
    print("\n🚪 ULKO-OVET:")
    print("-" * 40)
    
    ovet_1 = comparison['analyysi_1']['ulko_ovet']
    ovet_2 = comparison['analyysi_2']['ulko_ovet']
    
    print(f"Analyysi {comparison['analyysi_1']['id']}: {len(ovet_1) if ovet_1 else 0} ulko-ovea")
    print(f"Analyysi {comparison['analyysi_2']['id']}: {len(ovet_2) if ovet_2 else 0} ulko-ovea")
    
    # Väliovet vertailu
    print("\n🚪 VÄLIOVET:")
    print("-" * 40)
    
    valiovet_1 = comparison['analyysi_1']['valiovet']
    valiovet_2 = comparison['analyysi_2']['valiovet']
    
    print(f"Analyysi {comparison['analyysi_1']['id']}: {len(valiovet_1) if valiovet_1 else 0} väliovia")
    print(f"Analyysi {comparison['analyysi_2']['id']}: {len(valiovet_2) if valiovet_2 else 0} väliovia")

def format_single_analysis(analysis):
    """
    Muotoile yksittäinen analyysi terminaaliin
    
    Args:
        analysis: Analyysi sanakirjana
    """
    
    print(f"\n📊 ANALYYSI {analysis['id']}")
    print("-" * 50)
    
    # Ikkunat
    if analysis['ikkunat']:
        print("🪟 IKKUNAT:")
        ikkunat_data = []
        for ikkuna in analysis['ikkunat']:
            ikkunat_data.append([
                f"{ikkuna.leveys}x{ikkuna.korkeus}",
                "✅" if ikkuna.turvalasi else "❌",
                "✅" if ikkuna.valikarmi else "❌",
                "✅" if ikkuna.salekaihtimet else "❌"
            ])
        
        print(tabulate(
            ikkunat_data,
            headers=["Koko", "Turvalasi", "Välikarmi", "Sälekaihtimet"],
            tablefmt="grid"
        ))
    else:
        print("🪟 Ikkunoita ei löytynyt")
    
    # Ulko-ovet
    if analysis['ulko_ovet']:
        print("\n🚪 ULKO-OVET:")
        ovet_data = []
        for ovi in analysis['ulko_ovet']:
            ovet_data.append([
                ovi.ovimalli or "N/A",
                f"{ovi.leveys}x{ovi.korkeus}" if ovi.leveys and ovi.korkeus else "N/A",
                ovi.materiaali or "N/A"
            ])
        
        print(tabulate(
            ovet_data,
            headers=["Malli", "Koko", "Materiaali"],
            tablefmt="grid"
        ))
    else:
        print("\n🚪 Ulko-ovia ei löytynyt")
    
    # Väliovet
    if analysis['valiovet']:
        print("\n🚪 VÄLIOVET:")
        valiovet_data = []
        for valiovi in analysis['valiovet']:
            valiovet_data.append([valiovi.ovimalli or "N/A"])
        
        print(tabulate(
            valiovet_data,
            headers=["Ovimalli"],
            tablefmt="grid"
        ))
    else:
        print("\n🚪 Väliovia ei löytynyt")

def print_header():
    """Tulosta otsikko"""
    print("🏠" + "="*78 + "🏠")
    print("🏠" + " " * 20 + "TALOBOT - OMAKOTITALORAKENTAJAN APURI" + " " * 20 + "🏠")
    print("🏠" + " " * 25 + "PDF-analyysi terminaalissa" + " " * 25 + "🏠")
    print("🏠" + "="*78 + "🏠")

def print_help():
    """Tulosta apu"""
    print("""
Käytettävissä olevat komennot:

  analyze <tiedosto1> <tiedosto2>  - Analysoi kaksi PDF-tiedostoa
  compare <id1> <id2>             - Vertaile kahta analyysiä
  list [--limit N]                - Listaa analyysit
  show <id>                       - Näytä tietty analyysi
  help                            - Näytä tämä apu

Esimerkkejä:
  python main.py analyze sievitalo.pdf kastelli.pdf
  python main.py compare 123 456
  python main.py list --limit 5
  python main.py show 123
""")
