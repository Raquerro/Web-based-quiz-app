from main.models import Quiz, StudentQuiz, db, Question, Answer, StudentQuiz, StudentAnswer
from sqlalchemy import func, case

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

    # policz średni wynik na podstawie odpowiedzi
    # najpierw liczba poprawnych odpowiedzi per StudentQuiz
    correct_counts = (
        db.session.query(
            StudentAnswer.student_quiz_id.label("sq_id"),
            func.count().label("correct_count")
        )
        .join(Answer, StudentAnswer.answer_id == Answer.id)
        .filter(Answer.is_correct == True)
        .group_by(StudentAnswer.student_quiz_id)
        .subquery()
    )

    # liczba pytań per quiz
    question_counts = (
        db.session.query(
            Question.quiz_id.label("quiz_id"),
            func.count().label("total_questions")
        )
        .group_by(Question.quiz_id)
        .subquery()
    )

    # wynik procentowy dla każdego StudentQuiz
    scores_query = (
        db.session.query(
            (correct_counts.c.correct_count * 100.0 / question_counts.c.total_questions).label("score")
        )
        .join(StudentQuiz, StudentQuiz.id == correct_counts.c.sq_id)
        .join(question_counts, question_counts.c.quiz_id == StudentQuiz.quiz_id)
        .filter(StudentQuiz.quiz_id.in_(quiz_ids))
    )

    average_score = db.session.query(func.avg(scores_query.subquery().c.score)).scalar()
    average_score = round(average_score, 2) if average_score else 0

    # Ostatni quiz
    last_quiz = max(quizzes, key=lambda q: q.created_at)
    last_quiz_info = {"title": last_quiz.title, "created_at": last_quiz.created_at}

    return {
        "unique_students_count": unique_students_count,
        "average_score": average_score,
        "last_quiz": last_quiz_info,
    }
