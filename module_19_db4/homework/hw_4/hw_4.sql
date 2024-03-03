SELECT ROUND(AVG(cnt), 3) avg_count, MIN(cnt) min_count, MAX(cnt) max_count
FROM (SELECT COUNT(a.group_id) cnt
        FROM `assignments_grades` ag
        JOIN `assignments` a ON a.`assisgnment_id` = ag.`assisgnment_id`
        WHERE ag.`date` > a.`due_date`
        GROUP BY group_id)
