import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise RuntimeError("DATABASE_URL is not set!")

    # fix Railway / Heroku style URL
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security cookies
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

    # Railway = HTTPS → powinno być True
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True