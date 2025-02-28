import os
import tkinter as tk
from tkinter import filedialog
import sys

# Lisätään oikea hakemisto moduulin hakupolkuun
sys.path.append(r"C:\Talobot")

from k_ikkuna import muuta_tekstiksi2  # Tuodaan valmis funktio

# Luodaan piilotettu Tkinter-ikkuna
root = tk.Tk()
root.withdraw()

# Avataan tiedostonvalitsin
pdf_polku = filedialog.askopenfilename(title="Valitse PDF-tiedosto", filetypes=[("PDF Files", "*.pdf")])

# Tarkistetaan, valitsiko käyttäjä tiedoston
if pdf_polku:
    try:
        with open(pdf_polku, "rb") as tiedosto:
            print("\n🚀 Kutsutaan muuta_tekstiksi-metodia...")
            muuta_tekstiksi2(tiedosto)  # Annetaan tiedosto suoraan funktiolle
            print("\n✅ muuta_tekstiksi-metodi suoritettu!")

        print(f"\n✅ PDF käsitelty onnistuneesti! ({os.path.basename(pdf_polku)})")

    except Exception as e:
        print(f"\n❌ Virhe PDF:n käsittelyssä: {e}")
else:
    print("\n❌ Tiedostoa ei valittu.")


