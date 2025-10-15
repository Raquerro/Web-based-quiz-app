from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


# --- USERS ---
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # teacher lub student
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacje
    quizzes = db.relationship("Quiz", back_populates="teacher", cascade="all, delete-orphan")
    student_quizzes = db.relationship("StudentQuiz", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


# --- QUIZZES ---
class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacje
    teacher = db.relationship("User", back_populates="quizzes")
    questions = db.relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    student_quizzes = db.relationship("StudentQuiz", back_populates="quiz", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Quiz {self.title}>"


# --- QUESTIONS ---
class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default="single")  # single/multiple

    # Relacje
    quiz = db.relationship("Quiz", back_populates="questions")
    answers = db.relationship("Answer", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Question {self.id} ({self.question_type})>"


# --- ANSWERS ---
class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    # Relacje
    question = db.relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"<Answer {self.id} {'✔' if self.is_correct else '✘'}>"


# --- STUDENT_QUIZZES ---
class StudentQuiz(db.Model):
    __tablename__ = "student_quizzes"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False)
    started_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime)

    # Relacje
    student = db.relationship("User", back_populates="student_quizzes")
    quiz = db.relationship("Quiz", back_populates="student_quizzes")
    student_answers = db.relationship("StudentAnswer", back_populates="student_quiz", cascade="all, delete-orphan")

    # Unikalny indeks (student_id + quiz_id)
    __table_args__ = (db.UniqueConstraint("student_id", "quiz_id", name="uix_student_quiz"),)

    def __repr__(self):
        return f"<StudentQuiz student={self.student_id} quiz={self.quiz_id}>"


# --- STUDENT_ANSWERS ---
class StudentAnswer(db.Model):
    __tablename__ = "student_answers"

    id = db.Column(db.Integer, primary_key=True)
    student_quiz_id = db.Column(db.Integer, db.ForeignKey("student_quizzes.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey("answers.id"))
    is_selected = db.Column(db.Boolean, default=True)

    # Relacje
    student_quiz = db.relationship("StudentQuiz", back_populates="student_answers")
    question = db.relationship("Question")
    answer = db.relationship("Answer")

    def __repr__(self):
        return f"<StudentAnswer quiz={self.student_quiz_id} q={self.question_id}>"
