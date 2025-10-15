FROM python:3.10-slim

# Ustaw katalog roboczy wewnątrz kontenera
WORKDIR /app

# Skopiuj pliki z projektu
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj całość projektu
COPY . .

# Ustaw zmienne środowiskowe dla Flask
ENV FLASK_APP=main/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Otwórz port
EXPOSE 5000

# Uruchom aplikację Flask
CMD ["flask", "run"]

