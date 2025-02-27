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
def suorita_yhdistaminen():
    sievitalo_tiedosto = "data/s/ikkuna_json_2.txt"
    kastelli_tiedosto = "data/k/ikkuna_json_2.txt"
    output_tiedosto = "C:/Talobot/data/yhd/ikkunat_yhdessa.txt"

    print("Aloitetaan Sievitalon ja Kastellin ikkunoiden yhdistäminen...")
    yhdista_ikkunat(sievitalo_tiedosto, kastelli_tiedosto, output_tiedosto)
    print("Yhdistäminen valmis!")

# **Kutsutaan yhdistämismetodia**
suorita_yhdistaminen()
