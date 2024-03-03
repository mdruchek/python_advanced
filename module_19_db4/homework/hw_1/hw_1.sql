SELECT t.full_name
FROM `assignments_grades` ag
JOIN `assignments` a ON a.`assisgnment_id` = ag.`assisgnment_id`
JOIN `teachers` t ON t.`teacher_id` = a.`teacher_id`
GROUP BY t.`full_name`
ORDER BY ROUND(AVG(ag.`grade`), 2) ASC
LIMIT 1