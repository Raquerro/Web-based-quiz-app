from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from flask_bcrypt import Bcrypt

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

# Dummy users na razie (później zamienimy na bazę)
users = {
    "student@example.com": {"password": bcrypt.generate_password_hash("student123").decode('utf-8'), "role": "student"},
    "teacher@example.com": {"password": bcrypt.generate_password_hash("teacher123").decode('utf-8'), "role": "teacher"}
}

# Minimalna klasa User
class User(UserMixin):
    def __init__(self, id_, email, role):
        self.id = id_
        self.email = email
        self.role = role

# Flask-Login loader (do użycia w app.py z login_manager)
login_manager = None  # login_manager będziemy przekazywać z app.py później

def init_login_manager(app, lm):
    global login_manager
    login_manager = lm

    @login_manager.user_loader
    def load_user(user_id):
        for email, data in users.items():
            if email == user_id:
                return User(user_id, email, data['role'])
        return None

# --------------------------
# Endpointy
# --------------------------

# Logowanie
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user_data = users.get(email)
    if user_data and bcrypt.check_password_hash(user_data['password'], password):
        user = User(email, email, user_data['role'])
        login_user(user)
        return {"message": f"Zalogowano jako {user.role}"}, 200
    return {"message": "Nieprawidłowy email lub hasło"}, 401

# Wylogowanie
@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return {"message": "Wylogowano"}, 200

# Rejestracja (dummy, tylko dodaje do users)
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "student")  # domyślnie student

    if email in users:
        return {"message": "Użytkownik już istnieje"}, 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users[email] = {"password": hashed_password, "role": role}
    return {"message": f"Zarejestrowano użytkownika {email} jako {role}"}, 201

# Informacje o aktualnym użytkowniku
@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return {
        "email": current_user.email,
        "role": current_user.role
    }, 200
