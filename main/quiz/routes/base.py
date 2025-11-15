from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from main.models import db, Quiz
from .. import quiz_bp
from .utils import generate_code

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
        flash("Quiz został utworzony! Teraz możesz dodać pytania.", "success")
        return redirect(url_for("quiz.add_question", quiz_id=new_quiz.id))

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
