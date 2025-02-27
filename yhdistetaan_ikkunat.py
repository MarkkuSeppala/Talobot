'''
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
        koko = item["mm_koko"]  # Muoto esim. "300x2300"
        yhdistetyt_ikkunat[koko] = {
            "Sievitalo_mm_koko": item["mm_koko"],
            "Kastellin_pyoristetty_koko": None,
            "Sievitalo_turvalasi": item["turvalasi"],
            "Kastelli_turvalasi": None,
            "Sievitalo_välikarmi": item["välikarmi"],
            "Kastelli_välikarmi": None,
            "Sievitalo_sälekaihtimet": item["sälekaihtimet"],
            "Kastelli_sälekaihtimet": None
        }

    # **Käsitellään Kastellin ikkunat**
    for item in kastelli_data:
        koko = item["pyoristetty_koko"]  # Muoto esim. "800x500"
        if koko in yhdistetyt_ikkunat:
            # Täydennetään olemassa olevaa riviä
            yhdistetyt_ikkunat[koko]["Kastellin_pyoristetty_koko"] = item["pyoristetty_koko"]
            yhdistetyt_ikkunat[koko]["Kastelli_turvalasi"] = item["turvalasi"]
            yhdistetyt_ikkunat[koko]["Kastelli_välikarmi"] = item["välikarmi"]
            yhdistetyt_ikkunat[koko]["Kastelli_sälekaihtimet"] = item["sälekaihtimet"]
        else:
            # Lisätään uusi rivi Kastellin ikkunalle
            yhdistetyt_ikkunat[koko] = {
                "Sievitalo_mm_koko": None,
                "Kastellin_pyoristetty_koko": item["pyoristetty_koko"],
                "Sievitalo_turvalasi": None,
                "Kastelli_turvalasi": item["turvalasi"],
                "Sievitalo_välikarmi": None,
                "Kastelli_välikarmi": item["välikarmi"],
                "Sievitalo_sälekaihtimet": None,
                "Kastelli_sälekaihtimet": item["sälekaihtimet"]
            }

    # **Muutetaan sanakirja listaksi ja lajitellaan leveyden mukaan**
    output_json = sorted(yhdistetyt_ikkunat.values(), key=lambda x: 
                         int(x["Sievitalo_mm_koko"].split("x")[0]) if x["Sievitalo_mm_koko"] 
                         else int(x["Kastellin_pyoristetty_koko"].split("x")[0]))

    # Tallennetaan yhdistetyt ikkunat tiedostoon
    with open(output_tiedosto, "w", encoding="utf-8") as tiedosto:
        json.dump(output_json, tiedosto, ensure_ascii=False, indent=4)

    print("Yhdistetyt ikkunat tallennettu tiedostoon:", output_tiedosto)

# **Uusi metodi, joka kutsuu yhdistämistoimintoa oikeilla tiedostopolkuilla**

'''
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

