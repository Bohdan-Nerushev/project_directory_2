SELECT AVG(grades.grade) as avg_grade
FROM grades
JOIN subjects ON grades.subject_id = subjects.id
WHERE subjects.teacher_id = ?;

