from flask import Flask, request, render_template, Response, redirect, url_for, jsonify
import os
import sys
import uuid
from werkzeug.utils import secure_filename
import io
import logging
from datetime import datetime 
import json

# Yksinkertainen logging konfiguraatio
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

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
    """Terveystarkistus-reitti"""
    return jsonify({
        "status": "OK", 
        "message": "Kotiko-sovellus toimii",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/test")
def test():
    """Testi-reitti"""
    return "Kotiko test-sivu toimii!"

@app.route("/suodata_tiedot", methods=["GET", "POST"])
def suodata_tiedot():
    """Tiedostojen käsittely - yksinkertaistettu versio"""
    try:
        if request.method == "POST":
            # Tässä vaiheessa palautetaan vain placeholder-data
            tulokset = {
                "message": "Tiedostojen käsittely on kehitteillä",
                "status": "placeholder"
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
    logger.info(f"Starting Kotiko app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
