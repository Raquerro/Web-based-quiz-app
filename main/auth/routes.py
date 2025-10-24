from flask import Blueprint, request, render_template, redirect, url_for, flash, session
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
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Wszystkie pola są wymagane", "danger")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(username=username).first()
        if not user or user.password != password:  # jawne porównanie
            flash("Niepoprawny login lub hasło", "danger")
            return redirect(url_for("auth.login"))
        
        login_user(user)
        flash(f"Zalogowano pomyślnie, {user.username}!", "success")
        return redirect(url_for("homepage"))  
    
    return render_template("login.html")


# --------------------------
# Wylogowanie
# --------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()     # wyczyszczenie sesji
    flash("Pomyślnie wylogowano", "info")
    return redirect(url_for("auth.login"))  


# --------------------------
# Rejestracja
# --------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "student")
        
        # Zabepieczenie ról
        if role not in ["student", "teacher"]:
            role = "student"

        # Walidacja pól
        if not username or not email or not password:
            return render_template("register.html", error="Wszystkie pola są wymagane")
        
        #Sprawdzenie czy użytkownik już istnieje
        if User.query.filter_by(email=email).first() and User.query.filter_by(username=username).first():
            return render_template("register.html", error="Użytkownik już istnieje")

        #Haszowanie hasła
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        #tworzenie użytkownika
        user = User(username=username, email=email, password=hashed_password, role=role)
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
        "username": current_user.username,
        "role": current_user.role,
        "id": current_user.id
    }
