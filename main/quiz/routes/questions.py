from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from main.models import db, Quiz, Question, Answer
from .. import quiz_bp


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

    # --- Usuwanie pytania ---
@quiz_bp.route("/<int:quiz_id>/delete_question/<int:question_id>", methods=["POST"])
@login_required
def delete_question(quiz_id, question_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    question = Question.query.get_or_404(question_id)

    if quiz.teacher_id != current_user.id:
        return "Brak uprawnień", 403

    db.session.delete(question)
    db.session.commit()
    flash("Pytanie zostało usunięte.", "success")
    return redirect(url_for("quiz.edit_quiz", quiz_id=quiz.id))