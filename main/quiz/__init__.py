from flask import Blueprint

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")

# Importujemy podmoduły, żeby zarejestrowały swoje endpointy
from .routes import base, questions, results, stats
