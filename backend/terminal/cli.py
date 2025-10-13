"""
Terminaalikäyttöliittymä CLI-funktiot
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Lisää polut
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("utils"))

from logger_config import configure_logging
import logging

# Loggerin alustus
configure_logging()
logger = logging.getLogger(__name__)

def analyze_documents(file1_path: str, file2_path: str, output_file: str = None):
    """
    Analysoi kaksi PDF-tiedostoa
    
    Args:
        file1_path: Ensimmäinen PDF-tiedosto
        file2_path: Toinen PDF-tiedosto
        output_file: Tulostetiedosto (valinnainen)
    """
    print("🔍 Talobot - PDF-analyysi aloitetaan...")
    print(f"📄 Tiedosto 1: {file1_path}")
    print(f"📄 Tiedosto 2: {file2_path}")
    print()
    
    try:
        # Tarkista tiedostot
        if not Path(file1_path).exists():
            raise FileNotFoundError(f"Tiedostoa ei löytynyt: {file1_path}")
        if not Path(file2_path).exists():
            raise FileNotFoundError(f"Tiedostoa ei löytynyt: {file2_path}")
        
        # Tuo tarvittavat moduulit
        from SQL_kyselyt import vastaanota_toimitussisalto, hae_toimittaja_uuidlla, hae_toimitussisalto_id_uuidlla
        from SQL_kyselyt import hae_pdf_url_uuidlla, hae_uuid_toimitussisalto_idlla, lisaa_vertailu
        from SQL_kyselyt import hae_toimitussisallon_ikkunat, hae_toimitussisallon_ulko_ovet, hae_toimitussisallon_valiovet
        from run import run_sievitalo, run_kastelli
        from backend.terminal.output_formatter import format_analysis_results
        
        # Käsittele ensimmäinen tiedosto
        print("📥 Käsitellään ensimmäinen tiedosto...")
        with open(file1_path, 'rb') as f:
            unique_id_1 = vastaanota_toimitussisalto(f)
        
        # Käsittele toinen tiedosto
        print("📥 Käsitellään toinen tiedosto...")
        with open(file2_path, 'rb') as f:
            unique_id_2 = vastaanota_toimitussisalto(f)
        
        # Luo vertailu
        print("🔗 Luodaan vertailu...")
        lisaa_vertailu(
            hae_toimitussisalto_id_uuidlla(unique_id_1), 
            hae_toimitussisalto_id_uuidlla(unique_id_2)
        )
        
        # Analysoi ensimmäinen tiedosto
        print("🔍 Analysoidaan ensimmäinen tiedosto...")
        toimittaja_1 = hae_toimittaja_uuidlla(unique_id_1)
        print(f"   Toimittaja: {toimittaja_1}")
        
        toimitussisalto_id_1 = hae_toimitussisalto_id_uuidlla(unique_id_1)
        pdf_url_1 = hae_pdf_url_uuidlla(uuid=hae_uuid_toimitussisalto_idlla(toimitussisalto_id_1))
        
        if toimittaja_1 == "Sievitalo":
            print("   Suoritetaan Sievitalo-analyysi...")
            run_sievitalo(pdf_url_1, toimitussisalto_id_1)
        elif toimittaja_1 == "Kastelli":
            print("   Suoritetaan Kastelli-analyysi...")
            run_kastelli(pdf_url_1, toimitussisalto_id_1)
        else:
            print(f"   ⚠️ Tuntematon toimittaja: {toimittaja_1}")
        
        # Analysoi toinen tiedosto
        print("🔍 Analysoidaan toinen tiedosto...")
        toimittaja_2 = hae_toimittaja_uuidlla(unique_id_2)
        print(f"   Toimittaja: {toimittaja_2}")
        
        toimitussisalto_id_2 = hae_toimitussisalto_id_uuidlla(unique_id_2)
        pdf_url_2 = hae_pdf_url_uuidlla(uuid=hae_uuid_toimitussisalto_idlla(toimitussisalto_id_2))
        
        if toimittaja_2 == "Sievitalo":
            print("   Suoritetaan Sievitalo-analyysi...")
            run_sievitalo(pdf_url_2, toimitussisalto_id_2)
        elif toimittaja_2 == "Kastelli":
            print("   Suoritetaan Kastelli-analyysi...")
            run_kastelli(pdf_url_2, toimitussisalto_id_2)
        else:
            print(f"   ⚠️ Tuntematon toimittaja: {toimittaja_2}")
        
        # Hae tulokset
        print("📊 Haetaan analyysitulokset...")
        ikkunat_1 = hae_toimitussisallon_ikkunat(toimitussisalto_id_1)
        ulko_ovet_1 = hae_toimitussisallon_ulko_ovet(toimitussisalto_id_1)
        valiovet_1 = hae_toimitussisallon_valiovet(toimitussisalto_id_1)
        
        ikkunat_2 = hae_toimitussisallon_ikkunat(toimitussisalto_id_2)
        ulko_ovet_2 = hae_toimitussisallon_ulko_ovet(toimitussisalto_id_2)
        valiovet_2 = hae_toimitussisallon_valiovet(toimitussisalto_id_2)
        
        # Muodosta tulokset
        tulokset = {
            "analyysi_1": {
                "toimittaja": toimittaja_1,
                "id": toimitussisalto_id_1,
                "ikkunat": ikkunat_1,
                "ulko_ovet": ulko_ovet_1,
                "valiovet": valiovet_1
            },
            "analyysi_2": {
                "toimittaja": toimittaja_2,
                "id": toimitussisalto_id_2,
                "ikkunat": ikkunat_2,
                "ulko_ovet": ulko_ovet_2,
                "valiovet": valiovet_2
            }
        }
        
        # Tulosta tulokset
        print("\n" + "="*80)
        print("📊 ANALYYSITULOKSET")
        print("="*80)
        
        format_analysis_results(tulokset)
        
        # Tallenna tulokset tiedostoon jos pyydetty
        if output_file:
            print(f"\n💾 Tallennetaan tulokset tiedostoon: {output_file}")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(tulokset, f, ensure_ascii=False, indent=2, default=str)
            print("✅ Tulokset tallennettu!")
        
        print(f"\n✅ Analyysi valmis! Analyysi-ID:t: {toimitussisalto_id_1}, {toimitussisalto_id_2}")
        
    except Exception as e:
        logger.error(f"Virhe analyysissa: {e}")
        print(f"❌ Virhe analyysissa: {e}")
        raise

def compare_analyses(id1: int, id2: int):
    """
    Vertaile kahta analyysiä
    
    Args:
        id1: Ensimmäinen analyysi-ID
        id2: Toinen analyysi-ID
    """
    print(f"🔄 Vertaillaan analyysejä {id1} ja {id2}...")
    
    try:
        from SQL_kyselyt import hae_toimitussisallon_ikkunat, hae_toimitussisallon_ulko_ovet, hae_toimitussisallon_valiovet
        from backend.terminal.output_formatter import format_comparison
        
        # Hae analyysit
        ikkunat_1 = hae_toimitussisallon_ikkunat(id1)
        ulko_ovet_1 = hae_toimitussisallon_ulko_ovet(id1)
        valiovet_1 = hae_toimitussisallon_valiovet(id1)
        
        ikkunat_2 = hae_toimitussisallon_ikkunat(id2)
        ulko_ovet_2 = hae_toimitussisallon_ulko_ovet(id2)
        valiovet_2 = hae_toimitussisallon_valiovet(id2)
        
        # Muodosta vertailu
        vertailu = {
            "analyysi_1": {
                "id": id1,
                "ikkunat": ikkunat_1,
                "ulko_ovet": ulko_ovet_1,
                "valiovet": valiovet_1
            },
            "analyysi_2": {
                "id": id2,
                "ikkunat": ikkunat_2,
                "ulko_ovet": ulko_ovet_2,
                "valiovet": valiovet_2
            }
        }
        
        # Tulosta vertailu
        print("\n" + "="*80)
        print("🔄 VERTAILU")
        print("="*80)
        
        format_comparison(vertailu)
        
    except Exception as e:
        logger.error(f"Virhe vertailussa: {e}")
        print(f"❌ Virhe vertailussa: {e}")
        raise

def list_analyses(limit: int = 10):
    """
    Listaa kaikki analyysit
    
    Args:
        limit: Maksimimäärä analyysejä
    """
    print(f"📋 Listataan {limit} viimeisintä analyysiä...")
    
    try:
        from SQL_kyselyt import hae_paivan_toimitussisallot
        from datetime import datetime
        
        # Hae tämän päivän analyysit
        pvm = datetime.now().strftime('%d.%m.%Y')
        analyysit = hae_paivan_toimitussisallot(pvm)
        
        if not analyysit:
            print("❌ Analyysejä ei löytynyt")
            return
        
        print(f"\n📊 Löytyi {len(analyysit)} analyysiä:")
        print("-" * 60)
        
        for i, analyysi in enumerate(analyysit[:limit], 1):
            print(f"{i:2d}. ID: {analyysi.id:3d} | Toimittaja: {analyysi.toimittaja:12s} | PVM: {analyysi.created_at.strftime('%d.%m.%Y %H:%M')}")
        
        if len(analyysit) > limit:
            print(f"... ja {len(analyysit) - limit} muuta")
            
    except Exception as e:
        logger.error(f"Virhe listauksessa: {e}")
        print(f"❌ Virhe listauksessa: {e}")
        raise

def show_analysis(analysis_id: int):
    """
    Näytä tietty analyysi
    
    Args:
        analysis_id: Analyysi-ID
    """
    print(f"👁️ Näytetään analyysi {analysis_id}...")
    
    try:
        from SQL_kyselyt import hae_toimitussisallon_ikkunat, hae_toimitussisallon_ulko_ovet, hae_toimitussisallon_valiovet
        from backend.terminal.output_formatter import format_single_analysis
        
        # Hae analyysi
        ikkunat = hae_toimitussisallon_ikkunat(analysis_id)
        ulko_ovet = hae_toimitussisallon_ulko_ovet(analysis_id)
        valiovet = hae_toimitussisallon_valiovet(analysis_id)
        
        if not ikkunat and not ulko_ovet and not valiovet:
            print(f"❌ Analyysiä {analysis_id} ei löytynyt")
            return
        
        # Muodosta analyysi
        analyysi = {
            "id": analysis_id,
            "ikkunat": ikkunat,
            "ulko_ovet": ulko_ovet,
            "valiovet": valiovet
        }
        
        # Tulosta analyysi
        print("\n" + "="*80)
        print(f"📊 ANALYYSI {analysis_id}")
        print("="*80)
        
        format_single_analysis(analyysi)
        
    except Exception as e:
        logger.error(f"Virhe analyysin näyttämisessä: {e}")
        print(f"❌ Virhe analyysin näyttämisessä: {e}")
        raise



