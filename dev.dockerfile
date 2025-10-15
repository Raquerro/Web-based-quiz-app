FROM python:3.10-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj tylko plik requirements.txt, żeby cache działał szybciej
COPY requirements.txt ./

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Zmienna środowiskowa dla Flask
ENV FLASK_APP=main.app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development  
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Nie kopiuj kodu tutaj — kod będzie montowany jako wolumen z hosta

# Komenda startowa
CMD ["python", "-m", "main.app"]
