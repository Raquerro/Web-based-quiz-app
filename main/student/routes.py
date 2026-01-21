from flask_login import login_required
from . import student_bp
from .services import (
    join_quiz_service,
    solve_quiz_service,
    result_quiz_service,
    review_quiz_service,
    home_student_service,
)

@student_bp.route("/join", methods=["GET", "POST"])
@login_required
def join_quiz():
    return join_quiz_service()


@student_bp.route("/solve/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def solve_quiz(quiz_id):
    return solve_quiz_service(quiz_id)


@student_bp.route("/result/<int:quiz_id>")
@login_required
def result_quiz(quiz_id):
    return result_quiz_service(quiz_id)

@student_bp.route("/review/<int:student_quiz_id>")
@login_required
def review_quiz(student_quiz_id):
    return review_quiz_service(student_quiz_id)

@student_bp.route("/home")
@login_required
def home_student():
    return home_student_service()
