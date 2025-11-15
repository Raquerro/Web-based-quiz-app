from flask_login import current_user
from .utils import get_last_quizzes, calculate_teacher_statistics
from flask import render_template, jsonify
from main.models import Quiz, db
from statistics import median

def teacher_dashboard_service():
    if current_user.role != "teacher":
        return "Brak uprawnień", 403

    # Lista ostatnich 5 quizów
    last_quizzes = get_last_quizzes(current_user.id, limit=5)

    # Statystyki ogólne
    unique_students_count, average_score, last_quiz_info = calculate_teacher_statistics(current_user.id)

    # Możesz zwrócić JSON lub renderować szablon
    return render_template(
        "teacher_dashboard.html",
        last_quizzes=last_quizzes,
        unique_students_count=unique_students_count,
        average_score=average_score,
        last_quiz=last_quiz_info
    )

    # Przykład JSON:
    # return jsonify({
    #     "last_quizzes": last_quizzes,
    #     "unique_students_count": unique_students_count,
    #     "average_score": average_score,
    #     "last_quiz": last_quiz_info
    # })

def teacher_quizzes_service():
    if current_user.role != "teacher":
        return "Brak uprawnień", 403

    quizzes = Quiz.query.filter_by(teacher_id=current_user.id).all()
    return render_template("quiz_list.html", quizzes=quizzes)

def teacher_quiz_report_service(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Sprawdzenie uprawnień
    if quiz.teacher_id != current_user.id or current_user.role != "teacher":
        return "Brak uprawnień", 403

    student_quizzes = quiz.student_quizzes
    total_students = len(student_quizzes)
    finished_students = [sq for sq in student_quizzes if sq.finished_at]

    results_data, scores = [], []
    question_stats = {q.id: {"text": q.text, "correct_count": 0, "total": 0} for q in quiz.questions}

    for sq in finished_students:
        total_q = len(quiz.questions)
        correct = 0
        for q in quiz.questions:
            correct_answer = next((a.id for a in q.answers if a.is_correct), None)
            chosen = next(
                (sa.answer_id for sa in sq.student_answers if sa.question_id == q.id),
                None
            )
            if correct_answer:
                question_stats[q.id]["total"] += 1
                if chosen == correct_answer:
                    correct += 1
                    question_stats[q.id]["correct_count"] += 1

        score = round((correct / total_q) * 100, 2) if total_q else 0
        scores.append(score)
        results_data.append({"username": sq.student.username, "score": score})

    # Statystyki ogólne
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0
    median_score = round(median(scores), 2) if scores else 0
    highest_score = max(scores) if scores else 0
    lowest_score = min(scores) if scores else 0
    completion_rate = round((len(finished_students) / total_students) * 100, 2) if total_students else 0

    # Ranking TOP 5 studentów
    top_students = sorted(results_data, key=lambda r: r["score"], reverse=True)[:5]

    # Procent poprawnych odpowiedzi dla każdego pytania
    question_accuracy = [
        {
            "text": q["text"],
            "accuracy": round((q["correct_count"] / q["total"]) * 100, 2) if q["total"] else 0
        }
        for q in question_stats.values()
    ]

    return render_template(
        "quiz_report.html",
        quiz=quiz,
        total_students=total_students,
        finished_students=len(finished_students),
        avg_score=avg_score,
        median_score=median_score,
        highest_score=highest_score,
        lowest_score=lowest_score,
        completion_rate=completion_rate,
        results_data=results_data,
        top_students=top_students,
        question_accuracy=question_accuracy
    )