from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from math import ceil
from main.models import db, Quiz, StudentQuiz, StudentAnswer
from main.student.utils import calculate_quiz_score

def join_quiz_service():
    if current_user.role != "student":
        return "Nauczyciel nie może dołączać do quizu!", 403

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


def solve_quiz_service(quiz_id):
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


def result_quiz_service(quiz_id):
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

def home_student_service():
    if current_user.role != "student":
        return "Brak uprawnień", 403

    page = request.args.get("page", 1, type=int)
    per_page = 10
    status_filter = request.args.get("status", "all")  
    sort_by = request.args.get("sort", "finished_at")  

    query = StudentQuiz.query.filter_by(student_id=current_user.id)

    if status_filter == "finished":
        query = query.filter(StudentQuiz.finished_at.isnot(None))
    elif status_filter == "unfinished":
        query = query.filter(StudentQuiz.finished_at.is_(None))

    all_quizzes = query.order_by(StudentQuiz.started_at.desc()).all()

    quizzes_data = []
    for sq in all_quizzes:
        quizzes_data.append({
            "id": sq.quiz.id,
            "title": sq.quiz.title,
            "status": "Ukończony" if sq.finished_at else "Nieukończony",
            "score": calculate_quiz_score(sq) if sq.finished_at else None,
            "finished_at": sq.finished_at
        })

    # Sortowanie
    if sort_by == "score":
        quizzes_data.sort(key=lambda x: (x["score"] is None, -x["score"] if x["score"] is not None else 0))
    else:
        quizzes_data.sort(key=lambda x: x["finished_at"] or datetime.min, reverse=True)

    # Paginacja
    total_quizzes = len(quizzes_data)
    total_pages = ceil(total_quizzes / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    quizzes_page = quizzes_data[start:end]

    # Ostatni ukończony quiz
    finished_quizzes = [q for q in quizzes_data if q["status"] == "Ukończony"]
    last_quiz = finished_quizzes[0] if finished_quizzes else None
    last_score = last_quiz["score"] if last_quiz else None

    return render_template(
        "home_student.html",
        last_quiz=last_quiz,
        last_score=last_score,
        quizzes=quizzes_page,
        total_quizzes=total_quizzes,
        total_pages=total_pages,
        current_page=page,
        status_filter=status_filter,
        sort_by=sort_by
    )