def calculate_quiz_score(student_quiz):
    total_questions = len(student_quiz.quiz.questions)
    if total_questions == 0:
        return 0

    correct = 0
    for q in student_quiz.quiz.questions:
        correct_answer = next((a.id for a in q.answers if a.is_correct), None)
        chosen = next(
            (sa.answer_id for sa in student_quiz.student_answers if sa.question_id == q.id),
            None
        )
        if correct_answer and chosen == correct_answer:
            correct += 1

    return round((correct / total_questions) * 100, 2)