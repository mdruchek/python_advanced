SELECT s.`full_name`
FROM `assignments_grades` ag
JOIN `students` s ON ag.`student_id` = s.`student_id`
GROUP BY s.`full_name`
ORDER BY ROUND(AVG(ag.`grade`), 2) DESC, COUNT(ag.`grade`) DESC
LIMIT 10