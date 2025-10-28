from flask import render_template
from flask_login import login_required, current_user
from main.models import Quiz
from .. import quiz_bp

# --- Wyniki quizu ---
@quiz_bp.route("/results/<int:quiz_id>")
@login_required
def quiz_results(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.teacher_id != current_user.id:
        return "Brak uprawnień", 403

    student_results = quiz.student_quizzes  # lista StudentQuiz
    return render_template("quiz_results.html", quiz=quiz, student_results=student_results)