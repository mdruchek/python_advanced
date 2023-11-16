### Ответ на вопрос 1: синий

#### Решение:
sql запрос:
```sqlite-sql
select
    phones.colour `цвет`,
    count(phones.id) `кол-во` 
from table_checkout as checkout
join table_phones as phones ON checkout.phone_id = phones.id
group by phones.colour
order by `кол-во` desc limit 1
```
ответ:

| цвет                          | кол-во |
|-------------------------------|--------|
|синий|500|


### Ответ на вопрос 2: синий
#### Решение:
sql запрос:
```sqlite-sql
select
    phones.colour `цвет`,
    count(*) `кол-во` 
from table_checkout as checkout
join table_phones as phones ON checkout.phone_id = phones.id
where colour = 'синий' or colour = 'красный'
group by phones.colour
```

ответ:

| цвет                          | кол-во |
|-------------------------------|--------|
|синий|500|
|красный|429|


### Ответ на вопрос 3: золотой

#### Решение:
sql запрос:
```sqlite-sql
select
    phones.colour `цвет`,
    count(phones.id) `кол-во` 
from table_checkout as checkout
join table_phones as phones ON checkout.phone_id = phones.id
group by phones.colour
order by `кол-во` limit 1
```
ответ:

| цвет    | кол-во |
|---------|--------|
| золотой | 28     |