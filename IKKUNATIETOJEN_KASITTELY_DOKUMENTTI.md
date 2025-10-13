# Ikkunatietojen käsittely Kotiko-sovelluksessa

## Yleiskuvaus

Tämä dokumentti kuvaa, miten ikkunatiedot käsitellään Kotiko-sovelluksessa sen jälkeen, kun toimitussisältö on tallennettu tietokantaan. Prosessi sisältää PDF-tiedostojen lataamisen, tekstin puhdistamisen, AI-analyysin ja lopullisen tallentamisen tietokantaan.

## Käsittelypipeline

### 1. Toimitussisällön vastaanotto ja tallennus

**Tiedosto:** `SQL_kyselyt.py`  
**Funktio:** `vastaanota_toimitussisalto(file)`

```python
def vastaanota_toimitussisalto(file) -> str:
    # 1. Luo yksilöllinen UUID
    unique_id = str(uuid.uuid4())
    
    # 2. Tallenna PDF palvelimelle
    pdf_filepath = anna_polku(unique_id)
    with open(pdf_filepath, "wb") as f:
        f.write(file_data)
    
    # 3. Muunna PDF tekstiksi
    teksti = muuta_pdf_tekstiksi(io.BytesIO(file_data))
    
    # 4. Tunnista toimittaja
    toimittaja = tunnista_toimittaja(teksti)
    
    # 5. Tallenna teksti tiedostoksi
    txt_filepath = UPLOAD_FOLDER_DATA / f"{unique_id}.txt"
    kirjoita_txt_tiedosto(teksti, txt_filepath)
    
    # 6. Tallenna tietokantaan
    tallenna_toimitussisalto_tietokantaan(toimittaja, pdf_filepath, txt_filepath, unique_id)
    
    return unique_id
```

### 2. Toimittajakohtainen käsittely

**Tiedosto:** `run.py`  
**Funktiot:** `run_sievitalo()` ja `run_kastelli()`

Kun toimitussisältö on tallennettu, järjestelmä tunnistaa toimittajan ja kutsuu sopivaa käsittelyfunktiota:

#### Sievitalo-käsittely

```python
def run_sievitalo(toimitussisalto_pdf, toimitussisalto_id):
    # 1. Puhdista toimitussisältö
    puhdistettu_toimitussisalto = muuta_pdf_ja_puhdista_teksti_docling(toimitussisalto_pdf)
    puhdistettu_toimitussisalto = f"**TOIMITUSSISÄLTÖ START**\n{puhdistettu_toimitussisalto}\n**TOIMITUSSISÄLTÖ END**"
    
    # 2. Ikkunatiedot
    ikkunatiedot_kokonaisuudessa = api_kysely(GENERATION_CONFIG, PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT, puhdistettu_toimitussisalto)
    ikkunat_json = api_kysely(GENERATION_CONFIG_JSON, PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, ikkunatiedot_kokonaisuudessa)
    lisaa_ikkunat_kantaan_ja_koko_x_100(ikkunat_json, toimitussisalto_id)
    
    # 3. Ulko-ovet
    ulko_ovet = api_kysely(GENERATION_CONFIG, PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT_TXT, puhdistettu_toimitussisalto)
    ulko_ovet = api_kysely_ulko_ovet(GENERATION_CONFIG, PROMPT_SIEVITALO_ULKO_OVI_TIEDOT_LUOKKAMUOTOON, ulko_ovet)
    lisaa_ulko_ovet_kantaan(ulko_ovet, toimitussisalto_id)
    
    # 4. Väliovet
    valio_ovet = api_kysely(GENERATION_CONFIG, PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT_TXT, puhdistettu_toimitussisalto)
    valio_ovet = api_kysely(GENERATION_CONFIG, PROMPT_SIEVITALO_ANNA_VALIOVIMALLIT_TXT, valio_ovet)
    lisaa_valiovet_kantaan(valio_ovet, toimitussisalto_id)
    
    # 5. Tuotteet
    tuotteet = hae_tuotteet_if_prompt_1_true()
    toimitussisalto_tuotteet = api_kysely_nelja_parametria(GENERATION_CONFIG, PROMPT_POIMI_TUOTTEET_1_TXT, puhdistettu_toimitussisalto, tuotteet)
    tallenna_ai_hakutulokset_kantaan(toimitussisalto_tuotteet)
```

#### Kastelli-käsittely

```python
def run_kastelli(toimitussisalto_txt_polku: str, toimitussisalto_id: str):
    # 1. Puhdista toimitussisältö
    puhdistettu_toimitussisalto = puhdista_teksti(toimitussisalto_txt_polku)
    puhdistettu_toimitussisalto = f"**TOIMITUSSISÄLTÖ START**\n{puhdistettu_toimitussisalto}\n**TOIMITUSSISÄLTÖ END**"
    
    # 2. Ikkunatiedot
    ikkunatiedot_kokonaisuudessa = api_kysely(GENERATION_CONFIG, PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT, puhdistettu_toimitussisalto)
    ikkunat_json = api_kysely(GENERATION_CONFIG_JSON, PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON, ikkunatiedot_kokonaisuudessa)
    lisaa_ikkunat_kantaan(ikkunat_json, toimitussisalto_id)
    
    # 3. Ulko-ovet
    ulko_ovet = api_kysely(GENERATION_CONFIG, PROMPT_KASTELLI_POIMI_ULKO_OVI_TIEDOT_TXT, puhdistettu_toimitussisalto)
    ulko_ovet = api_kysely_ulko_ovet(GENERATION_CONFIG, PROMPT_KASTELLI_ULKO_OVI_TIEDOT_LUOKKAMUOTOON, ulko_ovet)
    lisaa_ulko_ovet_kantaan(ulko_ovet, toimitussisalto_id)
    
    # 4. Väliovet
    valio_ovet = api_kysely(GENERATION_CONFIG, PROMPT_KASTELLI_POIMI_VALIOVITIEDOT_TXT, puhdistettu_toimitussisalto)
    valio_ovet = api_kysely(GENERATION_CONFIG, PROMPT_KASTELLI_ANNA_VALIOVIMALLIT_TXT, valio_ovet)
    lisaa_valiovet_kantaan(valio_ovet, toimitussisalto_id)
    
    # 5. Tuotteet
    tuotteet = hae_tuotteet_prompt1_str()
    toimitussisalto_tuotteet = api_kysely_nelja_parametria(GENERATION_CONFIG, PROMPT_KASTELLI_POIMI_TUOTTEET_TXT, puhdistettu_toimitussisalto, tuotteet)
    lisaa_toimitussisalto_tuotteet_kantaan(toimitussisalto_tuotteet, toimitussisalto_id)
```

### 3. Ikkunatietojen tallennus tietokantaan

**Tiedosto:** `SQL_kyselyt.py`  
**Funktiot:** `lisaa_ikkunat_kantaan()` ja `lisaa_ikkunat_kantaan_ja_koko_x_100()`

#### Sievitalo-ikkunat (koko kerroin x100)

```python
def lisaa_ikkunat_kantaan_ja_koko_x_100(ikkunat_json_str, toimitussisalto_id: int):
    # 1. Muunna JSON Python-listaksi
    ikkunat_lista = json.loads(ikkunat_json_str)
    
    with SessionLocal() as db:
        for ikkuna_data in ikkunat_lista:
            # 2. Parsitaan leveys ja korkeus koko-kentästä
            leveys_dm, korkeus_dm = map(int, ikkuna_data["koko"].split('x'))
            
            # 3. Luodaan ikkuna jokaiselle kappaleelle
            for _ in range(ikkuna_data["kpl"]):
                # 4. Muunnetaan mitat millimetreiksi (x100)
                leveys_mm = leveys_dm * 100
                korkeus_mm = korkeus_dm * 100
                
                # 5. Luodaan uusi ikkuna-tietue
                uusi_ikkuna = Ikkuna(
                    leveys=leveys_mm,
                    korkeus=korkeus_mm,
                    turvalasi=ikkuna_data["turvalasi"],
                    valikarmi=ikkuna_data["välikarmi"],
                    salekaihtimet=ikkuna_data["sälekaihtimet"],
                    toimitussisalto_id=toimitussisalto_id
                )
                db.add(uusi_ikkuna)
        
        db.commit()
```

#### Kastelli-ikkunat (suora tallennus)

```python
def lisaa_ikkunat_kantaan(ikkunat_json_str, toimitussisalto_id: int):
    # 1. Muunna JSON Python-listaksi
    ikkunat_lista = json.loads(ikkunat_json_str)
    
    with SessionLocal() as db:
        for ikkuna_data in ikkunat_lista:
            # 2. Parsitaan leveys ja korkeus koko-kentästä
            leveys, korkeus = map(int, ikkuna_data["koko"].split('x'))
            
            # 3. Luodaan ikkuna jokaiselle kappaleelle
            for _ in range(ikkuna_data["kpl"]):
                # 4. Luodaan uusi ikkuna-tietue (ei kerrointa)
                uusi_ikkuna = Ikkuna(
                    leveys=leveys,
                    korkeus=korkeus,
                    turvalasi=ikkuna_data["turvalasi"],
                    valikarmi=ikkuna_data["välikarmi"],
                    salekaihtimet=ikkuna_data["sälekaihtimet"],
                    toimitussisalto_id=toimitussisalto_id
                )
                db.add(uusi_ikkuna)
        
        db.commit()
```

### 4. Tietokantarakenteet

**Tiedosto:** `db_luokat.py`

#### Ikkuna-taulun rakenne

```python
class Ikkuna(Base):
    __tablename__ = "ikkunat"
    
    id = Column(Integer, primary_key=True)
    leveys = Column(Integer, nullable=False)  # millimetreissä
    korkeus = Column(Integer, nullable=False)  # millimetreissä
    turvalasi = Column(Boolean, default=False)
    valikarmi = Column(Boolean, default=False)
    salekaihtimet = Column(Boolean, default=False)
    toimitussisalto_id = Column(Integer, ForeignKey("toimitussisallot.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### Toimitussisalto-taulun rakenne

```python
class Toimitussisalto(Base):
    __tablename__ = "toimitussisallot"
    
    id = Column(Integer, primary_key=True)
    kayttaja_id = Column(Integer, ForeignKey("kayttajat.id", ondelete="SET NULL"))
    toimittaja_id = Column(Integer, ForeignKey("toimittajat.id", ondelete="SET NULL"))
    uuid = Column(String(36), unique=True, nullable=False)
    pdf_url = Column(Text, nullable=False)
    txt_url = Column(Text, nullable=False)
    toimittaja = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    aktiivinen = Column(Boolean, default=True)
```

### 5. AI-analyysin promptit

**Tiedosto:** `config_data.py`

#### Sievitalo-ikkunat

```python
PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT_TXT = """
Poimi toimitussisällöstä kaikki ikkunatiedot.
Etsi seuraavat tiedot jokaiselle ikkunalle:
- Ikkunan tyyppi (esim. 2-ikkunainen, 3-ikkunainen)
- Koko (esim. 1200x1200, 1800x1200)
- Turvalasi (kyllä/ei)
- Välikarmi (kyllä/ei)
- Sälekaihtimet (kyllä/ei)
- Kappalemäärä
"""

PROMPT_SIEVITALO_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON = """
Muunna ikkunatiedot JSON-muotoon:
{
  "ikkunat": [
    {
      "tyyppi": "2-ikkunainen",
      "koko": "1200x1200",
      "turvalasi": true,
      "välikarmi": false,
      "sälekaihtimet": true,
      "kpl": 5
    }
  ]
}
"""
```

#### Kastelli-ikkunat

```python
PROMPT_KASTELLI_POIMI_IKKUNATIEDOT_TXT = """
Poimi toimitussisällöstä kaikki ikkunatiedot.
Etsi seuraavat tiedot jokaiselle ikkunalle:
- Ikkunan tyyppi
- Koko
- Turvalasi (kyllä/ei)
- Välikarmi (kyllä/ei)
- Sälekaihtimet (kyllä/ei)
- Kappalemäärä
"""

PROMPT_KASTELLI_RYHMITELLE_VALITUT_IKKUNATIEDOT_JSON_MUOTOON = """
Muunna ikkunatiedot JSON-muotoon:
{
  "ikkunat": [
    {
      "tyyppi": "1-ikkunainen",
      "koko": "600x1200",
      "turvalasi": false,
      "välikarmi": true,
      "sälekaihtimet": false,
      "kpl": 3
    }
  ]
}
"""
```

### 6. Tietojen hakeminen tietokannasta

**Tiedosto:** `SQL_kyselyt.py`

#### Kaikkien ikkunoiden haku

```python
def hae_kaikki_ikkunat():
    with SessionLocal() as db:
        kysely = text("""
            SELECT 
                i.id, i.leveys, i.korkeus, i.turvalasi, i.valikarmi, i.salekaihtimet,
                i.created_at, i.toimitussisalto_id, t.toimittaja, t.uuid
            FROM ikkunat i
            LEFT JOIN toimitussisallot t ON i.toimitussisalto_id = t.id
            ORDER BY i.toimitussisalto_id, i.leveys;
        """)
        
        tulokset = db.execute(kysely).fetchall()
        return tulokset
```

#### Tietyn toimitussisällön ikkunat

```python
def hae_toimitussisallon_ikkunat(toimitussisalto_id: int) -> list:
    with SessionLocal() as db:
        ikkunat = session.query(Ikkuna).filter(
            Ikkuna.toimitussisalto_id == toimitussisalto_id
        ).all()
        return ikkunat
```

### 7. Virheenkäsittely

Järjestelmä sisältää kattavan virheenkäsittelyn:

```python
try:
    # JSON-muunnos
    ikkunat_lista = json.loads(ikkunat_json_str)
    
    # Tietokantatallennus
    with SessionLocal() as db:
        # ... tallennuslogiikka ...
        db.commit()
        
except json.JSONDecodeError as e:
    logger.warning(f"❌ Virheellinen JSON-muoto: {str(e)}")
except KeyError as e:
    logger.warning(f"❌ Puuttuva kenttä JSON:issa: {str(e)}")
    db.rollback()
except Exception as e:
    logger.warning(f"❌ Virhe ikkunoiden lisäämisessä: {str(e)}")
    db.rollback()
```

## Yhteenveto

Ikkunatietojen käsittely Kotiko-sovelluksessa noudattaa seuraavaa järjestystä:

1. **PDF-lataus** → Tiedosto tallennetaan palvelimelle UUID:lla
2. **Tekstimuunnos** → PDF muunnetaan tekstiksi
3. **Toimittajan tunnistus** → Määritetään käsittelytapa (Sievitalo/Kastelli)
4. **AI-analyysi** → Tekoäly poimii ikkunatiedot tekstistä
5. **JSON-muunnos** → Tiedot muunnetaan strukturoiduksi JSON:ksi
6. **Tietokantatallennus** → Ikkunat tallennetaan `ikkunat`-tauluun
7. **Virheenkäsittely** → Mahdolliset virheet logitetaan ja käsitellään

Järjestelmä tukee eri toimittajien erilaisia ikkunamuotoja ja mittayksiköitä, ja varmistaa että kaikki tiedot tallennetaan oikein tietokantaan.
