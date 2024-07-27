SELECT s.name, g.grade
FROM grades g
JOIN students s ON s.id = g.student_id
WHERE s.group_id = ? AND g.subject_id = ?
ORDER BY g.date_received DESC
LIMIT 1;
