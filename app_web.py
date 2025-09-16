#!/usr/bin/env python3
"""
Talobot - Web-käyttöliittymä
Yksinkertainen selainkäyttöliittymä PDF-analyysiin
"""

import os
import sys
import uuid
from pathlib import Path
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import json

# Lisää polut
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("utils"))
sys.path.append(os.path.abspath("backend"))

from logger_config import configure_logging
import logging

# Loggerin alustus
configure_logging()
logger = logging.getLogger(__name__)

# Flask-sovellus
app = Flask(__name__)
app.secret_key = 'talobot-secret-key-2024'

# Konfiguraatio
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Tarkista onko tiedosto sallittu"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Pääsivu - PDF-lataus"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Käsittele PDF-tiedostojen lataus"""
    try:
        # Tarkista että kaksi tiedostoa on valittu
        if 'file1' not in request.files or 'file2' not in request.files:
            flash('Valitse molemmat PDF-tiedostot!', 'error')
            return redirect(url_for('index'))
        
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        # Tarkista että tiedostot on valittu
        if file1.filename == '' or file2.filename == '':
            flash('Valitse molemmat PDF-tiedostot!', 'error')
            return redirect(url_for('index'))
        
        # Tarkista tiedostotyypit
        if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
            flash('Vain PDF-tiedostot sallittu!', 'error')
            return redirect(url_for('index'))
        
        # Tallenna tiedostot
        file1_id = str(uuid.uuid4())
        file2_id = str(uuid.uuid4())
        
        file1_path = UPLOAD_FOLDER / f"{file1_id}.pdf"
        file2_path = UPLOAD_FOLDER / f"{file2_id}.pdf"
        
        file1.save(str(file1_path))
        file2.save(str(file2_path))
        
        logger.info(f"Tallennettu tiedostot: {file1_id}, {file2_id}")
        
        # Analysoi tiedostot
        return analyze_documents(str(file1_path), str(file2_path))
        
    except Exception as e:
        logger.error(f"Virhe tiedostojen latauksessa: {e}")
        flash(f'Virhe tiedostojen latauksessa: {e}', 'error')
        return redirect(url_for('index'))

def analyze_documents(file1_path, file2_path):
    """Analysoi kaksi PDF-tiedostoa"""
    try:
        logger.info(f"Aloitetaan analyysi: {file1_path}, {file2_path}")
        
        # Tuo tarvittavat moduulit
        from SQL_kyselyt import vastaanota_toimitussisalto, hae_toimittaja_uuidlla, hae_toimitussisalto_id_uuidlla
        from SQL_kyselyt import hae_pdf_url_uuidlla, hae_uuid_toimitussisalto_idlla, lisaa_vertailu
        from SQL_kyselyt import hae_toimitussisallon_ikkunat, hae_toimitussisallon_ulko_ovet, hae_toimitussisallon_valiovet
        from run import run_sievitalo, run_kastelli
        
        # Käsittele ensimmäinen tiedosto
        logger.info("Käsitellään ensimmäinen tiedosto...")
        with open(file1_path, 'rb') as f:
            unique_id_1 = vastaanota_toimitussisalto(f)
        
        # Käsittele toinen tiedosto
        logger.info("Käsitellään toinen tiedosto...")
        with open(file2_path, 'rb') as f:
            unique_id_2 = vastaanota_toimitussisalto(f)
        
        # Luo vertailu
        logger.info("Luodaan vertailu...")
        lisaa_vertailu(
            hae_toimitussisalto_id_uuidlla(unique_id_1), 
            hae_toimitussisalto_id_uuidlla(unique_id_2)
        )
        
        # Analysoi ensimmäinen tiedosto
        logger.info("Analysoidaan ensimmäinen tiedosto...")
        toimittaja_1 = hae_toimittaja_uuidlla(unique_id_1)
        toimitussisalto_id_1 = hae_toimitussisalto_id_uuidlla(unique_id_1)
        pdf_url_1 = hae_pdf_url_uuidlla(uuid=hae_uuid_toimitussisalto_idlla(toimitussisalto_id_1))
        
        if toimittaja_1 == "Sievitalo":
            logger.info("Suoritetaan Sievitalo-analyysi...")
            run_sievitalo(pdf_url_1, toimitussisalto_id_1)
        elif toimittaja_1 == "Kastelli":
            logger.info("Suoritetaan Kastelli-analyysi...")
            run_kastelli(pdf_url_1, toimitussisalto_id_1)
        else:
            logger.warning(f"Tuntematon toimittaja: {toimittaja_1}")
        
        # Analysoi toinen tiedosto
        logger.info("Analysoidaan toinen tiedosto...")
        toimittaja_2 = hae_toimittaja_uuidlla(unique_id_2)
        toimitussisalto_id_2 = hae_toimitussisalto_id_uuidlla(unique_id_2)
        pdf_url_2 = hae_pdf_url_uuidlla(uuid=hae_uuid_toimitussisalto_idlla(toimitussisalto_id_2))
        
        if toimittaja_2 == "Sievitalo":
            logger.info("Suoritetaan Sievitalo-analyysi...")
            run_sievitalo(pdf_url_2, toimitussisalto_id_2)
        elif toimittaja_2 == "Kastelli":
            logger.info("Suoritetaan Kastelli-analyysi...")
            run_kastelli(pdf_url_2, toimitussisalto_id_2)
        else:
            logger.warning(f"Tuntematon toimittaja: {toimittaja_2}")
        
        # Hae tulokset
        logger.info("Haetaan analyysitulokset...")
        ikkunat_1 = hae_toimitussisallon_ikkunat(toimitussisalto_id_1)
        ulko_ovet_1 = hae_toimitussisallon_ulko_ovet(toimitussisalto_id_1)
        valiovet_1 = hae_toimitussisallon_valiovet(toimitussisalto_id_1)
        
        ikkunat_2 = hae_toimitussisallon_ikkunat(toimitussisalto_id_2)
        ulko_ovet_2 = hae_toimitussisallon_ulko_ovet(toimitussisalto_id_2)
        valiovet_2 = hae_toimitussisallon_valiovet(toimitussisalto_id_2)
        
        # Muodosta tulokset
        tulokset = {
            "analyysi_1": {
                "toimittaja": toimittaja_1,
                "id": toimitussisalto_id_1,
                "ikkunat": ikkunat_1,
                "ulko_ovet": ulko_ovet_1,
                "valiovet": valiovet_1
            },
            "analyysi_2": {
                "toimittaja": toimittaja_2,
                "id": toimitussisalto_id_2,
                "ikkunat": ikkunat_2,
                "ulko_ovet": ulko_ovet_2,
                "valiovet": valiovet_2
            }
        }
        
        logger.info("Analyysi valmis!")
        return render_template('results.html', tulokset=tulokset)
        
    except Exception as e:
        logger.error(f"Virhe analyysissa: {e}")
        flash(f'Virhe analyysissa: {e}', 'error')
        return redirect(url_for('index'))

@app.route('/health')
def health():
    """Terveystarkistus"""
    return jsonify({
        "status": "OK",
        "message": "Talobot web-käyttöliittymä toimii"
    })

if __name__ == '__main__':
    logger.info("Käynnistetään Talobot web-käyttöliittymä...")
    # Debug-moodi pois päältä tuotantokäyttöön
    app.run(host='0.0.0.0', port=5000, debug=False)

