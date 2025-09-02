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
    from SQL_kyselyt import (hae_toimittaja_uuidlla, hae_toimitussisalto_id_uuidlla, 
                             vastaanota_toimitussisalto, lisaa_vertailu,
                             hae_pdf_url_uuidlla, hae_uuid_toimitussisalto_idlla, 
                             hae_toimitussisallon_ikkunat, hae_toimitussisallon_ulko_ovet, hae_toimitussisallon_valiovet)
    from run import run_sievitalo, run_kastelli
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
            
            # Oikea tiedostojen käsittely
            logging.info("Aloitetaan tiedostojen käsittely")
            
            # Ensimmainen toimitussisalto
            if "ensimmainen_toimitussisalto" in request.files:
                pdf_file_1 = request.files["ensimmainen_toimitussisalto"]
                unique_tiedostonimi_ensimmainen_toimitussisalto = vastaanota_toimitussisalto(pdf_file_1)
                logging.info(f"Ensimmäinen toimitussisältö lisätty kantaan: {unique_tiedostonimi_ensimmainen_toimitussisalto}")
            
            # Toinen toimitussisalto
            if "toinen_toimitussisalto" in request.files:
                pdf_file_2 = request.files["toinen_toimitussisalto"]            
                unique_tiedostonimi_toinen_toimitussisalto = vastaanota_toimitussisalto(pdf_file_2)
                logging.info(f"Toinen toimitussisältö lisätty kantaan: {unique_tiedostonimi_toinen_toimitussisalto}")
                
                # Lisää vertailu
                lisaa_vertailu(hae_toimitussisalto_id_uuidlla(unique_tiedostonimi_ensimmainen_toimitussisalto), hae_toimitussisalto_id_uuidlla(unique_tiedostonimi_toinen_toimitussisalto))
            
            # Sievitalo-käsittely
            if hae_toimittaja_uuidlla(unique_tiedostonimi_ensimmainen_toimitussisalto) == "Sievitalo":
                logging.info("Tunnistettu Sievitalo toimitussisalto")
                
                toimitussisallon_id = hae_toimitussisalto_id_uuidlla(unique_tiedostonimi_ensimmainen_toimitussisalto)
                pdf_url = hae_pdf_url_uuidlla(uuid=hae_uuid_toimitussisalto_idlla(toimitussisallon_id))
                
                logging.info("Aloitetaan run_sievitalo")
                run_sievitalo(pdf_url, toimitussisallon_id)
                logging.info("run_sievitalo valmis")
                
                # Haetaan käsitellyt tiedot tietokannasta
                ikkunat = hae_toimitussisallon_ikkunat(toimitussisallon_id)
                ulko_ovet = hae_toimitussisallon_ulko_ovet(toimitussisallon_id)
                valiovi_mallit = hae_toimitussisallon_valiovet(toimitussisallon_id)
                
                logging.info(f"Haettu ikkunoita: {len(ikkunat) if ikkunat else 0}")
                
                tulokset["sievitalo"] = {
                    "ikkunat": ikkunat,
                    "ulko_ovet": ulko_ovet,
                    "valiovi_mallit": valiovi_mallit
                }
            
            # Kastelli-käsittely
            if hae_toimittaja_uuidlla(unique_tiedostonimi_toinen_toimitussisalto) == "Kastelli":
                logging.info("Tunnistettu Kastelli toimitussisalto")
                
                toimitussisallon_id = hae_toimitussisalto_id_uuidlla(unique_tiedostonimi_toinen_toimitussisalto)
                pdf_url = hae_pdf_url_uuidlla(uuid=hae_uuid_toimitussisalto_idlla(toimitussisallon_id))
                
                logging.info("Aloitetaan run_kastelli")
                run_kastelli(pdf_url, toimitussisallon_id)
                logging.info("run_kastelli valmis")
                
                # Haetaan käsitellyt tiedot tietokannasta
                ikkunat = hae_toimitussisallon_ikkunat(toimitussisallon_id)
                ulko_ovet = hae_toimitussisallon_ulko_ovet(toimitussisallon_id)
                valiovi_mallit = hae_toimitussisallon_valiovet(toimitussisallon_id)
                
                logging.info(f"Haettu ikkunoita: {len(ikkunat) if ikkunat else 0}")
                
                tulokset["kastelli"] = {
                    "ikkunat": ikkunat,
                    "ulko_ovet": ulko_ovet,
                    "valiovi_mallit": valiovi_mallit
                }
            
            # Lisätään viesti
            tulokset["message"] = "Tiedostot vastaanotettu onnistuneesti"
            tulokset["status"] = "success"
            
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
