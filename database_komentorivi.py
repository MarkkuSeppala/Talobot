from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from database import Base
import pandas as pd
import os
from dotenv import load_dotenv


# Lataa ympäristömuuttujat .env-tiedostosta

load_dotenv("ymparistomuuttujat.env")


# Haetaan tietokantayhteys
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Tietokantayhteys: {DATABASE_URL}")

# 🔹 Yhdistä PostgreSQL-tietokantaan (muuta oma DATABASE_URL)
#DATABASE_URL = "postgresql://eka_tietokanta_user:Ipi86uNZg0FCRXcCSzGODzIteTVqUcyS@dpg-cvbac9jtq21c73dt8ho0-a.oregon-postgres.render.com/eka_tietokanta"
engine = create_engine(DATABASE_URL)

def suorita_kysely():
    """Interaktiivinen PostgreSQL-komentorivi Pythonilla."""
    print("\n🔹 **PostgreSQL Python-kehote** – Kirjoita SQL-komento tai 'exit' poistuaksesi.\n")

    while True:
        sql = input("📝 SQL > ").strip()

        if sql.lower() == "exit":
            print("\n👋 Suljetaan yhteys. Kiitos!")
            break

        try:
            with engine.connect() as conn:
                result = conn.execute(text(sql))

                # Tarkistetaan, palauttaako kysely tuloksia
                if result.returns_rows:
                    df = pd.DataFrame(result.fetchall(), columns=result.keys())
                    print("\n📊 **Tulokset:**")
                    print(df if not df.empty else "✅ Ei tuloksia.")
                else:
                    conn.commit()
                    print("✅ Kysely suoritettu onnistuneesti!")

        except Exception as e:
            print(f"\n❌ Virhe: {e}")

# Käynnistä ohjelma
#if __name__ == "__main__":
    #suorita_kysely()
