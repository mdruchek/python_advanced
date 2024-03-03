## Типы связей между таблицами в схеме

![](../img/cinema_schema_diagram.png)

|  Тип связи   | Таблица 1       | Таблица 2 |
|:------------:|-----------------|-----------|
| many to many | actors          | movie     |
| one to many  | movie_cast      | actors    |
| one to many  | movie_cast      | movie     |
| one to many  | oscar_awarded   | movie     |
| many to many | director        | movie     |
| one to many  | movie_direction | movie     |
| one to many  | movie_direction | director  |
