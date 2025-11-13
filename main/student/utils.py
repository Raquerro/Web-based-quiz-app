def calculate_quiz_score(student_quiz):
    """Oblicza procentowy wynik całego quizu."""
    total_questions = len(student_quiz.quiz.questions)
    if total_questions == 0:
        return 0

    correct = sum(
        1 for q in student_quiz.quiz.questions
        if next((a.id for a in q.answers if a.is_correct), None) ==
           next((sa.answer_id for sa in student_quiz.student_answers if sa.question_id == q.id), None)
    )
    return round((correct / total_questions) * 100, 2)


def get_question_review(student_quiz, question_index):
    """Zwraca dane do review pojedynczego pytania."""
    question = student_quiz.quiz.questions[question_index]

    student_answer = next(
        (sa.answer for sa in student_quiz.student_answers if sa.question_id == question.id),
        None
    )
    correct_answer = next((a for a in question.answers if a.is_correct), None)
    is_correct = student_answer.id == correct_answer.id if student_answer and correct_answer else False

    return {
        "question": question,
        "student_answer": student_answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct
    }


def calculate_current_score(student_quiz, upto_index):
    """Oblicza bieżący wynik (liczba poprawnych odpowiedzi) do danego pytania."""
    correct_count = sum(
        1 for q in student_quiz.quiz.questions[:upto_index + 1]
        if next((sa.answer for sa in student_quiz.student_answers if sa.question_id == q.id), None) ==
           next((a for a in q.answers if a.is_correct), None)
    )
    return f"{correct_count}/{upto_index + 1}"
