from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Quiz, StudentQuiz, StudentAnswer, Question, Answer

student_bp = Blueprint("student", __name__, url_prefix="/student")


# --- Dołączanie do quizu po kodzie ---
@student_bp.route("/join", methods=["GET", "POST"])
@login_required
def join_quiz():
    if current_user.role != "student":
        return "Brak uprawnień", 403

    if request.method == "POST":
        code = request.form.get("code", "").strip().upper()
        if not code:
            flash("Wprowadź kod quizu", "danger")
            return render_template("student_join.html")

        quiz = Quiz.query.filter_by(code=code).first()
        if not quiz:
            flash("Nie znaleziono quizu o podanym kodzie", "danger")
            return render_template("student_join.html")

        # Sprawdź, czy uczeń już brał udział
        existing = StudentQuiz.query.filter_by(student_id=current_user.id, quiz_id=quiz.id).first()
        if existing:
            flash("Już dołączyłeś do tego quizu!", "info")
            return redirect(url_for("student.solve_quiz", quiz_id=quiz.id))

        # Utwórz nowy rekord udziału ucznia w quizie
        student_quiz = StudentQuiz(
            student_id=current_user.id,
            quiz_id=quiz.id,
            started_at=datetime.utcnow()
        )
        db.session.add(student_quiz)
        db.session.commit()

        flash(f"Dołączono do quizu: {quiz.title}", "success")
        return redirect(url_for("student.solve_quiz", quiz_id=quiz.id))

    return render_template("student_join.html")


# --- Rozwiązywanie quizu ---
@student_bp.route("/solve/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def solve_quiz(quiz_id):
    if current_user.role != "student":
        return "Brak uprawnień", 403

    quiz = Quiz.query.get_or_404(quiz_id)
    student_quiz = StudentQuiz.query.filter_by(student_id=current_user.id, quiz_id=quiz.id).first()

    if not student_quiz:
        flash("Nie jesteś zapisany do tego quizu", "danger")
        return redirect(url_for("student.join_quiz"))

    # Jeśli quiz już zakończony – pokaż wynik
    if student_quiz.finished_at:
        return redirect(url_for("student.result_quiz", quiz_id=quiz.id))

    if request.method == "POST":
        # Usuń wcześniejsze odpowiedzi (jeśli ktoś odświeży stronę)
        StudentAnswer.query.filter_by(student_quiz_id=student_quiz.id).delete()

        for question in quiz.questions:
            selected_answer_id = request.form.get(str(question.id))
            if selected_answer_id:
                db.session.add(StudentAnswer(
                    student_quiz_id=student_quiz.id,
                    question_id=question.id,
                    answer_id=int(selected_answer_id)
                ))

        student_quiz.finished_at = datetime.utcnow()
        db.session.commit()

        flash("Quiz zakończony! Możesz sprawdzić wynik.", "success")
        return redirect(url_for("student.result_quiz", quiz_id=quiz.id))

    return render_template("student_solve.html", quiz=quiz)


# --- Wynik ucznia ---
@student_bp.route("/result/<int:quiz_id>")
@login_required
def result_quiz(quiz_id):
    if current_user.role != "student":
        return "Brak uprawnień", 403

    quiz = Quiz.query.get_or_404(quiz_id)
    student_quiz = StudentQuiz.query.filter_by(student_id=current_user.id, quiz_id=quiz.id).first_or_404()

    if not student_quiz.finished_at:
        flash("Najpierw zakończ quiz", "warning")
        return redirect(url_for("student.solve_quiz", quiz_id=quiz.id))

    # Liczenie wyniku
    total_questions = len(quiz.questions)
    correct_answers = 0

    for q in quiz.questions:
        correct = next((a.id for a in q.answers if a.is_correct), None)
        chosen = next(
            (sa.answer_id for sa in student_quiz.student_answers if sa.question_id == q.id),
            None
        )
        if correct and chosen == correct:
            correct_answers += 1

    score_percent = round((correct_answers / total_questions) * 100, 2) if total_questions else 0

    return render_template(
        "student_result.html",
        quiz=quiz,
        correct=correct_answers,
        total=total_questions,
        score=score_percent
    )
