# Vertailun Pipeline - Kotiko Asuntoanalyysipalvelu

## Yleiskuvaus

Vertailun pipeline on Kotiko-palvelun ydinosa, joka mahdollistaa kahden toimitussisällön (esim. tarjousten) vertailun ja analyysin. Pipeline käyttää tekoälyä (OpenAI GPT) tuotteiden tunnistamiseen ja vertailuun.

## Pipeline-arkkitehtuuri

### 1. Tietojen Vastaanotto
```
PDF-tiedosto → Tekstin poiminta → Puhdistettu toimitussisältö
```

### 2. Tuotteiden Tunnistus
```
Puhdistettu toimitussisältö + Tuotelistaus → AI-analyysi → Tuotteiden tunnistus
```

### 3. Vertailun Suoritus
```
Tuotteiden tunnistus + Vertailukohde → Vertailu → Tulosten tallennus
```

## Tärkeimmät Komponentit

### Tuotteet-taulun hallinta (`SQL_kyselyt_tuotteet_tauluun.py`)

#### Tuotteiden tuonti
- **`tuo_tuotteet_sheetista(csv_url)`**: Tuo tuotteet Google Sheets -taulukosta
- **`siisti_arvo(arvo)`**: Puhdistaa ja validoi tuotetietoja
- **Tuetut kentät**:
  - `version_number`: Tuotteen versio
  - `valid_from/valid_to`: Voimassaoloaika
  - `prompt_1/2/3`: Tekoälyn käyttöoikeudet
  - `tuote`: Tuotteen nimi
  - `yksikko`: Mittayksikkö
  - `hinta`: Hinta
  - `tarkenne_*`: Toimittajakohtaiset tarkennukset

#### Tuotteiden haku
- **`hae_tuotteet_prompt_1_tuote_tarkenne_yleinen()`**: Hakee prompt_1=True tuotteet
- **`hae_tuotteet_prompt_1_tuote_tarkenne_yleinen_tarkenne_sievitalo()`**: Hakee Sievitalo-spesifiset tuotteet
- **`hae_tuotteet_tarkenne_sievitalo()`**: Hakee uniikit Sievitalo-tarkennukset

### Vertailun hallinta (`SQL_kyselyt.py`)

#### Vertailun luonti
- **`lisaa_vertailu(toimitussisalto_1_id, toimitussisalto_2_id)`**: Luo uusi vertailu
- **`hae_kaikki_vertailut()`**: Listaa kaikki vertailut aikajärjestyksessä

#### Vertailutietojen haku
- **`hae_vertailun_toimitussisalto_1_tiedot(vertailu_id)`**: Hakee ensimmäisen toimitussisällön tiedot
- **`hae_vertailun_toimitussisalto_2_tiedot(vertailu_id)`**: Hakee toisen toimitussisällön tiedot

## Toimittajakohtaiset Pipeline-t

### Sievitalo (`run.py`)

```python
def run_sievitalo(toimitussisalto_pdf, toimitussisalto_id):
    # 1. Toimitussisällön puhdistus
    puhdistettu_toimitussisalto = siivoo_toimitussisalto(...)
    
    # 2. Ikkunatietojen poiminta
    ikkunat = api_kysely(PROMPT_SIEVITALO_POIMI_IKKUNATIEDOT, ...)
    
    # 3. Ulko-ovien poiminta
    ulko_ovet = api_kysely(PROMPT_SIEVITALO_POIMI_ULKO_OVI_TIEDOT, ...)
    
    # 4. Väliovien poiminta
    valio_ovet = api_kysely(PROMPT_SIEVITALO_POIMI_VALIOVITIEDOT, ...)
    
    # 5. Tuotteiden tunnistus
    tuotteet = hae_tuotteet_if_prompt_1_true()
    toimitussisalto_tuotteet = api_kysely_nelja_parametria(...)
    
    # 6. Tietojen tallennus kantaan
    lisaa_ikkunat_kantaan(ikkunat, toimitussisalto_id)
    lisaa_ulko_ovet_kantaan(ulko_ovet, toimitussisalto_id)
    lisaa_valiovet_kantaan(valio_ovet, toimitussisalto_id)
    tallenna_ai_hakutulokset_kantaan(toimitussisalto_tuotteet)
```

### Kastelli (`run.py`)

```python
def run_kastelli(toimitussisalto_txt_polku, toimitussisalto_id):
    # Samankaltainen pipeline kuin Sievitalolla
    # Käyttää Kastelli-spesifisiä prompteja
```

### Designtalo (`run.py`)

```python
def run_designtalo(toimitussisalto_pdf, toimitussisalto_id):
    # Designtalo-spesifinen pipeline
    # Käyttää millimetrejä kokoja varten
```

## Tekoälyn Integraatio

### Prompt-rakenne
1. **Tuotteiden tunnistus**: "Olet talonrakentamisen ammattilainen..."
2. **Tuotteiden yhdistäminen**: Vertaa tuotelistauksen ja löydettyjen tuotteiden välillä
3. **JSON-muotoinen vastaus**: Standardoitu rakenne tunnistuksille

### API-kyselyt
- **`api_kysely()`**: Perus OpenAI API -kutsu
- **`api_kysely_nelja_parametria()`**: Neljän parametrin kysely (toimitussisältö + tuotelistaus)

## Tietokantarakenne

### Päätaulut
- **`tuotteet`**: Tuotemasterdata
- **`toimitussisallot`**: PDF-tiedostot ja tekstit
- **`ikkunat`**: Ikkunatiedot
- **`ulko_ovet`**: Ulko-ovien tiedot
- **`valiovet`**: Väliovien tiedot
- **`vertailut`**: Vertailujen linkitykset

### Avainkentät
- **`toimitussisalto_id`**: Linkittää kaikki tiedot toimitussisältöön
- **`vertailu_id`**: Linkittää vertailut toimitussisältöihin

## Virheenkäsittely

### Logging
- **`configure_logging()`**: Keskitetty lokitus
- **Virheiden tallennus**: Kaikki virheet lokitetaan

### Tietokantavirheet
- **`SessionLocal()`**: Automaattinen session-hallinta
- **`try-except-finally`**: Varmistaa resurssien vapauttamisen

## Suorituskyky ja Optimoinnit

### Batch-käsittely
- Tuotteiden lisäys 10:n ryhmissä
- Tietokantayhteyksien uudelleenkäyttö

### Indeksit
- `prompt_1` -indeksi tuotteiden haussa
- `toimitussisalto_id` -indeksi liitostauluissa

## Tulevaisuuden Kehityssuunnat

### Mahdolliset parannukset
1. **Cache-järjestelmä**: Tuotteiden välimuisti
2. **Asynkroninen käsittely**: Rinnakkaiset API-kutsut
3. **Machine Learning**: Tuotteiden automaattinen luokittelu
4. **Real-time vertailu**: Live-vertailut

### Skalautuvuus
- **Mikropalvelurakenne**: Eri toimittajille omat palvelut
- **Queue-järjestelmä**: Taustalla suoritettavat vertailut
- **CDN**: PDF-tiedostojen nopea jakelu

## Yhteenveto

Vertailun pipeline on monimutkainen mutta hyvin suunniteltu järjestelmä, joka:
- Käsittelee eri toimittajien toimitussisällöt
- Käyttää tekoälyä tuotteiden tunnistamiseen
- Tallentaa kaikki tiedot strukturoidusti
- Mahdollistaa vertailujen suorittamisen
- On laajennettavissa uusille toimittajille

Pipeline on suunniteltu modulaarisesti, mikä tekee siitä ylläpidettävän ja laajennettavan.
