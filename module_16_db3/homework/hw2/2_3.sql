SELECT
    o.`order_no`,
    m.`full_name` AS 'manager',
    c.`full_name` AS 'customer'
FROM
    `order` o
JOIN `customer` c ON c.`customer_id` = o.`customer_id`
JOIN `manager` m ON m.`manager_id` = o.`manager_id`
WHERE m.`city` != c.`city`;