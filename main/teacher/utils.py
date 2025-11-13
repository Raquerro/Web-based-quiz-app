from main.models import Quiz, StudentQuiz, db
from sqlalchemy import func

def get_last_quizzes(teacher_id, limit=3):
    """Zwraca ostatnie n quizów danego nauczyciela"""
    quizzes = (
        Quiz.query.filter_by(teacher_id=teacher_id)
        .order_by(Quiz.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {"id": q.id, "title": q.title, "created_at": q.created_at}
        for q in quizzes
    ]


def calculate_teacher_statistics(teacher_id):
    """Oblicza statystyki ogólne nauczyciela"""

    # Pobierz wszystkie quizy nauczyciela
    quizzes = Quiz.query.filter_by(teacher_id=teacher_id).all()
    if not quizzes:
        return {
            "unique_students_count": 0,
            "average_score": 0,
            "last_quiz": None,
        }

    quiz_ids = [q.id for q in quizzes]

    # Liczba unikalnych studentów
    unique_students_count = (
        db.session.query(StudentQuiz.student_id)
        .filter(StudentQuiz.quiz_id.in_(quiz_ids))
        .distinct()
        .count()
    )

    # Średni wynik wszystkich quizów – lepiej policzyć w SQL, jeśli masz pole score
    average_score = (
        db.session.query(func.avg(StudentQuiz.score))
        .filter(StudentQuiz.quiz_id.in_(quiz_ids))
        .scalar()
    )
    average_score = round(average_score, 2) if average_score else 0

    # Ostatni quiz
    last_quiz = max(quizzes, key=lambda q: q.created_at)
    last_quiz_info = {"title": last_quiz.title, "created_at": last_quiz.created_at}

    return {
        "unique_students_count": unique_students_count,
        "average_score": average_score,
        "last_quiz": last_quiz_info,
    }
