import json
from dataclasses import dataclass, asdict
from typing import List
import re 

# ----- Luokat -----
@dataclass
class IkkunaRaaka:
    koko: str
    kpl: int
    turvalasi: bool
    välikarmi: bool
    sälekaihtimet: bool

@dataclass
class Ikkuna:
    koko: str
    mm_koko: str
    turvalasi: bool
    välikarmi: bool
    sälekaihtimet: bool

# ----- Apufunktio -----
def koko_to_mm(koko: str) -> str:
    """Muuntaa kokomuodon kuten '6x15' → '600x1500'."""
    try:
        leveys, korkeus = koko.lower().split("x")
        return f"{int(leveys)*100}x{int(korkeus)*100}"
    except Exception as e:
        raise ValueError(f"Virhe kokomuodossa '{koko}': {e}")

# ----- Muunnosfunktio -----
def muunna_raaka_ikkunat_yksittaisiksi(raaka_lista: List[IkkunaRaaka]) -> List[Ikkuna]:
    yksittaiset = []
    for raaka in raaka_lista:
        for _ in range(raaka.kpl):
            ikkuna = Ikkuna(
                koko=raaka.koko,
                mm_koko=koko_to_mm(raaka.koko),
                turvalasi=raaka.turvalasi,
                välikarmi=raaka.välikarmi,
                sälekaihtimet=raaka.sälekaihtimet
            )
            yksittaiset.append(ikkuna)
    return yksittaiset


#---------------------------------------     MUUNNA_RAAKA_IKKUNAT_YKSIKKUIKSII_KASTELLI     ----------------------------------------
def muunna_raaka_ikkunat_yksittaisiksi_kastelli(raaka_lista: List[IkkunaRaaka]) -> List[Ikkuna]:
    yksittaiset = []
    for raaka in raaka_lista:
        for _ in range(raaka.kpl):
            ikkuna = Ikkuna(
                koko=raaka.koko,
                mm_koko=raaka.koko,
                turvalasi=raaka.turvalasi,
                välikarmi=raaka.välikarmi,
                sälekaihtimet=raaka.sälekaihtimet
            )
            yksittaiset.append(ikkuna)
    return yksittaiset

#---------------------------------------     PARSI_RIVIT_TIEDOIKSII     ----------------------------------------
def parsi_rivit_tiedoiksi(rivit: List[str]) -> List[IkkunaRaaka]:
    tulos = []
    
    # Tarkistetaan syötteen tyyppi
    if isinstance(rivit, str):
        #print("Muunnetaan string listaksi")
        rivit = rivit.split('\n')
    
    # print(f"Käsitellään {len(rivit)} riviä")
    # print("Rivien sisältö:", rivit)

    for i, rivi in enumerate(rivit):
        if isinstance(rivi, (list, dict)):
            print(f"Ohitetaan väärän tyyppinen rivi {i}: {rivi}")
            continue
            
        rivi = str(rivi).strip()
        if not rivi:
            continue

        #print(f"\nKäsitellään rivi {i+1}: '{rivi}'")

        # Yritetään löytää koko ja kpl
        match = re.search(r"Ikkuna\s+(\d+x\d+)\s+(\d+)\s+kpl", rivi)
        if not match:
            print(f"❌ Ei löytynyt koko/kpl riviltä: '{rivi}'")
            continue

        koko = match.group(1)
        kpl = int(match.group(2))
        #print(f"  ✅ Koko: {koko}, Kpl: {kpl}")

        # Turvalasi
        turvalasi = bool(re.search(r"turvalasi", rivi, re.IGNORECASE))
        #print(f"  🔍 Turvalasi: {turvalasi}")

        # Välikarmi – tarkistetaan esiintyykö sanana, vaikkei ole tiedostossa
        välikarmi = "välikarmi" in rivi.lower()
        #print(f"  🔍 Välikarmi: {välikarmi}")

        # Sälekaihtimet
        sälekaihtimet = bool(re.search(r"sälekaihdin", rivi, re.IGNORECASE))
        #print(f"  🔍 Sälekaihtimet: {sälekaihtimet}")

        ikkuna = IkkunaRaaka(
            koko=koko,
            kpl=kpl,
            turvalasi=turvalasi,
            välikarmi=välikarmi,
            sälekaihtimet=sälekaihtimet
        )
        tulos.append(ikkuna)

    #print(f"\nYhteensä {len(tulos)} ikkunaa parsittu.")
    return tulos

def kastelli_parsi_rivit_tiedoiksi(rivit: List[str]) -> List[IkkunaRaaka]:
    """
    Parsii Kastellin ikkunatiedot tekstimuodosta IkkunaRaaka-olioiksi.
    Kastellin mitat ovat valmiiksi millimetreinä.
    
    Args:
        rivit: Lista tekstirivejä ikkunatiedoista
    
    Returns:
        Lista IkkunaRaaka-olioita
    """
    tulos = []
    
    # Tarkistetaan syötteen tyyppi
    if isinstance(rivit, str):
        rivit = rivit.split('\n')
    
    current_ikkuna = {}
    for rivi in rivit:
        rivi = str(rivi).strip()
        if not rivi:
            continue
            
        # Uuden ikkunan alku
        if rivi.startswith("Nro:"):
            # Tallenna edellinen ikkuna jos se on olemassa
            if current_ikkuna:
                tulos.extend(_luo_ikkunat(current_ikkuna))
            current_ikkuna = {}
            
            # Parsi numero ja kappalemäärä
            match = re.search(r"Nro:\s*(\d+),\s*(\d+)\s*Kpl", rivi)
            if match:
                current_ikkuna["numero"] = match.group(1)
                current_ikkuna["kpl"] = int(match.group(2))
        
        # Parsi karmimitat (käytetään suoraan millimetreinä)
        elif "Karmimitat:" in rivi:
            match = re.search(r"Karmimitat:\s*(\d+)x(\d+)", rivi)
            if match:
                # Käytetään mittoja suoraan ilman kertomista
                leveys = match.group(1)
                korkeus = match.group(2)
                current_ikkuna["koko"] = f"{leveys}x{korkeus}"
        
        # Tarkista turvalasi
        elif "LASITUS:" in rivi:
            if "karkaistu" in rivi.lower():
                current_ikkuna["turvalasi"] = True
    
    # Tallenna viimeinen ikkuna
    if current_ikkuna:
        tulos.extend(_luo_ikkunat(current_ikkuna))
    
    print(f"✅ Parsittu {len(tulos)} Kastellin ikkunaa")
    return tulos

def _luo_ikkunat(ikkuna_tiedot: dict) -> List[IkkunaRaaka]:
    """
    Apufunktio, joka luo IkkunaRaaka-oliot annetuista tiedoista.
    """
    ikkunat = []
    for _ in range(ikkuna_tiedot.get("kpl", 0)):
        ikkuna = IkkunaRaaka(
            koko=ikkuna_tiedot.get("koko", ""),
            kpl=1,  # Yksittäinen ikkuna
            turvalasi=ikkuna_tiedot.get("turvalasi", False),
            välikarmi=False,  # Oletuksena ei välikarmia
            sälekaihtimet=False  # Oletuksena ei sälekaihtimia
        )
        ikkunat.append(ikkuna)
    
    return ikkunat

