SELECT product.model, laptop.price
FROM product
JOIN laptop ON laptop.model = product.model
WHERE maker = 'B'
UNION
SELECT product.model, pc.price
FROM product
JOIN pc ON pc.model = product.model
WHERE maker = 'B'
UNION
SELECT product.model, printer.price
FROM product
JOIN printer ON printer.model = product.model
WHERE maker = 'B'