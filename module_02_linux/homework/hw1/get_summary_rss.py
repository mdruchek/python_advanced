"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""


def get_summary_rss(ps_output_file_path: str) -> str:
    with open(ps_output_file_path, 'r') as file:
        lines = file.readlines()[1:]
    summary_rss: int = 0
    for line in lines:
        columns: list = line.split()
        summary_rss += int(columns[5])
    number_digits = len(str(summary_rss))
    for degree, dimension in ((6, 'ГБ'), (3, 'МБ'), (0, 'кБ')):
        if number_digits > degree:
            return f'{summary_rss / 10 ** degree} {dimension}'


if __name__ == '__main__':
    path: str = 'output_file.txt'
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)