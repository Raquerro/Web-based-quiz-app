from flask_login import login_required
from .services import teacher_dashboard_service, teacher_quizzes_service, teacher_quiz_report_service
from . import teacher_bp

@teacher_bp.route("/home")
@login_required
def home_student():
    return teacher_dashboard_service()

# --- Lista quizów nauczyciela ---
@teacher_bp.route("/my")
@login_required
def my_quizzes():
    return teacher_quizzes_service()

# --- Wyniki quizu dla nauczyciela ---
@teacher_bp.route("/report/<int:quiz_id>")
@login_required
def quiz_report(quiz_id):
    return teacher_quiz_report_service(quiz_id)
