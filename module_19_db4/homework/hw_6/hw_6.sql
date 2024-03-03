SELECT ROUND(AVG(`grade`), 2) avg_grade
FROM `assignments_grades`
WHERE `assisgnment_id` IN (
            SELECT `assisgnment_id`
            FROM `assignments`
            WHERE `assignment_text` LIKE 'прочитать%' OR `assignment_text` LIKE 'выучить%'
       )

