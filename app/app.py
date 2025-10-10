import os
from dotenv import load_dotenv
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from auth.routes import auth_bp


# 🔹 Wczytaj .env
load_dotenv()

app = Flask(__name__ , template_folder='templates')

@app.route("/")
def home():
    return redirect(url_for('login'))

# Strona logowania
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Na razie tylko testowo — bez logiki logowania czy działa
        if username == "admin" and password == "admin":
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html', error="Niepoprawne dane logowania")

    return render_template('login.html')

#Strona domowa -> TO DO 
@app.route('/home')
def homepage():
    return render_template('home.html')


# 🔹 Ustaw SECRET_KEY z .env
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['DEBUG'] = os.getenv("DEBUG") == "True"

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# Tymczasowy brak użytkownika (zeby buggow nie bylo)
@login_manager.user_loader
def load_user(user_id):
    return None  # jeszcze nie ładujemy użytkowników z bazy

# Bcrypt
bcrypt = Bcrypt(app)

# Rejestracja blueprinta auth
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)
