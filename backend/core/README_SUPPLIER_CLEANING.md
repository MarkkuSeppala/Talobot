# Toimittajakohtainen puhdistusjärjestelmä

Tämä järjestelmä mahdollistaa toimittajakohtaisen dokumenttien puhdistuksen ennen AI-analyysiä.

## Arkkitehtuuri

### 1. DocumentCleaner (Abstrakti luokka)
- Määrittelee toimittajakohtaisen puhdistuksen rajapinnan
- Sisältää yhteiset metodit kuten `_add_markers()`

### 2. Toimittajakohtaiset puhdistusluokat
- `SievitaloCleaner`: Sievitalo-kohtainen puhdistus
- `KastelliCleaner`: Kastelli-kohtainen puhdistus  
- `DesigntaloCleaner`: Designtalo-kohtainen puhdistus

### 3. CleanerFactory
- Luo puhdistusluokkia toimittajan mukaan
- Mahdollistaa uusien toimittajien rekisteröinnin

### 4. DocumentProcessor (Päivitetty)
- Käyttää toimittajakohtaisia puhdistajia
- Tunnistaa toimittajan automaattisesti jos ei määritelty

## Käyttö

### Peruskäyttö

```python
from backend.core.document_processor import DocumentProcessor

processor = DocumentProcessor()

# Tunnista toimittaja automaattisesti
result = processor.process_pdf("path/to/document.pdf")

# Määritä toimittaja suoraan
result = processor.process_pdf("path/to/document.pdf", supplier="Sievitalo")
```

### Suora puhdistajien käyttö

```python
from backend.core.cleaner_factory import CleanerFactory

# Luo puhdistaja
cleaner = CleanerFactory.create_cleaner("Sievitalo")

# Puhdista dokumentti
cleaned_text = cleaner.clean_document("path/to/document.pdf")
```

### Palveluiden käyttö

```python
from backend.services.sievitalo_service import SievitaloService

service = SievitaloService()
result = service.process_document("path/to/document.pdf", toimitussisalto_id=123)
```

## Konfiguraatio

Puhdistussäännöt määritellään `cleaner_config.py` tiedostossa:

```python
CLEANER_CONFIGS = {
    "Sievitalo": {
        "remove_patterns": [
            r"Sievitalo Oy.*?Y-tunnus: \d+-\d+",
            r"TOIMITUSTAPASELOSTE\s+\d+"
        ],
        "format_rules": {
            "section_headers": True,
            "bullet_points": True
        }
    }
}
```

## Uusien toimittajien lisääminen

### 1. Luo puhdistusluokka

```python
class UusiToimittajaCleaner(DocumentCleaner):
    def clean_document(self, pdf_path: str) -> str:
        # Toimittajakohtainen puhdistuslogiikka
        text = muuta_pdf_ja_puhdista_teksti_docling(pdf_path)
        text = self._remove_specific_content(text)
        text = self._format_structure(text)
        return self._add_markers(text)
    
    def get_supplier_name(self) -> str:
        return "UusiToimittaja"
```

### 2. Rekisteröi factoryyn

```python
from backend.core.cleaner_factory import CleanerFactory

CleanerFactory.register_cleaner("UusiToimittaja", UusiToimittajaCleaner)
```

### 3. Lisää konfiguraatio

```python
# cleaner_config.py
CLEANER_CONFIGS["UusiToimittaja"] = {
    "remove_patterns": [...],
    "format_rules": {...}
}
```

## Hyödyt

1. **Toimittajakohtainen optimointi**: Jokainen toimittaja saa optimoidun puhdistuksen
2. **Helppo laajentaa**: Uusi toimittaja lisätään vain uudella luokalla
3. **Ylläpidettävyys**: Puhdistuslogiikka on eroteltu toimittajittain
4. **Testattavuus**: Jokainen cleaner voidaan testata erikseen
5. **Konfiguroitavuus**: Puhdistussäännöt voidaan säilyttää konfiguraatiotiedostoissa

## Esimerkki

Katso `backend/examples/supplier_specific_cleaning_example.py` täydellisestä esimerkistä.




