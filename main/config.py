import os
from dotenv import load_dotenv

# Wczytanie pliku .env (poziom wyżej od /main)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Ustawione DB_URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
        f"@localhost:5432/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

 # Bezpieczeństwo ciasteczek
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # True jeśli masz HTTPS
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False
