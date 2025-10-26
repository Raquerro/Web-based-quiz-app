import random
import string
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from main.models import db, Quiz, StudentQuiz, Question, Answer

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")


# --- Pomocnicza funkcja: generowanie kodu ---
def generate_code(length=6):
    """Generuje unikalny kod quizu (np. A8D5FZ)."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# --- Lista quizów nauczyciela ---
@quiz_bp.route("/my")
@login_required
def my_quizzes():
    if current_user.role != "teacher":
        return "Brak uprawnień", 403

    quizzes = Quiz.query.filter_by(teacher_id=current_user.id).all()
    return render_template("quiz_list.html", quizzes=quizzes)


# --- Tworzenie nowego quizu ---
@quiz_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_quiz():
    if current_user.role != "teacher":
        return "Brak uprawnień", 403

    if request.method == "POST":
        title = request.form.get("title")
        if not title:
            flash("Tytuł quizu jest wymagany", "danger")
            return render_template("quiz_create.html")

        new_quiz = Quiz(
            teacher_id=current_user.id,
            title=title.strip(),
            code=generate_code(),
        )
        db.session.add(new_quiz)
        db.session.commit()
        flash("Quiz został utworzony!", "success")
        return redirect(url_for("quiz.my_quizzes"))

    return render_template("quiz_create.html")


# --- Edycja quizu ---
@quiz_bp.route("/edit/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.teacher_id != current_user.id:
        return "Brak uprawnień", 403

    if request.method == "POST":
        title = request.form.get("title")
        if not title:
            flash("Tytuł nie może być pusty", "danger")
            return render_template("quiz_edit.html", quiz=quiz)

        quiz.title = title.strip()
        db.session.commit()
        flash("Quiz został zaktualizowany!", "success")
        return redirect(url_for("quiz.my_quizzes"))

    return render_template("quiz_edit.html", quiz=quiz)


# --- Usuwanie quizu ---
@quiz_bp.route("/delete/<int:quiz_id>", methods=["POST"])
@login_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.teacher_id != current_user.id:
        return "Brak uprawnień", 403

    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz został usunięty", "success")
    return redirect(url_for("quiz.my_quizzes"))


# --- Wyniki quizu ---
@quiz_bp.route("/results/<int:quiz_id>")
@login_required
def quiz_results(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.teacher_id != current_user.id:
        return "Brak uprawnień", 403

    student_results = quiz.student_quizzes  # lista StudentQuiz
    return render_template("quiz_results.html", quiz=quiz, student_results=student_results)

# --- Dodawanie pytania do quizu ---
@quiz_bp.route("/<int:quiz_id>/add_question", methods=["GET", "POST"])
@login_required
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.teacher_id != current_user.id:
        return "Brak uprawnień", 403

    if request.method == "POST":
        text = request.form.get("text")
        answers = request.form.getlist("answers[]")
        correct_index = int(request.form.get("correct", -1))

        if not text or not answers:
            flash("Wprowadź pytanie i odpowiedzi", "danger")
            return render_template("question_add.html", quiz=quiz)

        # Utwórz pytanie
        question = Question(text=text.strip())
        quiz.questions.append(question)  # automatycznie ustawia quiz_id

        #odpowiedzi
        for i, a in enumerate(answers):
            question.answers.append(Answer(
                text=a.strip(),
                is_correct=(i == correct_index)
            ))


        db.session.commit()
        flash("Pytanie dodane!", "success")
        return redirect(url_for("quiz.edit_quiz", quiz_id=quiz.id))

    return render_template("question_add.html", quiz=quiz)