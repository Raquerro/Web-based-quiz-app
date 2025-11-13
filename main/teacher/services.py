from flask_login import current_user
from .utils import get_last_quizzes, calculate_teacher_statistics
from flask import render_template, jsonify

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