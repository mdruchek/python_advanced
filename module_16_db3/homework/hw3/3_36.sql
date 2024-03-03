SELECT c.class
FROM Classes c
JOIN Ships s ON c.class = s.name
UNION
SELECT c.class
FROM Classes c
JOIN Outcomes o ON c.class = o.Ship