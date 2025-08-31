web: gunicorn -w 2 --timeout 120 app:app --bind 0.0.0.0:$PORT

worker: python Testeri.py
