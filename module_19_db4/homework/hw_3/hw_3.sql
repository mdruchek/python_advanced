SELECT `full_name`
FROM `students`
WHERE `group_id` in (
            SELECT `group_id`
            FROM `students_groups`
            WHERE `teacher_id` = (
                        SELECT a.`teacher_id`
                        FROM `assignments_grades` ag
                        JOIN `assignments` a ON a.`assisgnment_id` = ag.`assisgnment_id`
                        GROUP BY a.`teacher_id`
                        ORDER BY ROUND(AVG(ag.`grade`), 2) DESC
                        LIMIT 1
                    )
        )