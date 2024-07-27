SELECT name
FROM subjects
WHERE id IN (SELECT subject_id FROM grades WHERE student_id = ?);
