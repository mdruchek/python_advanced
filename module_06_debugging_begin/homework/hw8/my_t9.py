"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
import itertools
import re
from typing import List

keyboard = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz"
}


def my_t9(input_numbers: str) -> List[str]:
    with open("words", "r", encoding="utf-8") as file:
        dictionary = file.read()
    letters = [keyboard[key] for key in input_numbers]
    combinations = ["".join(list(combination)) for combination in itertools.product(*letters)]
    _words = list(filter(lambda x: x is not None,
                         [re.search(r"(\b" + comb + r")" + r"(\b)", dictionary)
                          for comb
                          in combinations]))
    return list(map(lambda x: x.group(1), _words))


if __name__ == '__main__':
    numbers: str = input()
    words: List[str] = my_t9(numbers)
    print(*words, sep='\n')
