from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db
from flask_bcrypt import Bcrypt

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

# --------------------------
# Logowanie
# --------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("homepage"))  # przekierowanie po poprawnym loginie
        return render_template("login.html", error="Niepoprawny login lub hasło")
    return render_template("login.html")


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
