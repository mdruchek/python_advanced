SELECT DISTINCT p.maker
FROM product p
JOIN pc ON pc.model = p.model
WHERE speed >= 450