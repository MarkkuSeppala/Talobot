# Talobot - Modulaarinen kehityssuunnitelma

## 🎯 Tavoite
Viedä projektia eteen päin modulaarisesti siten, että:
1. **Vaihe 1**: Kaikki tulosteet terminaaliin (backend-logiikka)
2. **Vaihe 2**: Selaimeen siirtymä (frontend) samalla logiikalla

## 📋 Nykyinen tilanne (Analyysi tehty: 2024-12-19)

### Projektin rakenne
```
talobot_env/
├── app.py (289 riviä) - Monoliittinen Flask-sovellus
├── run.py (343 riviä) - Toimittajakohtaiset funktiot
├── SQL_kyselyt.py (2500+ riviä) - Tietokantaoperaatiot
├── factory.py - Toimittajakohtaiset getter-funktiot
├── utils/ - Apufunktiot
├── models/ - Tietokantamallit
├── templates/ - HTML-templatet
└── data/ - Konfiguraatiotiedostot
```

### Tunnistetut ongelmat
- **Sekamainen rakenne**: Web-logiikka, business-logiikka ja data-käsittely sekaisin
- **Monoliittinen koodi**: Kaikki app.py:ssä
- **Vaikea testata**: Ei erillistä logiikkaa
- **Vaikea laajentaa**: Uudet toimittajat vaativat koodin muutoksia

## 🏗️ Ehdotettu modulaarinen rakenne

```
talobot_env/
├── backend/                    # Ydinlogiikka (terminaalitulostukset)
│   ├── core/                  # Ydinlogiikka
│   │   ├── __init__.py
│   │   ├── document_processor.py    # PDF-käsittely
│   │   ├── ai_analyzer.py          # AI-analyysi (Gemini/Groq)
│   │   ├── data_extractor.py       # Tietojen poiminta
│   │   └── supplier_detector.py    # Toimittajan tunnistus
│   ├── models/                # Tietomallit
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── entities.py
│   ├── services/              # Palvelut
│   │   ├── __init__.py
│   │   ├── sievitalo_service.py
│   │   ├── kastelli_service.py
│   │   └── designtalo_service.py
│   └── terminal/              # Terminaalikäyttöliittymä
│       ├── __init__.py
│       ├── cli.py
│       └── output_formatter.py
├── frontend/                  # Selaimeen siirtymä (tulevaisuudessa)
│   ├── web/                   # Web-käyttöliittymä
│   └── api/                   # REST API
├── shared/                    # Jaetut apufunktiot
│   ├── __init__.py
│   ├── file_handler.py
│   ├── logger_config.py
│   └── config_data.py
└── main.py                    # Pääkäynnistys
```

## 🚀 Kehitysstrategia

### Vaihe 1: Terminaalitulostukset (NYKYINEN)
**Tavoite**: Kaikki toiminnallisuus terminaaliin

**Tehtävät**:
1. ✅ Analysoi nykyinen rakenne
2. 🔄 Luo modulaarinen rakenne
3. ⏳ Erota ydinlogiikka web-rajapinnasta
4. ⏳ Luo terminaalikäyttöliittymä
5. ⏳ Testaa kaikki toiminnallisuudet terminaalissa

**Käyttö**:
```bash
python main.py --mode terminal
python main.py --analyze sievitalo.pdf kastelli.pdf
python main.py --compare 123 456
```

### Vaihe 2: Selaimeen siirtymä (TULEVAISUUDESSA)
**Tavoite**: Sama logiikka selaimeen

**Tehtävät**:
1. ⏳ Käytä samaa ydinlogiikkaa
2. ⏳ Lisää web-rajapinta
3. ⏳ Säilytä terminaalituki

## 📊 Modulaarisuuden edut

### 1. Varmuus
- Voit testata logiikan terminaalissa ennen web-kompleksisuutta
- Selkeät virheilmoitukset
- Helppo debug

### 2. Modulaarisuus
- Jokainen osa on itsenäinen
- Helppo testata yksittäisiä osia
- Uudelleenkäytettävyys

### 3. Asteittainen kehitys
- Voit lisätä ominaisuuksia vaihe vaiheelta
- Ei tarvitse muuttaa koko koodia
- Helppo palata takaisin

### 4. Ylläpidettävyys
- Selkeä rakenne
- Helppo löytää koodia
- Helppo lisätä uusia toimittajia

## 🔧 Toteutussuunnitelma

### 1. Ydinlogiikan erottaminen
**Lähde**: `run.py`, `app.py` suodata_tiedot-funktio
**Kohde**: `backend/core/`

**Funktiot**:
- `document_processor.py`: PDF → teksti
- `ai_analyzer.py`: AI-kutsut (Gemini/Groq)
- `data_extractor.py`: Tietojen poiminta
- `supplier_detector.py`: Toimittajan tunnistus

### 2. Palveluiden luominen
**Lähde**: `run_sievitalo()`, `run_kastelli()`
**Kohde**: `backend/services/`

**Palvelut**:
- `sievitalo_service.py`: Sievitalo-spesifinen logiikka
- `kastelli_service.py`: Kastelli-spesifinen logiikka
- `designtalo_service.py`: Designtalo-spesifinen logiikka

### 3. Terminaalikäyttöliittymä
**Kohde**: `backend/terminal/`

**Ominaisuudet**:
- Komentoriviparametrit
- Selkeät tulosteet
- Virheenkäsittely
- Edistymisen näyttö

### 4. Tietokantayhteyden säilyttäminen
**Lähde**: `SQL_kyselyt.py`, `db_luokat.py`
**Kohde**: `backend/models/`

**Säilytetään**:
- Kaikki tietokantaoperaatiot
- Mallit
- Yhteydet

## 📝 Käyttöohjeet

### Terminaalikäyttö (Vaihe 1)
```bash
# Analysoi kaksi toimitussisältöä
python main.py --analyze sievitalo.pdf kastelli.pdf

# Vertaile kahta analyysiä
python main.py --compare 123 456

# Näytä kaikki analyysit
python main.py --list

# Näytä tietty analyysi
python main.py --show 123
```

### Web-käyttö (Vaihe 2)
```bash
# Käynnistä web-palvelin
python main.py --mode web

# Käynnistä API-palvelin
python main.py --mode api
```

## 🎯 Seuraavat askeleet

1. **Luo modulaarinen rakenne** - Siirrä koodi uusiin kansioihin
2. **Toteuta terminaalikäyttöliittymä** - CLI-rajapinta
3. **Testaa kaikki toiminnallisuudet** - Varmista että kaikki toimii
4. **Dokumentoi käyttö** - Käyttöohjeet
5. **Valmistele web-siirtymä** - API-rajapinta

## 📚 Viittaukset

- **Nykyinen koodi**: `app.py`, `run.py`, `SQL_kyselyt.py`
- **Konfiguraatio**: `config_data.py`, `generation_config.py`
- **Apufunktiot**: `utils/`-kansio
- **Tietokanta**: `db_luokat.py`, `models/`-kansio

---

**Päivitetty**: 2024-12-19  
**Tila**: Suunnittelu valmis, toteutus aloitettu  
**Seuraava**: Modulaarisen rakenteen luominen
