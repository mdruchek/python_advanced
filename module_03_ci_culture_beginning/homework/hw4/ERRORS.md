### Ошибки в файле person.py:

1. Импортировать модуль datetime:

        import datetime


2. Хорошая практика - давать значащие и развёрнутые имена переменным:

        def __init__(self, name: str, year_of_birth: int, address: str = '') -> None:
            self.name: str = name
            self.year_of_birth: int = year_of_birth
            self.address: str = address


3. Метод get_age() возвращает отрицательное число.
В расчете возраста, текущий год и год рождения нужно поменять местами.

        def get_age(self) -> int:
            now: datetime.datetime = datetime.datetime.now()
            return now.year - self.year_of_birth


4. В методе set_name() необходимо атрибут объекта name приравнять параметру метода name

        def set_name(self, name: str) -> None:
            self.name = name


5. В методе set_address() не верный оператор присваивания (правильно = а не ==)

        def set_address(self, address: str) -> None:
            self.address = address
 

8. В методе is_homeless() переменная address долна быть атрибутом экземпляра класса

       def is_homeless(self) -> bool:
           '''
           returns True if address is not set, false in other case
           '''
           return self.address is None
