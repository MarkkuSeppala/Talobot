#!/usr/bin/env python3
"""
Talobot web-käyttöliittymä debug-versiolla
"""

import os
import sys
sys.path.append(os.path.abspath("."))

# Tuo pääsovellus
from app_web import app, logger

if __name__ == '__main__':
    logger.info("Käynnistetään Talobot web-käyttöliittymä DEBUG-moodissa...")
    # Debug-moodi päällä kehitysympäristöä varten
    app.run(host='0.0.0.0', port=5000, debug=True)


