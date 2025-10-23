-- Dodanie przykładowych użytkowników (Nauczycieli i Uczniów)
-- ID zostanie nadane automatycznie przez bazę danych.
-- !!Dodać hashowanie haseł po produkcji! 
INSERT INTO users (username, email, password, role)
VALUES
('admin', 'admin@quizapp.local', 'admin', 'teacher'),  
('nauczyciel', 'nauczyciel@test.com', 'nauczyciel', 'teacher'),
('janek', 'janek@student.com', 'janek', 'student'),    
('ania', 'anna@student.com', 'ania', 'student'),  
('piotr', 'piotr@student.com', 'piotr', 'student');    