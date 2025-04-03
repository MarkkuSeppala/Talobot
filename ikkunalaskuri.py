import math
from logger_config import configure_logging
import logging

def laske_ikkunan_hinta(leveys, korkeus):
    """
    Laskee ikkunan hinnan annettujen mittojen perusteella käyttäen
    lähimpään pinta-alaan perustuvaa neliöhintaa datasta.

    Args:
        leveys (int): Ikkunan leveys (datan yksiköissä, oletettavasti cm tai dm).
        korkeus (int): Ikkunan korkeus (datan yksiköissä, oletettavasti cm tai dm).

    Returns:
        float: Arvioitu ikkunan hinta euroina.
               Palauttaa None, jos syötteet ovat epäkelvot tai dataa ei ole.
    """

    # Hintadata kuvasta (leveys, korkeus, hinta)
    # Huom: OCR-tunnistus voi sisältää virheitä, data on tarkistettu silmämääräisesti.
    # Joitakin rivejä on jätetty pois, jos leveys tai korkeus puuttui OCR-tuloksesta.
    data = [
        {'leveys': 18, 'korkeus': 21, 'hinta': 877},
        {'leveys': 18, 'korkeus': 20, 'hinta': 858},
        {'leveys': 18, 'korkeus': 19, 'hinta': 839},
        {'leveys': 14, 'korkeus': 23, 'hinta': 823},
        {'leveys': 14, 'korkeus': 22, 'hinta': 807},
        {'leveys': 14, 'korkeus': 21, 'hinta': 791},
        {'leveys': 14, 'korkeus': 20, 'hinta': 768},
        {'leveys': 14, 'korkeus': 19, 'hinta': 749},
        {'leveys': 14, 'korkeus': 18, 'hinta': 726},
        {'leveys': 14, 'korkeus': 17, 'hinta': 706},
        {'leveys': 11, 'korkeus': 22, 'hinta': 719},
        {'leveys': 14, 'korkeus': 16, 'hinta': 686}, # Kaksi identtistä riviä datassa
        {'leveys': 15, 'korkeus': 14, 'hinta': 663},
        {'leveys': 14, 'korkeus': 15, 'hinta': 663},
        {'leveys': 9, 'korkeus': 23, 'hinta': 676},
        {'leveys': 9, 'korkeus': 22, 'hinta': 661},
        {'leveys': 9, 'korkeus': 21, 'hinta': 645},
        {'leveys': 9, 'korkeus': 20, 'hinta': 629},
        {'leveys': 9, 'korkeus': 19, 'hinta': 614},
        {'leveys': 9, 'korkeus': 18, 'hinta': 598},
        {'leveys': 7, 'korkeus': 23, 'hinta': 613},
        {'leveys': 7, 'korkeus': 22, 'hinta': 602},
        {'leveys': 7, 'korkeus': 21, 'hinta': 590},
        {'leveys': 7, 'korkeus': 20, 'hinta': 578}, # Oletetaan leveys 7 riviltä yläpuolelta
        {'leveys': 7, 'korkeus': 15, 'hinta': 558}, # Oletetaan leveys 7 (hyppäys korkeudessa)
        {'leveys': 7, 'korkeus': 19, 'hinta': 567}, # Oletetaan leveys 7 riviltä yläpuolelta
        {'leveys': 7, 'korkeus': 18, 'hinta': 555}, # Oletetaan leveys 7 riviltä yläpuolelta
        {'leveys': 7, 'korkeus': 17, 'hinta': 542},
        {'leveys': 14, 'korkeus': 8, 'hinta': 525},
        {'leveys': 7, 'korkeus': 16, 'hinta': 530},
        {'leveys': 7, 'korkeus': 15, 'hinta': 520},
        {'leveys': 7, 'korkeus': 14, 'hinta': 509},
        {'leveys': 7, 'korkeus': 13, 'hinta': 497},
        {'leveys': 15, 'korkeus': 6, 'hinta': 501},
        {'leveys': 7, 'korkeus': 12, 'hinta': 486},
        {'leveys': 4, 'korkeus': 23, 'hinta': 533},
        {'leveys': 14, 'korkeus': 6, 'hinta': 491},
        {'leveys': 13, 'korkeus': 6, 'hinta': 480},
        {'leveys': 7, 'korkeus': 11, 'hinta': 474},
        {'leveys': 7, 'korkeus': 10, 'hinta': 462},
        {'leveys': 3, 'korkeus': 23, 'hinta': 507},
        {'leveys': 3, 'korkeus': 22, 'hinta': 499},
        {'leveys': 3, 'korkeus': 21, 'hinta': 492},
        {'leveys': 3, 'korkeus': 20, 'hinta': 483},
        {'leveys': 3, 'korkeus': 19, 'hinta': 478}, # Oletetaan leveys 3 riviltä yläpuolelta
        {'leveys': 3, 'korkeus': 18, 'hinta': 468}, # Oletetaan leveys 3 riviltä yläpuolelta
        {'leveys': 3, 'korkeus': 17, 'hinta': 460}, # Oletetaan leveys 3 riviltä yläpuolelta
        {'leveys': 3, 'korkeus': 16, 'hinta': 453}, # Oletetaan leveys 3 riviltä yläpuolelta
        {'leveys': 3, 'korkeus': 15, 'hinta': 446}, # Oletetaan leveys 3 riviltä yläpuolelta
        {'leveys': 3, 'korkeus': 14, 'hinta': 438}, # Oletetaan leveys 3 riviltä yläpuolelta
        {'leveys': 3, 'korkeus': 13, 'hinta': 431},
        {'leveys': 3, 'korkeus': 12, 'hinta': 423},
        {'leveys': 3, 'korkeus': 11, 'hinta': 416},
        {'leveys': 6, 'korkeus': 5, 'hinta': 398},
        {'leveys': 3, 'korkeus': 10, 'hinta': 408},
        {'leveys': 3, 'korkeus': 9, 'hinta': 401},
        {'leveys': 3, 'korkeus': 8, 'hinta': 394},
        {'leveys': 3, 'korkeus': 7, 'hinta': 386},
        {'leveys': 3, 'korkeus': 6, 'hinta': 379}, # Oletetaan leveys 3 riviltä yläpuolelta
        {'leveys': 3, 'korkeus': 5, 'hinta': 371}, # Oletetaan leveys 3 riviltä yläpuolelta
    ]

    if not isinstance(leveys, (int, float)) or not isinstance(korkeus, (int, float)) or leveys <= 0 or korkeus <= 0:
        logging.warning("Virhe: Leveyden ja korkeuden tulee olla positiivisia numeroita.")
        return None

    if not data:
        logging.warning("Virhe: Hintadataa ei löytynyt.")
        return None

    target_area = leveys * korkeus

    # 1. Tarkista, löytyykö täsmälleen sama koko datasta
    for item in data:
        if item['leveys'] == leveys and item['korkeus'] == korkeus:
            logging.info(f"Löytyi tarkka vastine: {item['hinta']} €")
            return float(item['hinta'])

    # 2. Jos tarkkaa vastinetta ei löydy, etsi lähin pinta-ala
    min_area_diff = float('inf')
    best_match = None

    for item in data:
        item_area = item['leveys'] * item['korkeus']
        if item_area <= 0: # Varmistetaan ettei jaeta nollalla
            continue

        area_diff = abs(item_area - target_area)

        if area_diff < min_area_diff:
            min_area_diff = area_diff
            best_match = item

    # 3. Laske hinta lähimmän pinta-alan neliöhinnalla
    if best_match:
        best_match_area = best_match['leveys'] * best_match['korkeus']
        price_per_area = best_match['hinta'] / best_match_area
        estimated_price = target_area * price_per_area
        logging.info(f"Lähin vastaava pinta-ala {best_match_area} (L: {best_match['leveys']}, K: {best_match['korkeus']}) antaa €/pinta-ala: {price_per_area:.4f}")
        return round(estimated_price, 2)
    else:
        # Tähän ei pitäisi päätyä, jos dataa on
        logging.warning("Virhe: Ei voitu löytää sopivaa vastinetta datasta.")
        return None





# --- Esimerkkikäyttö ---

# Testataan kokoa, joka on listassa
leveys1 = 14
korkeus1 = 20
hinta1 = laske_ikkunan_hinta(leveys1, korkeus1)
if hinta1 is not None:
    print(f"Ikkunan ({leveys1}x{korkeus1}) arvioitu hinta: {hinta1:.2f} € (Tarkka hinta listasta)")

# Testataan kokoa, jota ei ole listassa
leveys2 = 10
korkeus2 = 15
hinta2 = laske_ikkunan_hinta(leveys2, korkeus2)
if hinta2 is not None:
    print(f"Ikkunan ({leveys2}x{korkeus2}) arvioitu hinta: {hinta2:.2f} € (Arvioitu lähimmän pinta-alan perusteella)")

# Testataan toista kokoa, jota ei ole listassa
leveys3 = 5
korkeus3 = 10
hinta3 = laske_ikkunan_hinta(leveys3, korkeus3)
if hinta3 is not None:
    print(f"Ikkunan ({leveys3}x{korkeus3}) arvioitu hinta: {hinta3:.2f} € (Arvioitu lähimmän pinta-alan perusteella)")

# Testataan virheellistä syötettä
hinta4 = laske_ikkunan_hinta(-5, 10)