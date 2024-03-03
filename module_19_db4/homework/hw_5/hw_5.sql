-- общий
SELECT
    group_id,
    COUNT(`student_id`) count_students,
    (SELECT
        ROUND(AVG(ag2.`grade`),2)
        FROM `students` s2
        JOIN `assignments_grades` ag2 ON ag2.`student_id` = s2.`student_id`
        GROUP BY s2.`group_id`
        HAVING s2.`group_id` = s1.group_id) avg_grade,
    (SELECT
        COUNT(student_id)
        FROM (SELECT DISTINCT s3.student_id, s3.group_id
                FROM students s3
                JOIN assignments a3 ON s3.group_id = a3.group_id
                LEFT JOIN assignments_grades ag3 ON (ag3.student_id = s3.student_id AND ag3.assisgnment_id = a3.assisgnment_id)
                WHERE ag3.grade_id IS NULL)
        GROUP BY group_id
        HAVING group_id = s1.group_id) count_not_passed,
    (SELECT COUNT(*)
        FROM (SELECT DISTINCT s.student_id, s.group_id
                FROM assignments a
                JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
                JOIN students s ON s.student_id = ag.student_id
                WHERE
                    ag.date > a.due_date)
        WHERE group_id = s1.group_id) count_overdue,
    (SELECT SUM(count_submission)
        FROM(
            SELECT ag4.student_id, COUNT(ag4.assisgnment_id) count_submission, s4.group_id
            FROM assignments_grades ag4
            JOIN students s4 ON s4.student_id = ag4.student_id
            WHERE group_id = s1.group_id
            GROUP BY ag4.assisgnment_id, ag4.student_id
            HAVING COUNT(*) > 1)) count_submission
FROM `students` s1
GROUP BY `group_id`