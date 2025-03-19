from sqlalchemy import text
from db_config import SessionLocal

def update_toimitussisallot_table():
    """Päivittää `toimitussisallot`-taulun lisäämällä puuttuvat sarakkeet ja muuttamalla asetukset."""
    try:
        with SessionLocal() as db:
            print("🔹 Päivitetään `toimitussisallot`-taulua...")

            # 🔹 Lisätään puuttuvat sarakkeet (jos eivät ole olemassa)
            alter_statements = [
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS uuid VARCHAR(36) UNIQUE NOT NULL",
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS pdf_url TEXT NOT NULL",
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS txt_sisalto TEXT NOT NULL",
                "ALTER TABLE toimitussisallot ADD COLUMN IF NOT EXISTS toimittaja VARCHAR(100) NOT NULL"
            ]

            # 🔹 Muutetaan sarakkeiden `NULL`-asetuksia
            alter_nullable_statements = [
                "ALTER TABLE toimitussisallot ALTER COLUMN kayttaja_id SET NOT NULL",
                "ALTER TABLE toimitussisallot ALTER COLUMN created_at SET NOT NULL",
                "ALTER TABLE toimitussisallot ALTER COLUMN aktiivinen SET NOT NULL"
            ]

            # 🔹 Suoritetaan ALTER TABLE -komennot
            for stmt in alter_statements + alter_nullable_statements:
                try:
                    db.execute(text(stmt))
                except Exception as e:
                    print(f"❌ Virhe suoritettaessa: {stmt}")
                    print(f"   ➝ {e}")

            db.commit()
            print("✅ `toimitussisallot`-taulu päivitetty onnistuneesti!")

    except Exception as e:
        print(f"❌ Virhe tietokantapäivityksessä: {e}")

if __name__ == "__main__":
    update_toimitussisallot_table()
