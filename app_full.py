from flask import Flask, request, render_template, Response, redirect, url_for, jsonify
import os
import sys
import uuid
from werkzeug.utils import secure_filename
import io
import logging
from datetime import datetime 
import json

# Tietokantayhteyden importit
try:
    from db_luokat import SessionLocal, Toimitussisalto
    from sqlalchemy import text
    DB_AVAILABLE = True
    logging.info("✅ Tietokantamoduulit ladattu onnistuneesti")
except ImportError as e:
    DB_AVAILABLE = False
    logging.warning(f"❌ Tietokantamoduulit eivät ole saatavilla: {e}")

# Yksinkertainen logging konfiguraatio
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Tietokantayhteyden testaus
def test_database_connection():
    """Testaa tietokantayhteyttä turvallisesti"""
    if not DB_AVAILABLE:
        return False, "Tietokantamoduulit eivät ole saatavilla"
    
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
            return True, "Tietokantayhteys toimii"
    except Exception as e:
        return False, f"Tietokantayhteys epäonnistui: {str(e)}"

# Perusreitit
@app.route("/", methods=["GET", "POST"])
def index():
    """Pääsivu - näyttää index.html templaten"""
    try:
        return render_template("index.html")
    except Exception as e:
        logger.error(f"Virhe index-sivulla: {e}")
        return f"Virhe sivun latauksessa: {e}", 500

@app.route("/health")
def health():
    """Terveystarkistus-reitti tietokantayhteydellä"""
    db_status, db_message = test_database_connection()
    
    return jsonify({
        "status": "OK", 
        "message": "Kotiko-sovellus toimii",
        "timestamp": datetime.now().isoformat(),
        "database": {
            "available": db_status,
            "message": db_message
        }
    })

@app.route("/test")
def test():
    """Testi-reitti"""
    return "Kotiko test-sivu toimii!"

@app.route("/db_test")
def db_test():
    """Tietokantatestireitti"""
    db_status, db_message = test_database_connection()
    
    if db_status:
        return jsonify({
            "status": "success",
            "message": db_message,
            "timestamp": datetime.now().isoformat()
        })
    else:
        return jsonify({
            "status": "error", 
            "message": db_message,
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route("/suodata_tiedot", methods=["GET", "POST"])
def suodata_tiedot():
    """Tiedostojen käsittely - täysi versio"""
    try:
        if request.method == "POST":
            tulokset = {}
            
            # Tarkista että tiedostot on lähetetty
            if "ensimmainen_toimitussisalto" not in request.files or "toinen_toimitussisalto" not in request.files:
                return jsonify({"error": "Molemmat PDF-tiedostot vaaditaan"}), 400
            
            ensimmainen_file = request.files["ensimmainen_toimitussisalto"]
            toinen_file = request.files["toinen_toimitussisalto"]
            
            # Tarkista että tiedostot eivät ole tyhjiä
            if ensimmainen_file.filename == "" or toinen_file.filename == "":
                return jsonify({"error": "Valitse molemmat PDF-tiedostot"}), 400
            
            # Tarkista tiedostotyyppi
            if not ensimmainen_file.filename.lower().endswith('.pdf') or not toinen_file.filename.lower().endswith('.pdf'):
                return jsonify({"error": "Vain PDF-tiedostot sallitaan"}), 400
            
            # Tässä vaiheessa palautetaan testidataa
            # Myöhemmin lisätään oikea tiedostojen käsittely
            tulokset = {
                "sievitalo": {
                    "ikkunat": [
                        {"tyyppi": "2-ikkunainen", "koko": "1200x1200", "materiaali": "PVC"},
                        {"tyyppi": "3-ikkunainen", "koko": "1800x1200", "materiaali": "PVC"}
                    ],
                    "ulko_ovet": [
                        {"tyyppi": "Yksilehtinen", "koko": "900x2100", "materiaali": "Puuta"},
                        {"tyyppi": "Kaksilehtinen", "koko": "1800x2100", "materiaali": "Puuta"}
                    ],
                    "valiovi_mallit": {
                        "ovimallit": ["Ovimalli A", "Ovimalli B", "Ovimalli C"]
                    }
                },
                "kastelli": {
                    "ikkunat": [
                        {"tyyppi": "1-ikkunainen", "koko": "600x1200", "materiaali": "Alumiini"},
                        {"tyyppi": "2-ikkunainen", "koko": "1200x1200", "materiaali": "Alumiini"}
                    ],
                    "ulko_ovet": [
                        {"tyyppi": "Yksilehtinen", "koko": "800x2000", "materiaali": "Terästä"},
                        {"tyyppi": "Kaksilehtinen", "koko": "1600x2000", "materiaali": "Terästä"}
                    ],
                    "valiovi_mallit": {
                        "ovimallit": ["Kastelli-malli X", "Kastelli-malli Y"]
                    }
                },
                "message": "Tiedostot vastaanotettu onnistuneesti",
                "status": "success"
            }
            
            # Jos pyyntö on AJAX-pyyntö, palauta JSON-data
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return Response(
                    json.dumps(tulokset),
                    mimetype='application/json'
                )
            
            # Jos ei ole AJAX-pyyntö, näytä template
            return render_template("index.html", tulokset=tulokset)
        
        # GET-pyyntö
        return render_template("index.html")
        
    except Exception as e:
        logger.error(f"Virhe suodata_tiedot-reitissä: {e}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response(
                json.dumps({'error': str(e)}),
                mimetype='application/json'
            )
        return render_template("index.html", virheviesti=f"Virhe: {e}")

@app.route('/sql_hallinta')
def sql_hallinta():
    """SQL-hallintasivu - placeholder"""
    try:
        return render_template('sql_hallinta.html')
    except Exception as e:
        logger.error(f"Virhe SQL-hallintasivulla: {e}")
        return f"SQL-hallintasivu ei ole vielä käytössä: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Kotiko app with full functionality on port {port}")
    
    # Testaa tietokantayhteys käynnistyksessä
    if DB_AVAILABLE:
        db_status, db_message = test_database_connection()
        logger.info(f"Tietokantatesti: {db_message}")
    else:
        logger.warning("Tietokantamoduulit eivät ole saatavilla")
    
    app.run(host="0.0.0.0", port=port, debug=False)
