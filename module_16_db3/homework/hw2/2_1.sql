SELECT
    c.`full_name` AS 'customer',
    m.`full_name` AS 'manager',
    o.`purchase_amount`,
    o.`date`
FROM
    `order` o
JOIN `customer` c ON c.`customer_id` = o.`customer_id`
JOIN `manager` m ON m.`manager_id` = o.`manager_id`