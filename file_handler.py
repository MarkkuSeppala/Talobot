import os





#==================================================================================================#
#==================================================================================================#
#==================================================================================================#


# Lukee annetun txt-tiedoston ja palauttaa sen sisällön merkkijonona."""
def lue_txt_tiedosto(tiedostopolku: str) -> str:
    try:
        with open(tiedostopolku, "r", encoding="utf-8") as tiedosto:
            return tiedosto.read()
    except FileNotFoundError:
        print(f"Virhe: Tiedostoa '{tiedostopolku}' ei löytynyt.")
        return ""
    except Exception as e:
        print(f"Virhe tiedostoa luettaessa: {e}")

        return ""
    
#==================================================================================================#


#Kirjoittaa annetun tekstin tiedostoon annettuun polkuun.
#Palauttaa virheen, jos tiedostopolku ei ole kelvollinen.
def kirjoita_txt_tiedosto(sisalto: str, tiedostopolku: str):
    
    try:
        if not sisalto:
            raise ValueError("Virhe: Sisältö ei voi olla tyhjä.")

        if not tiedostopolku or not tiedostopolku.endswith(".txt"):
            raise ValueError("Virhe: Tiedostopolun täytyy olla kelvollinen .txt-tiedosto.")

        os.makedirs(os.path.dirname(tiedostopolku), exist_ok=True)  # Luo kansiot tarvittaessa

        with open(tiedostopolku, "w", encoding="utf-8") as tiedosto:
            tiedosto.write(sisalto)

        print(f"Tiedosto kirjoitettu onnistuneesti: {tiedostopolku}")

    except Exception as e:
        print(f"Virhe tiedostoa kirjoittaessa: {e}")


    