# Docker Setup - Talobot

## Asennusohje

### 1. Docker Desktop asennus
1. Lataa Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Asenna ja käynnistä Docker Desktop
3. Varmista että Docker toimii: `docker --version`

### 2. Environment-konfiguraatio
```bash
# Kopioi example-tiedosto
cp env.example .env

# Muokkaa .env-tiedostoa
nano .env
```

**Tärkeät muutokset .env-tiedostoon:**
```bash
# Lisää oma Gemini API-avain
GEMINI_API_KEY=your_actual_api_key_here

# Muuta salasana tuotantokäyttöön
POSTGRES_PASSWORD=strong_password_here
```

### 3. Käynnistys
```bash
# Käynnistä kaikki palvelut
docker-compose up

# Taustalla (detached mode)
docker-compose up -d

# Näytä logit
docker-compose logs -f

# Sammuta
docker-compose down
```

### 4. Tietokanta-migraatiot
```bash
# Suorita migraatiot
docker-compose exec web alembic upgrade head

# Luo uusi migraatio
docker-compose exec web alembic revision --autogenerate -m "Description"
```

## Kehitystyökalut

### Hyödylliset komennot
```bash
# Pääsy sovelluksen kontaineriin
docker-compose exec web bash

# Pääsy tietokantaan
docker-compose exec db psql -U talobot_user -d talobot

# Käynnistä vain tietokanta
docker-compose up db

# Puhdista kaikki
docker-compose down -v
docker system prune -a
```

### Debugging
```bash
# Näytä kontainerien tila
docker-compose ps

# Näytä resurssien käyttö
docker stats

# Tarkista logit
docker-compose logs web
docker-compose logs db
```

## Tiedostojen hallinta

### Volume-mapping
- `./persistent_data` → `/app/persistent_data` (PDF-tiedostot)
- `./data` → `/app/data` (konfiguraatiot)
- `postgres_data` → PostgreSQL data (automaattinen)

### Tiedostojen kopiointi
```bash
# Kopioi tiedosto kontainerista
docker cp container_name:/app/file.txt ./local_file.txt

# Kopioi tiedosto kontaineriin
docker cp ./local_file.txt container_name:/app/file.txt
```

## Suorituskyky-optimointi

### Docker Desktop asetukset
1. **Resources** → **Advanced**
   - CPU: 4+ cores
   - Memory: 8+ GB
   - Disk: 100+ GB

### Kehitysympäristö optimointi
```bash
# Käynnistä vain tarvittavat palvelut
docker-compose up db web

# Käytä development-moodia
FLASK_ENV=development docker-compose up
```

## Ongelmien ratkaisu

### Yleisimmät ongelmat

#### 1. Portti varattu
```bash
# Tarkista mikä käyttää porttia
netstat -tulpn | grep :8080

# Muuta portti docker-compose.yml:ssä
ports:
  - "8081:8080"  # Käytä porttia 8081
```

#### 2. Tietokantayhteys ei toimi
```bash
# Tarkista tietokanta
docker-compose exec db pg_isready -U talobot_user

# Käynnistä uudelleen
docker-compose restart db
```

#### 3. Tiedostojen oikeudet
```bash
# Korjaa oikeudet
sudo chown -R $USER:$USER persistent_data/
chmod -R 755 persistent_data/
```

#### 4. Docling-kirjasto ongelmat
```bash
# Päivitä requirements.txt
echo "docling[pdf]" >> requirements.txt

# Uudelleenrakenna
docker-compose build --no-cache web
```

## Tuotantokäyttö

### Tuotantokonfiguraatio
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  web:
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=0
    command: gunicorn --bind 0.0.0.0:8080 app:app
```

### Käynnistys tuotantotilassa
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Vaihtoehtoiset ratkaisut

### 1. Railway.app (Nopea deployment)
- Push GitHub → Automaattinen deployment
- PostgreSQL sisäänrakennettuna
- $5/kuukausi

### 2. Fly.io (Docker-native)
- `flyctl deploy` -komento
- Global CDN
- $0-10/kuukausi

### 3. Local development
```bash
# Asenna PostgreSQL paikallisesti
brew install postgresql  # macOS
sudo apt install postgresql  # Ubuntu

# Käynnistä Flask
python app.py
```

## Suositukset

### Kehitysvaiheessa
1. **Käytä Docker Compose** - Helppo ja nopea
2. **Volume-mapping** - Koodimuutokset näkyvät heti
3. **Development mode** - Hot reload toimii

### Tuotantokäyttöön
1. **Railway.app** - Nopein vaihtoehto
2. **Fly.io** - Parhaat Docker-työkalut
3. **DigitalOcean** - Edullisin pitkällä tähtäimellä

## Edut Docker Compose vs Render

### Docker Compose ✅
- **Nopea kehitys** - Muutokset näkyvät heti
- **Paikallinen** - Ei internet-riippuvuutta
- **Kustannus** - Ilmainen
- **Debugging** - Täysi kontrolli
- **Offline** - Toimii ilman internettiä

### Render ❌
- **Hidas** - 2-5 min deployment
- **Kustannus** - $7+/kuukausi
- **Riippuvuus** - Internet tarvitaan
- **Rajoitettu** - Ei täyttä kontrollia



