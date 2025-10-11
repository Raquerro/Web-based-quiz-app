FROM python:3.10-slim

# Ustaw katalog roboczy wewnątrz kontenera
WORKDIR /app

# Zainstaluj zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj pozostałe pliki projektu
COPY . .

# Wskaż aplikację Flask
ENV FLASK_APP=app.py

# Uruchom aplikację
CMD ["python", "app.py"]
