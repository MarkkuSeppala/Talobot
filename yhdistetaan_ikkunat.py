#============== YHDISTETÄÄN SIEVITALO JA KASTELLI IKKUNAT ============#
#=====================================================================#
#=====================================================================#
#=====================================================================#


import json

def yhdista_ikkunat(sievitalo_tiedosto, kastelli_tiedosto, output_tiedosto):
    # Ladataan JSON-tiedot
    with open(sievitalo_tiedosto, "r", encoding="utf-8") as tiedosto:
        sievitalo_data = json.load(tiedosto)

    with open(kastelli_tiedosto, "r", encoding="utf-8") as tiedosto:
        kastelli_data = json.load(tiedosto)

    yhdistetyt_ikkunat = {}

    # **Käsitellään Sievitalon ikkunat**
    for item in sievitalo_data:
        koko = item.get("mm_koko", "Tuntematon")  # Varmistetaan, että avain on olemassa
        yhdistetyt_ikkunat[koko] = {
            "Sievitalo_mm_koko": koko,
            "Kastellin_pyoristetty_koko": None,
            "Sievitalo_turvalasi": item.get("turvalasi", None),
            "Kastelli_turvalasi": None,
            "Sievitalo_välikarmi": item.get("välikarmi", None),
            "Kastelli_välikarmi": None,
            "Sievitalo_sälekaihtimet": item.get("sälekaihtimet", None),
            "Kastelli_sälekaihtimet": None
        }

    # **Käsitellään Kastellin ikkunat**
    for item in kastelli_data:
        koko = item.get("pyoristetty_koko", "Tuntematon")  # Varmistetaan, että avain on olemassa
        if koko in yhdistetyt_ikkunat:
            # Täydennetään olemassa olevaa riviä
            yhdistetyt_ikkunat[koko]["Kastellin_pyoristetty_koko"] = koko
            yhdistetyt_ikkunat[koko]["Kastelli_turvalasi"] = item.get("turvalasi", None)
            yhdistetyt_ikkunat[koko]["Kastelli_välikarmi"] = item.get("välikarmi", None)
            yhdistetyt_ikkunat[koko]["Kastelli_sälekaihtimet"] = item.get("sälekaihtimet", None)
        else:
            # Lisätään uusi rivi Kastellin ikkunalle
            yhdistetyt_ikkunat[koko] = {
                "Sievitalo_mm_koko": None,
                "Kastellin_pyoristetty_koko": koko,
                "Sievitalo_turvalasi": None,
                "Kastelli_turvalasi": item.get("turvalasi", None),
                "Sievitalo_välikarmi": None,
                "Kastelli_välikarmi": item.get("välikarmi", None),
                "Sievitalo_sälekaihtimet": None,
                "Kastelli_sälekaihtimet": item.get("sälekaihtimet", None)
            }

    # **Muutetaan sanakirja listaksi ja lajitellaan leveyden mukaan**
    try:
        output_json = sorted(
            yhdistetyt_ikkunat.values(),
            key=lambda x: int(x["Sievitalo_mm_koko"].split("x")[0]) if x["Sievitalo_mm_koko"] else int(x["Kastellin_pyoristetty_koko"].split("x")[0])
        )
    except Exception as e:
        print("Virhe lajittelussa:", str(e))
        output_json = list(yhdistetyt_ikkunat.values())

    # Tallennetaan yhdistetyt ikkunat tiedostoon
    with open(output_tiedosto, "w", encoding="utf-8") as tiedosto:
        json.dump(output_json, tiedosto, ensure_ascii=False, indent=4)

    print("Yhdistetyt ikkunat tallennettu tiedostoon:", output_tiedosto)




#============== YHDISTETÄÄN SIEVITALO JA KASTELLI IKKUNAT ============#
#=====================================================================#
#=====================================================================#
#=====================================================================#




import json
import os

def laske_ja_tallenna_ikkunat(input_tiedosto, output_tiedosto):
    """Laskee määrät ja tallentaa JSON-tiedostoon."""

    # **Varmistetaan, että input-tiedosto on olemassa ja ei ole tyhjä**
    if not os.path.exists(input_tiedosto) or os.stat(input_tiedosto).st_size == 0:
        print(f"⚠️ Virhe: Lähdetiedosto {input_tiedosto} ei löydy tai on tyhjä.")
        return

    # **Ladataan JSON-tiedosto**
    try:
        with open(input_tiedosto, "r", encoding="utf-8") as tiedosto:
            json_data = json.load(tiedosto)
    except json.JSONDecodeError as e:
        print(f"❌ JSON-virhe tiedostossa {input_tiedosto}: {e}")
        return

    if not json_data:
        print(f"⚠️ Virhe: JSON-tiedosto {input_tiedosto} on tyhjä.")
        return

    # **Alustetaan laskurit**
    sievitalo_kpl = sum(1 for item in json_data if item.get("Sievitalo_mm_koko"))
    kastelli_kpl = sum(1 for item in json_data if item.get("Kastellin_pyoristetty_koko"))

    sievitalo_turvalasi = sum(1 for item in json_data if item.get("Sievitalo_turvalasi") is True)
    kastelli_turvalasi = sum(1 for item in json_data if item.get("Kastelli_turvalasi") is True)

    sievitalo_välikarmi = sum(1 for item in json_data if item.get("Sievitalo_välikarmi") is True)
    kastelli_välikarmi = sum(1 for item in json_data if item.get("Kastelli_välikarmi") is True)

    sievitalo_sälekaihtimet = sum(1 for item in json_data if item.get("Sievitalo_sälekaihtimet") is True)
    kastelli_sälekaihtimet = sum(1 for item in json_data if item.get("Kastelli_sälekaihtimet") is True)

    # **Lisätään tilastorivi JSON-taulukkoon**
    tilasto_rivi = {
        "Sievitalo_mm_koko": f"Yhteensä: {sievitalo_kpl}",
        "Kastellin_pyoristetty_koko": f"Yhteensä: {kastelli_kpl}",
        "Sievitalo_turvalasi": f"Yhteensä: {sievitalo_turvalasi}",
        "Kastelli_turvalasi": f"Yhteensä: {kastelli_turvalasi}",
        "Sievitalo_välikarmi": f"Yhteensä: {sievitalo_välikarmi}",
        "Kastelli_välikarmi": f"Yhteensä: {kastelli_välikarmi}",
        "Sievitalo_sälekaihtimet": f"Yhteensä: {sievitalo_sälekaihtimet}",
        "Kastelli_sälekaihtimet": f"Yhteensä: {kastelli_sälekaihtimet}"
    }

    json_data.append(tilasto_rivi)

    # **Varmistetaan, että hakemisto on olemassa**
    os.makedirs(os.path.dirname(output_tiedosto), exist_ok=True)

    # **Tallennetaan JSON-tiedosto**
    try:
        with open(output_tiedosto, "w", encoding="utf-8") as tiedosto:
            json.dump(json_data, tiedosto, ensure_ascii=False, indent=4)
        print(f"✅ Tilastot lisätty ja tallennettu tiedostoon: {output_tiedosto}")
    except Exception as e:
        print(f"❌ Virhe tallennettaessa {output_tiedosto}: {e}")



'''
input_ikkunat_yhdessa_json = "data/yhd/ikkunat_yhdessa_json.txt"
output_ikkunat_yhdessa_json_2 = "data/yhd/ikkunat_yhdessa_json_2.txt"
laske_ja_tallenna_ikkunat(input_ikkunat_yhdessa_json, output_ikkunat_yhdessa_json_2)
'''