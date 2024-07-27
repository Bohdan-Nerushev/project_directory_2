SELECT students.name, grades.grade
FROM grades
JOIN students ON grades.student_id = students.id
JOIN groups ON students.group_id = groups.id
WHERE groups.id = ? AND grades.subject_id = ?;

