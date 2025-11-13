from main.models import Quiz, StudentQuiz, db

def get_last_quizzes(teacher_id, limit=3):
    """Zwraca ostatnie n quizów danego nauczyciela"""
    quizzes = Quiz.query.filter_by(teacher_id=teacher_id)\
                        .order_by(Quiz.created_at.desc())\
                        .limit(limit).all()
    return [
        {"id": q.id, "title": q.title, "created_at": q.created_at}
        for q in quizzes
    ]

def calculate_teacher_statistics(teacher_id):
    """Oblicza statystyki ogólne nauczyciela"""
    # Pobierz wszystkie quizy nauczyciela
    quizzes = Quiz.query.filter_by(teacher_id=teacher_id).all()
    quiz_ids = [q.id for q in quizzes]

    if not quiz_ids:
        return 0, 0, None

    # Unikalni studenci
    student_ids = db.session.query(StudentQuiz.student_id)\
                            .filter(StudentQuiz.quiz_id.in_(quiz_ids))\
                            .distinct().all()
    unique_students_count = len(student_ids)

    # Średni wynik wszystkich quizów
    all_scores = []
    for sq in StudentQuiz.query.filter(StudentQuiz.quiz_id.in_(quiz_ids)).all():
        total_questions = len(sq.quiz.questions)
        if total_questions == 0:
            continue
        correct = sum(
            1 for q in sq.quiz.questions
            if next((a.id for a in q.answers if a.is_correct), None) ==
               next((sa.answer_id for sa in sq.student_answers if sa.question_id == q.id), None)
        )
        score_percent = (correct / total_questions) * 100
        all_scores.append(score_percent)

    average_score = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0

    # Ostatni quiz
    last_quiz = max(quizzes, key=lambda q: q.created_at)
    last_quiz_info = {"title": last_quiz.title, "created_at": last_quiz.created_at}

    return unique_students_count, average_score, last_quiz_info