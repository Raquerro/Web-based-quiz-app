from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required, UserMixin
from flask_bcrypt import Bcrypt

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

@auth_bp.route("/test")
def test():
    return {"message": "Blueprint działa!"}


# Dummy users
users = {
    "student@example.com": {"password": bcrypt.generate_password_hash("student123").decode('utf-8'), "role": "student"},
    "teacher@example.com": {"password": bcrypt.generate_password_hash("teacher123").decode('utf-8'), "role": "teacher"}
}

class User(UserMixin):
    def __init__(self, id_, email, role):
        self.id = id_
        self.email = email
        self.role = role

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
