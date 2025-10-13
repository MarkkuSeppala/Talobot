#!/usr/bin/env python3
"""
Talobot - Terminaalikäyttöliittymä
Omakotitalorakentajan apuri PDF-analyysiin

Käyttö:
    python main.py --analyze sievitalo.pdf kastelli.pdf
    python main.py --compare 123 456
    python main.py --list
    python main.py --show 123
"""

import argparse
import sys
import os
from pathlib import Path

# Lisää projektin juurihakemisto Python-polkuun
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("utils"))
sys.path.append(os.path.abspath("backend"))

from logger_config import configure_logging
import logging

# Loggerin alustus
configure_logging()
logger = logging.getLogger(__name__)

def main():
    """Pääfunktio terminaalikäyttöliittymälle"""
    
    # Komentoriviparametrit
    parser = argparse.ArgumentParser(
        description="Talobot - Omakotitalorakentajan apuri",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esimerkkejä:
  python main.py --analyze sievitalo.pdf kastelli.pdf
  python main.py --compare 123 456
  python main.py --list
  python main.py --show 123
        """
    )
    
    # Alikomennot
    subparsers = parser.add_subparsers(dest='command', help='Käytettävissä olevat komennot')
    
    # Analysoi komennot
    analyze_parser = subparsers.add_parser('analyze', help='Analysoi kaksi toimitussisältöä')
    analyze_parser.add_argument('files', nargs=2, help='Kaksi PDF-tiedostoa analysoitavaksi')
    analyze_parser.add_argument('--output', '-o', help='Tulostetiedosto (valinnainen)')
    
    # Vertaile komennot
    compare_parser = subparsers.add_parser('compare', help='Vertaile kahta analyysiä')
    compare_parser.add_argument('id1', type=int, help='Ensimmäinen analyysi-ID')
    compare_parser.add_argument('id2', type=int, help='Toinen analyysi-ID')
    
    # Listaa komennot
    list_parser = subparsers.add_parser('list', help='Näytä kaikki analyysit')
    list_parser.add_argument('--limit', '-l', type=int, default=10, help='Maksimimäärä analyysejä')
    
    # Näytä komennot
    show_parser = subparsers.add_parser('show', help='Näytä tietty analyysi')
    show_parser.add_argument('id', type=int, help='Analyysi-ID')
    
    # Parsaa argumentit
    args = parser.parse_args()
    
    # Jos ei komentoa, näytä apu
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Suorita komento
        if args.command == 'analyze':
            from backend.terminal.cli import analyze_documents
            analyze_documents(args.files[0], args.files[1], args.output)
            
        elif args.command == 'compare':
            from backend.terminal.cli import compare_analyses
            compare_analyses(args.id1, args.id2)
            
        elif args.command == 'list':
            from backend.terminal.cli import list_analyses
            list_analyses(args.limit)
            
        elif args.command == 'show':
            from backend.terminal.cli import show_analysis
            show_analysis(args.id)
            
    except KeyboardInterrupt:
        print("\n❌ Toiminto keskeytetty käyttäjän toimesta")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Virhe: {e}")
        print(f"❌ Virhe: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



