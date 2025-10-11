import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from models import db, User
from auth.routes import auth_bp

# --- Wczytanie zmiennych środowiskowych ---
load_dotenv()

# --- Tworzenie aplikacji ---
app = Flask(__name__, template_folder="templates")

# --- Konfiguracja aplikacji ---
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['DEBUG'] = os.getenv("DEBUG") == "True"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@db:5432/{os.getenv('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- Inicjalizacja rozszerzeń ---
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

# --- Ładowanie użytkownika dla Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Tworzenie tabel przy starcie ---
with app.app_context():
    db.create_all()

# --- Routing ---
@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Sprawdzenie użytkownika z bazy
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return redirect(url_for("homepage"))
        else:
            return render_template("login.html", error="Niepoprawne dane logowania")

    return render_template('login.html')

@app.route('/home')
def homepage():
    users = User.query.all()
    return render_template('home.html', users=users)

# --- Rejestracja blueprintów ---
app.register_blueprint(auth_bp)

# --- Uruchomienie ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
