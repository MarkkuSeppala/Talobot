# Docker Desktop - Asennusopas

## Ennen asennusta - Tärkeät huomiot

### ⚠️ **Järjestelmävaatimukset**
- **Windows 10/11** (Pro, Enterprise, Education)
- **macOS 10.15+** (Catalina tai uudempi)
- **Linux** (Ubuntu 20.04+, Debian 10+, RHEL 7+)
- **RAM**: Vähintään 4GB (suositus 8GB+)
- **CPU**: 64-bit x86_64
- **Vapaa levytila**: 4GB+

### 🔧 **Järjestelmävalmistelut**

#### Windows:
- **WSL 2** (Windows Subsystem for Linux) - Pakollinen
- **Hyper-V** - Automaattisesti käynnistyy
- **Virtualization** - BIOS/UEFI:ssä käytössä

#### macOS:
- **Apple Silicon (M1/M2)** tai **Intel** -tuettu
- **Xcode Command Line Tools** - Suositeltu

#### Linux:
- **Kernel 3.10+** (Ubuntu 20.04+)
- **systemd** - Käynnistysjärjestelmä

## Asennusvaiheet

### 1. **Lataa Docker Desktop**

#### Windows:
1. Mene: https://www.docker.com/products/docker-desktop/
2. Klikkaa **"Download for Windows"**
3. Tiedosto: `Docker Desktop Installer.exe`

#### macOS:
1. Mene: https://www.docker.com/products/docker-desktop/
2. Klikkaa **"Download for Mac"**
3. Valitse oikea versio:
   - **Apple Silicon** (M1/M2) - `Docker.dmg`
   - **Intel** - `Docker.dmg`

#### Linux:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# Tai lataa .deb-paketti
wget https://desktop.docker.com/linux/main/amd64/docker-desktop-4.24.0-amd64.deb
sudo dpkg -i docker-desktop-4.24.0-amd64.deb
```

### 2. **Asenna Docker Desktop**

#### Windows:
1. **Käynnistä asennustiedosto** admin-oikeuksilla
2. **Hyväksy** käyttöehdot
3. **Valitse asetukset**:
   - ✅ **Use WSL 2 instead of Hyper-V** (suositus)
   - ✅ **Add shortcut to desktop**
   - ✅ **Use Windows containers** (valinnainen)
4. **Klikkaa "Install"**
5. **Käynnistä uudelleen** tarvittaessa

#### macOS:
1. **Vedä Docker.app** Applications-kansioon
2. **Käynnistä Docker Desktop** Applications-kansiosta
3. **Hyväksy** käyttöehdot
4. **Kirjaudu sisään** Docker Hubiin (valinnainen)

### 3. **Ensimmäinen käynnistys**

#### Windows:
1. **Käynnistä Docker Desktop** työpöydältä
2. **Hyväksy** WSL 2 -käyttöehdot
3. **Odota** Docker Engine käynnistymistä
4. **Näet** Docker-kuvan system tray:ssä

#### macOS:
1. **Käynnistä Docker Desktop** Applications-kansiosta
2. **Hyväksy** käyttöehdot
3. **Odota** Docker Engine käynnistymistä
4. **Näet** Docker-kuvan menu bar:ssa

### 4. **Tarkista asennus**

```bash
# Avaa komentorivi/terminaali
docker --version
# Tuloste: Docker version 24.0.7, build afdd53b

docker-compose --version
# Tuloste: Docker Compose version v2.21.0

# Testaa Docker
docker run hello-world
# Tuloste: Hello from Docker!
```

## Tärkeät asetukset

### 1. **Resources (Resurssit)**

#### Windows (WSL 2):
1. **Klikkaa** Docker-kuvaa system tray:ssä
2. **Settings** → **Resources** → **Advanced**
3. **WSL 2 -resurssit** konfiguroidaan `.wslconfig` -tiedostossa:

```ini
# Luo tiedosto: C:\Users\YourName\.wslconfig
[wsl2]
memory=8192        # 8GB RAM
processors=4       # 4 CPU-ydintä
swap=2048          # 2GB swap
diskSize=100       # 100GB levytila
```

4. **Käynnistä WSL uudelleen**:
```bash
wsl --shutdown
wsl --start
```

#### macOS:
1. **Klikkaa** Docker-kuvaa menu bar:ssa
2. **Settings** → **Resources**
3. **Advanced**:
   - **CPUs**: 4+ (suositus)
   - **Memory**: 8GB+ (suositus)
   - **Disk**: 100GB+ (suositus)

### 2. **WSL 2 (Windows)**

#### Tarkista WSL 2:
```bash
# PowerShell admin-oikeuksilla
wsl --list --verbose
# Tuloste: Ubuntu-20.04    Running         2
```

#### Jos WSL 2 puuttuu:
```bash
# PowerShell admin-oikeuksilla
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
wsl --set-default-version 2
```

### 3. **File Sharing (Tiedostojen jakaminen)**

#### Windows:
1. **Settings** → **Resources** → **File Sharing**
2. **Lisää** projektikansiosi (esim. `C:\Users\YourName\Projects`)

#### macOS:
1. **Settings** → **Resources** → **File Sharing**
2. **Lisää** projektikansiosi (esim. `/Users/YourName/Projects`)

## Yleisimmät ongelmat ja ratkaisut

### 1. **"Docker Desktop won't start"**

#### Windows:
```bash
# Tarkista WSL 2
wsl --status

# Käynnistä WSL 2 uudelleen
wsl --shutdown
wsl --start
```

#### macOS:
```bash
# Tarkista virtualization
sysctl kern.hv_support
# Tuloste: kern.hv_support: 1
```

### 2. **"Port already in use"**

```bash
# Tarkista mikä käyttää porttia
netstat -tulpn | grep :8080  # Linux
netstat -an | grep :8080     # Windows/macOS

# Muuta portti docker-compose.yml:ssä
ports:
  - "8081:8080"  # Käytä porttia 8081
```

### 3. **"Permission denied"**

#### Linux:
```bash
# Lisää käyttäjä docker-ryhmään
sudo usermod -aG docker $USER
# Kirjaudu ulos ja takaisin
```

#### Windows:
- **Käynnistä** Docker Desktop admin-oikeuksilla
- **Tarkista** Windows Defender -asetukset

### 4. **"Out of disk space"**

```bash
# Puhdista Docker
docker system prune -a
docker volume prune

# Tarkista levytila
docker system df
```

## Talobot-projektin testaus

### 1. **Kopioi environment**
```bash
# Projektikansiossa
cp env.example .env

# Muokkaa .env-tiedostoa
nano .env  # tai notepad .env
```

### 2. **Lisää API-avain**
```bash
# .env-tiedostoon
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. **Testaa Docker Compose**
```bash
# Käynnistä
docker-compose up

# Taustalla
docker-compose up -d

# Tarkista logit
docker-compose logs -f

# Sammuta
docker-compose down
```

## Suorituskyky-optimointi

### 1. **Docker Desktop asetukset**
- **CPU**: 4+ cores
- **Memory**: 8GB+ (16GB suositus)
- **Disk**: 100GB+ (SSD suositus)

### 2. **Kehitysympäristö**
```bash
# Käynnistä vain tarvittavat palvelut
docker-compose up db web

# Development mode
FLASK_ENV=development docker-compose up
```

### 3. **Volume-mapping optimointi**
```yaml
# docker-compose.yml
volumes:
  - .:/app                    # Koodi
  - ./persistent_data:/app/persistent_data  # Tiedostot
  - /app/venv                 # Ei synkronoi venv-kansiota
```

## Vaihtoehtoiset asennusmenetelmät

### 1. **Chocolatey (Windows)**
```bash
# Asenna Chocolatey ensin
# Sitten:
choco install docker-desktop
```

### 2. **Homebrew (macOS)**
```bash
# Asenna Homebrew ensin
# Sitten:
brew install --cask docker
```

### 3. **Snap (Linux)**
```bash
sudo snap install docker
```

## Seuraavat vaiheet

### 1. **Tarkista asennus**
```bash
docker --version
docker-compose --version
docker run hello-world
```

### 2. **Testaa Talobot**
```bash
# Projektikansiossa
docker-compose up
```

### 3. **Avaa selain**
- Mene: http://localhost:8080
- Näet Talobot-sovelluksen

## Ongelmatilanteet

### Jos Docker Desktop ei käynnisty:
1. **Käynnistä uudelleen** tietokone
2. **Tarkista** antivirus-ohjelma
3. **Päivitä** Docker Desktop
4. **Asenna uudelleen** tarvittaessa

### Jos kontainerit eivät käynnisty:
1. **Tarkista** .env-tiedosto
2. **Tarkista** porttien vapaus
3. **Tarkista** levytila
4. **Käynnistä** Docker Desktop uudelleen

## Yhteenveto

### ✅ **Onnistunut asennus:**
- Docker Desktop käynnistyy
- `docker --version` toimii
- `docker run hello-world` toimii
- Talobot käynnistyy `docker-compose up`:lla

### 🚀 **Seuraavat vaiheet:**
1. **Konfiguroi** .env-tiedosto
2. **Testaa** Talobot-sovellus
3. **Aloita** kehitystyö

### 📞 **Tarvitsetko apua?**
- **Docker Desktop** → Help → Documentation
- **Talobot** → DOCKER_SETUP.md
- **Ongelmat** → DOCKER_SETUP.md → Ongelmien ratkaisu

