SELECT student_id, AVG(grade) as avg_grade
FROM grades
GROUP BY student_id
ORDER BY avg_grade DESC
LIMIT 5;
