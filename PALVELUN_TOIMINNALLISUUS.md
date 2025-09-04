# Talobot - Omakotitalorakentajan apuri

## Mikä on Talobot?

Talobot on verkkopalvelu, joka auttaa omakotitalorakentajia analysoimaan ja vertailemaan eri rakennusyritysten toimitussisältöjä. Palvelu käyttää tekoälyä (AI) tunnistamaan ja järjestämään rakennusmateriaalien tiedot automaattisesti.

## Miten palvelu toimii?

### 1. Tiedostojen lataus
- **Syöte**: Kaksi PDF-tiedostoa (toimitussisältöjä)
  - Ensimmäinen toimitussisältö (esim. Sievitalo)
  - Toinen toimitussisältö (esim. Kastelli)
- **Tiedostomuoto**: PDF-tiedostot
- **Koko**: Ei erityisiä rajoituksia

### 2. Automaattinen käsittely
Palvelu suorittaa seuraavat vaiheet automaattisesti:

#### A) Tiedostojen tallennus
- Luo yksilöllisen tunnisteen (UUID) jokaiselle tiedostolle
- Tallentaa PDF-tiedostot palvelimelle
- Muuntaa PDF-tiedostot tekstiksi

#### B) Toimittajan tunnistus
- Lukee toimitussisällön tekstin
- Tunnistaa automaattisesti toimittajan (Sievitalo, Kastelli, Designtalo)
- Tallentaa tiedot tietokantaan

#### C) Tietojen puhdistus ja analyysi
- Puhdistaa tekstin turhista merkeistä ja muotoilusta
- Käyttää tekoälyä (Google Generative AI) analysoimaan sisältöä
- Etsii ja tunnistaa:
  - **Ikkunat** (koko, määrä, turvalasi, välikarmi, sälekaihtimet)
  - **Ulko-ovet** (tyyppi, koko, materiaali)
  - **Väliovet** (ovimallit ja tyypit)

#### D) Tietojen tallennus
- Tallentaa löydetyt tiedot tietokantaan
- Järjestää tiedot selkeään muotoon
- Luo vertailun kahden toimitussisällön välille

### 3. Tulosten näyttäminen
Palvelu näyttää analyysin tulokset selkeässä taulukkomuodossa:

#### Ikkunat
- Koko (esim. 1200x1500 mm)
- Määrä
- Turvalasi (kyllä/ei)
- Välikarmi (kyllä/ei)
- Sälekaihtimet (kyllä/ei)

#### Ulko-ovet
- Ovimalli/tyyppi
- Koko
- Materiaali
- Muut ominaisuudet

#### Väliovet
- Lista ovimalleista
- Ovityypit

## Käyttöliittymä

### Pääsivu
- **Otsikko**: "Tervetuloa Talobotiin"
- **Kuvaus**: "Analysoi talon toimitussisältö automaattisesti ja saa selkeä yhteenveto rakennusprojektisi materiaaleista"

### Latausosio
- Kaksi tiedostonvalinta-kenttää
- PDF-tiedostojen tarkistus
- "Analysoi toimitussisällöt" -painike (aktivoituu kun molemmat tiedostot on valittu)

### Tulosten näyttö
- Kaksi saraketta (Sievitalo ja Kastelli)
- Jokaisessa sarakkeessa:
  - Ikkunat-taulukko
  - Ulko-ovet-taulukko
  - Väliovimallit-lista
- "Analysoi uudet toimitussisällöt" -painike

### SQL Hallinta -sivu
- Päivämäärän valinta
- Mahdollisuus hakea:
  - Toimitussisällöt tietyltä päivältä
  - Ulko-ovet tietyltä päivältä
  - Väliovet tietyltä päivältä

## Tekninen toteutus

### Käytetyt teknologiat
- **Backend**: Python Flask
- **Tietokanta**: SQLAlchemy (PostgreSQL)
- **Tekoäly**: Google Generative AI
- **PDF-käsittely**: PyMuPDF, Docling
- **Frontend**: HTML, CSS, JavaScript

### Tietokantarakenteet
- **Toimitussisältö**: Toimittaja, PDF-polku, teksti-polku, UUID
- **Ikkunat**: Koko, määrä, ominaisuudet
- **Ulko-ovet**: Tyyppi, koko, materiaali
- **Väliovet**: Ovimallit
- **Vertailut**: Linkki kahden toimitussisällön välille

## Käyttöohje

### 1. Valmistelu
- Hanki kaksi toimitussisältöä PDF-muodossa
- Varmista, että tiedostot ovat luettavissa

### 2. Analyysin suorittaminen
1. Avaa Talobot-sivusto
2. Lataa ensimmäinen toimitussisältö (PDF)
3. Lataa toinen toimitussisältö (PDF)
4. Klikkaa "Analysoi toimitussisällöt"
5. Odota analyysin valmistumista (latausanimaatio)

### 3. Tulosten tarkastelu
- Tarkastele ikkunatietoja molemmista toimittajista
- Vertaile ulko-ovien eroja
- Tutki väliovimalleja
- Käytä tuloksia päätöksenteossa

### 4. Uusien analyysien tekeminen
- Klikkaa "Analysoi uudet toimitussisällöt"
- Lataa uudet tiedostot
- Toista prosessi

## Edut käyttäjälle

### Aikansäästö
- Automaattinen tiedon poiminta PDF:stä
- Ei tarvetta käydä läpi satoja sivuja manuaalisesti
- Nopea vertailu kahden tarjouksen välillä

### Tarkkuus
- Tekoäly tunnistaa tiedot luotettavasti
- Järjestelmällinen tiedon esittäminen
- Vähentää ihmisvirheitä

### Selkeys
- Taulukkomuotoinen esitys
- Helppo vertailla eri toimittajia
- Keskitetty näkymä kaikista materiaaleista

## Rajoitukset

### Tiedostomuoto
- Vain PDF-tiedostot tuetaan
- Tiedostojen on oltava luettavissa

### Toimittajat
- Tällä hetkellä tuetaan: Sievitalo, Kastelli, Designtalo
- Uusia toimittajia voidaan lisätä tarvittaessa

### Kieli
- Palvelu on suunniteltu suomenkielisille toimitussisällöille
- Muut kielet voivat aiheuttaa tunnistusongelmia

## Tulevaisuuden kehitysmahdollisuudet

- Lisää toimittajia
- Hintavertailut
- Kustannuslaskelmat
- Mobiilisovellus
- Sähköpostiraportit
- Integraatio rakennusohjelmistoihin

## Yhteenveto

Talobot on tehokas työkalu omakotitalorakentajille, joka automatisoi toimitussisältöjen analyysin ja vertailun. Palvelu säästää aikaa, parantaa tarkkuutta ja helpottaa päätöksentekoa rakennusprojektissa. Yksinkertainen käyttöliittymä tekee palvelusta helppokäyttöisen myös teknologiaa vähemmän tunteville käyttäjille.



