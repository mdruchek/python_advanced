"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field, ValidationError


def number_length(min: int = -1, max: int = -1, message: Optional[str] = None):
    if not message:
        message = 'Длина должна быть от %d до %d символов.' % (min, max)

    def _number_length(form: FlaskForm, field: Field):
        _len = field.data and len(str(field.data)) or 0
        if _len < min or max != -1 and _len > max:
            raise ValidationError(message)
    return _number_length


class NumberLength:
    def __init__(self, min: int = -1, max: int = -1, message: Optional[str] = None):
        self.min = min
        self.max = max
        if not message:
            message = 'Длина должна быть от %d до %d символов.' % (min, max)
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        _len = field.data and len(str(field.data)) or 0
        if _len < self.min or self.max != -1 and _len > self.max:
            raise ValidationError(self.message)
