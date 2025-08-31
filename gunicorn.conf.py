import os

# Portti ympäristömuuttujasta tai oletusarvo
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"

# Worker-prosessien määrä
workers = 2

# Timeout-asetukset
timeout = 120
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Muut asetukset
preload_app = True
max_requests = 1000
max_requests_jitter = 100

# Render.com:n ympäristössä varmistetaan että portti on oikein
if os.environ.get("RENDER"):
    print(f"Render.com ympäristö, portti: {os.environ.get('PORT', '8080')}")
    print(f"Bind: {bind}")
