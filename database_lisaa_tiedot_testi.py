from utils.file_handler import lue_json_tiedosto
from config_data import IKKUNA2_JSON

from sqlalchemy import create_engine, text, Column, Integer, String, DateTime, DECIMAL, Boolean, ForeignKey, Text, TIMESTAMP
import datetime
import sys

DATABASE_URL = "postgresql://eka_tietokanta_user:Ipi86uNZg0FCRXcCSzGODzIteTVqUcyS@dpg-cvbac9jtq21c73dt8ho0-a.oregon-postgres.render.com/eka_tietokanta"
engine = create_engine(DATABASE_URL)

def lisaa_ikkuna_tauluun(input):
    json_data = lue_json_tiedosto(input)
    print(json_data)
    for ikkuna in json_data:
        print(ikkuna)
        koko = ikkuna.get("mm_koko")
        turvalasi = ikkuna.get("turvalasi")
        valikarmi = ikkuna.get("välikarmi")
        salekaihtimet = ikkuna.get("sälekaihtimet")

        leveys = koko.split("x")[0]
        korkeus = koko.split("x")[1]

        print(f"Leveys: {leveys}, Korkeus: {korkeus}")

        with engine.connect() as connection:
            connection.execute(text("""
            INSERT INTO ikkunat (leveys, korkeus, turvalasi, valikarmi, salekaihtimet)
            VALUES (:leveys, :korkeus, :turvalasi, :välikarmi, :sälekaihtimet)
            """), {
                "leveys": leveys,
                "korkeus": korkeus,
                "turvalasi": turvalasi,
                "välikarmi": valikarmi,
                "sälekaihtimet": salekaihtimet
            })
            connection.commit()

def hae_ikkunat_taulusta():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM ikkunat"))
        print(result)
        print("--------------------------------")
        for row in result:
            print(row)


#lisaa_ikkuna_tauluun(IKKUNA2_JSON)
hae_ikkunat_taulusta()







