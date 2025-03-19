import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship




from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv
from database import Base

# Lataa ympäristömuuttujat oikeasta tiedostosta
load_dotenv("ymparistomuuttujat.env")

# Haetaan tietokantayhteys
DATABASE_URL = os.getenv("DATABASE_URL")








# Tarkista, että muuttuja löytyy
if DATABASE_URL is None:
    raise ValueError("❌ Ympäristömuuttuja 'DATABASE_URL' ei latautunut. Tarkista tiedoston nimi ja sijainti.")

print(f"Tietokantayhteys: {DATABASE_URL}")

# Luo tietokantayhteys SQLAlchemylla
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
if __name__ == "__main__":
    suorita_kysely()



class Toimitussisalto(Base):
    __tablename__ = "toimitussisallot"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # ✅ UUID tunnisteena
    kayttaja_id = Column(Integer, ForeignKey("kayttajat.id"), nullable=False)
    toimittaja_id = Column(Integer, ForeignKey("toimittajat.id"), nullable=True)
    pdf_url = Column(String, nullable=False)  # ✅ PDF-tiedoston polku
    txt_url = Column(String, nullable=False)  # ✅ TXT-tiedoston polku
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))
    aktiivinen = Column(Boolean, default=True)

    toimittaja = relationship("Toimittaja", back_populates="toimitussisallot")


from sqlalchemy import create_engine, text
from database import engine  # Käyttää tietokannan yhteyttä

def get_table_structure(table_name):
    """Hakee ja näyttää tietokantataulun rakenteen (sarakkeet ja tyypit)."""
    query = text(f"""
        SELECT column_name, data_type, character_maximum_length, is_nullable
        FROM information_schema.columns
        WHERE table_name = :table_name
        ORDER BY ordinal_position
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"table_name": table_name}).fetchall()

    if not result:
        print(f"❌ Taulua '{table_name}' ei löytynyt.")
        return

    print(f"\n🔹 **Rakenne: {table_name}** 🔹")
    print(f"{'Sarakkeen nimi':<20} {'Tietotyyppi':<20} {'Pituus':<10} {'NULL?':<10}")
    print("=" * 60)

    for row in result:
        column_name, data_type, char_length, is_nullable = row
        char_length = char_length if char_length else "-"
        print(f"{column_name:<20} {data_type:<20} {char_length:<10} {is_nullable:<10}")

# 🔹 Ajetaan tarkistus tietylle taululle
if __name__ == "__main__":
    table_name = "toimitussisallot"  # Muuta haluamaksesi tauluksi
    get_table_structure(table_name)


get_table_structure("toimitussisallot")