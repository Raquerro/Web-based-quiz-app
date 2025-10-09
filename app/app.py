import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from auth.routes import auth_bp

# 🔹 Wczytaj .env
load_dotenv()

app = Flask(__name__)

# 🔹 Ustaw SECRET_KEY z .env
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['DEBUG'] = os.getenv("DEBUG") == "True"

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# Bcrypt
bcrypt = Bcrypt(app)

# Rejestracja blueprinta auth
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)
