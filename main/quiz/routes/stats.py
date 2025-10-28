from flask import render_template
from flask_login import login_required, current_user
from main.models import Quiz
from .. import quiz_bp

# --- Statystyki quizu (dla nauczyciela) ---
@quiz_bp.route("/stats/<int:quiz_id>")
@login_required
def quiz_stats(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.teacher_id != current_user.id:
        return "Brak uprawnień", 403

    student_quizzes = quiz.student_quizzes  # lista StudentQuiz
    total_students = len(student_quizzes)
    finished_students = [sq for sq in student_quizzes if sq.finished_at]

    if not finished_students:
        avg_score = highest_score = lowest_score = 0
    else:
        results = []
        for sq in finished_students:
            total_q = len(quiz.questions)
            correct = 0
            for q in quiz.questions:
                correct_answer = next((a.id for a in q.answers if a.is_correct), None)
                chosen = next(
                    (sa.answer_id for sa in sq.student_answers if sa.question_id == q.id),
                    None
                )
                if correct_answer and chosen == correct_answer:
                    correct += 1
            score = round((correct / total_q) * 100, 2) if total_q else 0
            results.append(score)

        avg_score = round(sum(results) / len(results), 2)
        highest_score = max(results)
        lowest_score = min(results)

    completion_rate = round((len(finished_students) / total_students) * 100, 2) if total_students else 0

    return render_template(
        "quiz_stats.html",
        quiz=quiz,
        total_students=total_students,
        finished_students=len(finished_students),
        avg_score=avg_score,
        highest_score=highest_score,
        lowest_score=lowest_score,
        completion_rate=completion_rate
    )