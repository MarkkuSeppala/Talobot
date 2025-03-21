from pathlib import Path

test_path = Path("persistent_data/data/ladatut_toimitussisallot/testi.pdf")
test_path.parent.mkdir(parents=True, exist_ok=True)
with open(test_path, "wb") as f:
    f.write(b"Testidata")

print("Tallennettu:", test_path.exists(), test_path)
