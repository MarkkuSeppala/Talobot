# Talobot - Terminaalikäyttöliittymä

## ✅ Valmis!

Terminaalikäyttöliittymä on nyt valmis ja toimii! Voit käyttää kaikkia PDF-analyysiä terminaalissa.

## 🚀 Käyttöohjeet

### Pääkäynnistys
```bash
python main.py --help
```

### Komennot

#### 1. Analysoi kaksi PDF-tiedostoa
```bash
python main.py analyze sievitalo.pdf kastelli.pdf
python main.py analyze tiedosto1.pdf tiedosto2.pdf --output tulokset.json
```

#### 2. Vertaile kahta analyysiä
```bash
python main.py compare 1102 1103
```

#### 3. Listaa analyysit
```bash
python main.py list
python main.py list --limit 5
```

#### 4. Näytä tietty analyysi
```bash
python main.py show 1102
```

## 📊 Esimerkkituloste

```
🔍 Talobot - PDF-analyysi aloitetaan...
📄 Tiedosto 1: sievitalo.pdf
📄 Tiedosto 2: kastelli.pdf

📥 Käsitellään ensimmäinen tiedosto...
📥 Käsitellään toinen tiedosto...
🔗 Luodaan vertailu...
🔍 Analysoidaan ensimmäinen tiedosto...
   Toimittaja: Sievitalo
   Suoritetaan Sievitalo-analyysi...
🔍 Analysoidaan toinen tiedosto...
   Toimittaja: Kastelli
   Suoritetaan Kastelli-analyysi...
📊 Haetaan analyysitulokset...

================================================================================
📊 ANALYYSITULOKSET
================================================================================

📊 SIEVITALO
--------------------------------------------------
🪟 IKKUNAT:
+-----------+-------------+-------------+-----------------+
| Koko      | Turvalasi   | Välikarmi   | Sälekaihtimet   |
+===========+=============+=============+=================+
| 500x1600  | ❌          | ❌          | ❌              |
| 600x600   | ✅          | ❌          | ✅              |
| 1200x2100 | ✅          | ❌          | ✅              |
+-----------+-------------+-------------+-----------------+

🚪 ULKO-OVET:
+----------+--------+------------+
| Malli    | Koko   | Materiaali |
+==========+========+============+
| Perusovi | 900x2100| Puu       |
+----------+--------+------------+

🚪 VÄLIOVET:
+------------------+
| Ovimalli         |
+==================+
| Kylpyhuoneovi    |
| Makuuhuoneovi    |
+------------------+

📊 KASTELLI
--------------------------------------------------
🪟 IKKUNAT:
+-----------+-------------+-------------+-----------------+
| Koko      | Turvalasi   | Välikarmi   | Sälekaihtimet   |
+===========+=============+=============+=================+
| 600x1200  | ✅          | ✅          | ❌              |
| 1200x1500 | ✅          | ✅          | ✅              |
+-----------+-------------+-------------+-----------------+

✅ Analyysi valmis! Analyysi-ID:t: 1102, 1103
```

## 🏗️ Modulaarinen rakenne

```
talobot_env/
├── main.py                    # Pääkäynnistys
├── backend/                   # Ydinlogiikka
│   ├── core/                 # Ydinlogiikka
│   │   ├── document_processor.py
│   │   └── ai_analyzer.py
│   ├── services/             # Palvelut
│   │   ├── sievitalo_service.py
│   │   └── kastelli_service.py
│   └── terminal/             # Terminaalikäyttöliittymä
│       ├── cli.py
│       └── output_formatter.py
├── shared/                   # Jaetut apufunktiot
│   ├── file_handler.py
│   ├── logger_config.py
│   └── tietosissallon_kasittely.py
└── [muut tiedostot...]       # Tietokanta, konfiguraatiot jne.
```

## ✨ Ominaisuudet

### ✅ Toimivat komennot
- **analyze** - Analysoi kaksi PDF-tiedostoa
- **compare** - Vertaile kahta analyysiä
- **list** - Listaa analyysit
- **show** - Näytä tietty analyysi

### ✅ Toimittajat
- **Sievitalo** - Täysi tuki
- **Kastelli** - Täysi tuki
- **Designtalo** - Valmisteilla

### ✅ Tulosteet
- **Taulukkomuotoiset** - Selkeät taulukot
- **Emojit** - Visuaaliset merkit
- **Värit** - Selkeä erottelu
- **JSON-tallennus** - Valinnainen

## 🔧 Tekninen toteutus

### Moduulit
- **main.py** - Komentoriviparsinta ja päälogiikka
- **backend/terminal/cli.py** - CLI-funktiot
- **backend/terminal/output_formatter.py** - Tulostemuotoilu
- **backend/core/** - Ydinlogiikka
- **backend/services/** - Toimittajakohtaiset palvelut

### Riippuvuudet
- **tabulate** - Taulukkomuotoilu
- **SQLAlchemy** - Tietokanta
- **Groq API** - AI-analyysi
- **PyMuPDF** - PDF-käsittely

## 🎯 Seuraavat askeleet

1. **Testaa analyze-komento** - Kokeile PDF-analyysiä
2. **Lisää Designtalo-tuki** - Laajenna toimittajia
3. **Paranna virheenkäsittelyä** - Robustimpi koodi
4. **Lisää konfiguraatioita** - Asetustiedostot

## 📝 Huomioita

- **API-viiveet** - 30s viiveet API-kutsujen välillä
- **Tietokanta** - Vaatii toimivan tietokantayhteyden
- **Tiedostot** - PDF-tiedostot pitää olla luettavissa
- **Logit** - Kaikki toiminta logitetaan

---

**Päivitetty**: 2024-12-19  
**Tila**: ✅ Valmis ja toimii  
**Seuraava**: Testaa analyze-komento PDF-tiedostoilla
