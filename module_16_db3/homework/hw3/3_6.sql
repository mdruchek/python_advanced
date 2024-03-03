SELECT DISTINCT p.maker, l.speed
FROM laptop l
JOIN product p ON l.model = p.model
WHERE l.hd >= 10