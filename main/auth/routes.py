from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from main.models import User, db
from flask_bcrypt import Bcrypt

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

# --------------------------
# Logowanie
# --------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("homepage"))  # przekierowanie po poprawnym loginie
        return render_template("login.html", error="Niepoprawny email lub hasło")
    return render_template("login.html")


# --------------------------
# API login (JSON)
# --------------------------
@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return {"message": f"Zalogowano jako {user.role}"}, 200
    return {"message": "Nieprawidłowy email lub hasło"}, 401


# --------------------------
# Wylogowanie
# --------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))  # po wylogowaniu wraca do logowania


# --------------------------
# Rejestracja
# --------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "student")

        if User.query.filter_by(email=email).first():
            return render_template("register.html", error="Użytkownik już istnieje")

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("register.html")


# --------------------------
# Informacje o aktualnym użytkowniku
# --------------------------
@auth_bp.route("/me")
@login_required
def me():
    return {
        "email": current_user.email,
        "role": current_user.role
    }
