# Talobot - Tekninen arkkitehtuuri ja toteutus

## Yleiskuvaus

Talobot on Flask-pohjainen web-sovellus, joka käyttää Google Generative AI:ta (Gemini) rakennusmateriaalien automaattiseen tunnistamiseen ja analysointiin PDF-tiedostoista. Sovellus noudattaa MVC-arkkitehtuuria ja käyttää PostgreSQL-tietokantaa datan tallentamiseen.

## Tekninen stack

### Backend
- **Framework**: Flask 2.x
- **Kieli**: Python 3.13
- **WSGI Server**: Gunicorn (tuotantokäyttöön)
- **Tietokanta**: PostgreSQL + SQLAlchemy ORM
- **AI/ML**: Google Generative AI (Gemini 1.5 Flash)
- **PDF-käsittely**: PyMuPDF (fitz), Docling
- **Logging**: Python logging + custom logger_config

### Frontend
- **Template Engine**: Jinja2 (Flask)
- **Styling**: Vanilla CSS + Font Awesome
- **JavaScript**: Vanilla JS (AJAX, FormData)
- **Responsive**: CSS Grid/Flexbox

### DevOps & Deployment
- **Environment**: Heroku (Procfile)
- **Environment Variables**: python-dotenv
- **Database Migrations**: Alembic
- **File Storage**: Local filesystem (persistent_data/)

## Arkkitehtuurin komponentit

### 1. Web Layer (Flask Routes)

```python
# app.py - Pääsovellus
@app.route("/suodata_tiedot", methods=["GET", "POST"])
def suodata_tiedot():
    # PDF-tiedostojen vastaanotto ja käsittely
    # Toimittajan tunnistus
    # AI-analyysin käynnistys
    # JSON-vastauksen palautus
```

**Reitit:**
- `/` - Pääsivu (index.html)
- `/suodata_tiedot` - PDF-analyysi (POST)
- `/sql_hallinta` - Tietokantahallinta
- `/hae_toimitussisallot` - Päivittäiset raportit

### 2. Business Logic Layer

#### A) PDF Processing Pipeline
```python
# utils/tietosissallon_kasittely.py
def muuta_pdf_ja_puhdista_teksti_docling(pdf_file):
    # Docling-kirjaston käyttö PDF→Markdown muunnokseen
    converter = DocumentConverter()
    result = converter.convert(source)
    return result.document.export_to_markdown()
```

#### B) AI Integration Layer
```python
# api_kyselyt.py
def api_kysely(generation_config, system_instruction, input_text):
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=lue_txt_tiedosto(system_instruction)
    )
    return model.generate_content(kysymys)
```

**AI-konfiguraatio:**
```python
# generation_config.py
GENERATION_CONFIG = {
    "temperature": 0.05,      # Matala luovuus
    "top_p": 0.80,
    "top_k": 20,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain"
}
```

#### C) Processing Orchestration
```python
# run.py
def run_sievitalo(toimitussisalto_pdf, toimitussisalto_id):
    # 1. PDF → Text conversion
    puhdistettu_toimitussisalto = muuta_pdf_ja_puhdista_teksti_docling(pdf_file)
    
    # 2. AI-based extraction
    ikkunatiedot = api_kysely(GENERATION_CONFIG, PROMPT_IKKUNATIEDOT, text)
    ikkunat_json = api_kysely(GENERATION_CONFIG_JSON, PROMPT_JSON_MUOTOON, ikkunatiedot)
    
    # 3. Database persistence
    lisaa_ikkunat_kantaan_ja_koko_x_100(ikkunat_json, toimitussisalto_id)
```

### 3. Data Access Layer

#### A) Database Models (SQLAlchemy ORM)
```python
# db_luokat.py
class Toimitussisalto(Base):
    __tablename__ = "toimitussisallot"
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False)
    pdf_url = Column(Text, nullable=False)
    txt_url = Column(Text, nullable=False)
    toimittaja = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ikkunat = relationship("Ikkuna", back_populates="toimitussisalto", cascade="all, delete-orphan")

class Ikkuna(Base):
    __tablename__ = "ikkunat"
    id = Column(Integer, primary_key=True)
    leveys = Column(Integer)
    korkeus = Column(Integer)
    turvalasi = Column(Boolean)
    valikarmi = Column(Boolean)
    salekaihtimet = Column(Boolean)
    toimitussisalto_id = Column(Integer, ForeignKey("toimitussisallot.id", ondelete="CASCADE"))
```

#### B) Database Operations
```python
# SQL_kyselyt.py
def vastaanota_toimitussisalto(file) -> str:
    unique_id = str(uuid.uuid4())
    # PDF storage
    pdf_filepath = anna_polku(unique_id)
    # Text conversion
    teksti = muuta_pdf_tekstiksi(io.BytesIO(file_data))
    # Supplier identification
    toimittaja = tunnista_toimittaja(teksti)
    # Database persistence
    tallenna_toimitussisalto_tietokantaan(toimittaja, pdf_filepath, txt_filepath, unique_id)
```

### 4. Configuration Management

#### A) Environment Configuration
```python
# db_luokat.py
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_robust_engine(DATABASE_URL)  # Connection pooling
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

#### B) AI Configuration
```python
# generation_config.py
GENERATION_CONFIG = {
    "temperature": 0.05,      # Deterministic responses
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain"
}

GENERATION_CONFIG_JSON = {
    "response_mime_type": "application/json"  # Structured output
}
```

## Data Flow Architecture

### 1. Request Processing Flow
```
HTTP Request → Flask Route → File Upload → UUID Generation → 
PDF Storage → Text Extraction → Supplier Detection → 
AI Processing → Database Storage → JSON Response
```

### 2. AI Processing Pipeline
```
Raw PDF → Docling Converter → Cleaned Text → 
Prompt Engineering → Gemini API → JSON Response → 
Data Validation → Database Persistence
```

### 3. Multi-Supplier Support
```python
# Factory pattern for supplier-specific processing
if toimittaja == "Sievitalo":
    run_sievitalo(pdf_url, toimitussisalto_id)
elif toimittaja == "Kastelli":
    run_kastelli(pdf_url, toimitussisalto_id)
elif toimittaja == "Designtalo":
    run_designtalo(pdf_url, toimitussisalto_id)
```

## Database Schema

### Core Tables
```sql
-- Toimitussisallot (main entity)
CREATE TABLE toimitussisallot (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(36) NOT NULL UNIQUE,
    pdf_url TEXT NOT NULL,
    txt_url TEXT NOT NULL,
    toimittaja VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Ikkunat (extracted data)
CREATE TABLE ikkunat (
    id SERIAL PRIMARY KEY,
    leveys INTEGER,
    korkeus INTEGER,
    turvalasi BOOLEAN,
    valikarmi BOOLEAN,
    salekaihtimet BOOLEAN,
    toimitussisalto_id INTEGER REFERENCES toimitussisallot(id) ON DELETE CASCADE
);

-- Vertailut (comparison tracking)
CREATE TABLE vertailut (
    id SERIAL PRIMARY KEY,
    toimitussisalto_1_id INTEGER REFERENCES toimitussisallot(id),
    toimitussisalto_2_id INTEGER REFERENCES toimitussisallot(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## AI Integration Details

### 1. Prompt Engineering Strategy
- **System Instructions**: Toimittajakohtaiset prompt-tiedostot
- **Context Injection**: Tuotelistaus + toimitussisältö
- **Output Formatting**: JSON-skeemat tarkkoja vastauksia varten

### 2. Model Configuration
```python
# Low temperature for consistent extraction
generation_config = {
    "temperature": 0.05,      # Deterministic
    "top_p": 0.80,           # Focused sampling
    "max_output_tokens": 8192 # Sufficient for complex documents
}
```

### 3. Error Handling
```python
try:
    response = model.generate_content(kysymys)
    if response is not None:
        return response.text
    else:
        logger.warning("API-vastaus puuttuu")
except Exception as e:
    logger.error(f"Odottamaton virhe: {e}")
    return ""
```

## File Management

### 1. Storage Strategy
```
persistent_data/
├── data/
│   └── ladatut_toimitussisallot/
│       ├── {uuid}.pdf          # Original PDF
│       └── {uuid}.txt          # Extracted text
└── uploads/                    # Temporary uploads
```

### 2. File Processing
```python
def anna_polku(unique_id: str):
    return UPLOAD_FOLDER_DATA / f"{unique_id}.pdf"

def muuta_pdf_tekstiksi(pdf_file):
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        return "".join(page.get_text() for page in doc)
```

## Security Considerations

### 1. File Upload Security
- **File Type Validation**: PDF-only uploads
- **Secure Filenames**: UUID-based naming
- **Path Traversal Protection**: werkzeug.utils.secure_filename

### 2. API Security
- **Environment Variables**: API keys in .env
- **Input Sanitization**: Text cleaning before AI processing
- **Error Handling**: No sensitive data in error messages

### 3. Database Security
- **Connection Pooling**: Robust connection management
- **SQL Injection Prevention**: SQLAlchemy ORM
- **Cascade Deletes**: Proper foreign key constraints

## Performance Optimizations

### 1. Database Optimizations
```python
# Connection pooling with keepalive
engine = create_engine(
    url,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }
)
```

### 2. AI Processing
- **Batch Processing**: Multiple extractions per request
- **Caching**: Processed text storage
- **Async Potential**: Future enhancement for concurrent processing

### 3. Frontend Optimizations
- **AJAX Requests**: Non-blocking UI updates
- **Progressive Loading**: Step-by-step feedback
- **Client-side Validation**: Immediate feedback

## Deployment Architecture

### 1. Heroku Configuration
```procfile
web: gunicorn app:app
```

### 2. Environment Variables
```bash
DATABASE_URL=postgresql://...
GEMINI_API_KEY=...
PORT=8080
```

### 3. Dependencies
```txt
Flask
gunicorn
google-generativeai
pymupdf
sqlalchemy
psycopg2
docling
python-dotenv
```

## Monitoring & Logging

### 1. Logging Strategy
```python
# logger_config.py
configure_logging()
logger = logging.getLogger(__name__)

# Structured logging
logger.info("✅ Tietokantayhteys toimii")
logger.error(f"❌ Virhe: {str(e)}")
```

### 2. Error Tracking
- **Database Connection Monitoring**: Startup checks
- **API Response Validation**: Null checks
- **File Processing Errors**: Try-catch blocks

## Scalability Considerations

### 1. Current Limitations
- **Single-threaded Processing**: Sequential AI calls
- **Local File Storage**: Not cloud-native
- **Memory Usage**: Large PDF processing

### 2. Future Enhancements
- **Microservices**: Separate AI processing service
- **Queue System**: Celery/RQ for background processing
- **Cloud Storage**: AWS S3/Google Cloud Storage
- **Caching Layer**: Redis for processed data
- **Load Balancing**: Multiple app instances

## Development Workflow

### 1. Code Organization
```
talobot_env/
├── app.py                 # Main Flask application
├── run.py                 # Processing orchestration
├── api_kyselyt.py         # AI integration
├── db_luokat.py           # Database models
├── SQL_kyselyt.py         # Database operations
├── utils/                 # Utility functions
├── templates/             # HTML templates
├── static/                # CSS/JS assets
└── data/                  # Configuration files
```

### 2. Testing Strategy
- **Unit Tests**: Individual function testing
- **Integration Tests**: Database + AI pipeline
- **End-to-End Tests**: Full user workflow

### 3. Version Control
- **Git Workflow**: Feature branches
- **Environment Management**: .env files
- **Dependency Management**: requirements.txt

## Conclusion

Talobot noudattaa moderneja web-sovellusarkkitehtuurin periaatteita käyttäen Flask-frameworkia, SQLAlchemy ORM:ää ja Google Generative AI:ta. Sovellus on suunniteltu skaalautuvaksi ja ylläpidettäväksi, vaikka se tällä hetkellä toimii yksinkertaisessa monoliittisessa arkkitehtuurissa. Tulevaisuudessa sovellusta voidaan helposti laajentaa mikroservisiksi tai pilvipohjaiseksi ratkaisuksi.
