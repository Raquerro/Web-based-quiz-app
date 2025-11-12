from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from main.models import db, User
from main.config import Config
from main.auth.routes import auth_bp
from main.quiz import quiz_bp
from main.student.student_bp import student_bp


app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)


db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/home")
@login_required
def homepage():
    if current_user.role == "teacher":
        return render_template("home_teacher.html")
    elif current_user.role == "student":
        return render_template("home_student.html")
    else:
        return redirect(url_for("auth.logout"))


@app.route("/")
def home_redirect():
    return redirect(url_for("auth.login"))

app.register_blueprint(auth_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(student_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)