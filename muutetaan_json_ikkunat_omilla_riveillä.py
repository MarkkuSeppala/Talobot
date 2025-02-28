import json

import json
import math

# Alkuperäinen JSON-tiedosto
input_json = [
    {"koko": "2030x2290", "kpl": 3, "turvalasi": True, "välikarmi": False, "sälekaihtimet": True},
    {"koko": "1130x2290", "kpl": 1, "turvalasi": True, "välikarmi": False, "sälekaihtimet": True},
    {"koko": "1130x390", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True},
    {"koko": "1730x490", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True},
    {"koko": "1130x2290", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True},
    {"koko": "1130x2290", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True},
    {"koko": "830x2090", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True},
    {"koko": "830x2090", "kpl": 1, "turvalasi": False, "välikarmi": False, "sälekaihtimet": True}
]

# Muunnetaan tiedot niin, että jokainen ikkuna on oma lohkonsa
output_json = []

for item in input_json:
    leveys, korkeus = map(int, item["koko"].split("x"))  # Muutetaan mitat kokonaisluvuiksi
    pyoristetty_leveys = round(leveys / 100) * 100  # Pyöristetään lähimpään 100 mm
    pyoristetty_korkeus = round(korkeus / 100) * 100  # Pyöristetään lähimpään 100 mm
    pyoristetty_koko = f"{pyoristetty_leveys}x{pyoristetty_korkeus}"

    for _ in range(item["kpl"]):
        output_json.append({
            "koko": item["koko"],
            "pyoristetty_koko": pyoristetty_koko,  # Lisätään uusi kenttä
            "turvalasi": item["turvalasi"],
            "välikarmi": item["välikarmi"],
            "sälekaihtimet": item["sälekaihtimet"]
        })

# Tallennetaan muunnettu JSON-tiedosto
with open("muunnettu_ikkunat.json", "w", encoding="utf-8") as f:
    json.dump(output_json, f, ensure_ascii=False, indent=4)

# Tulostetaan muunnettu JSON
print(json.dumps(output_json, ensure_ascii=False, indent=4))

