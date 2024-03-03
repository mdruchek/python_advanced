import operator

from . import jsonrpc


@jsonrpc.method('logic.and')
def logic_and(A: bool, B: bool) -> bool:
    """
    Логическое И
    """
    return operator.and_(A, B)


@jsonrpc.method('logic.not')
def logic_not(A: bool) -> bool:
    """
    Логическое НЕ
    """
    return operator.not_(A)


@jsonrpc.method('logic.or')
def logic_or(A: bool, B: bool) -> bool:
    """
    Логическое ИЛИ
    """
    return operator.or_(A, B)


@jsonrpc.method('logic.xor)')
def logic_xor(A: bool, B: bool) -> bool:
    """
    Логическое ИСКЛЮЧАЮЩЕЕ ИЛИ
    """
    return operator.xor(A, B)


@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    """
    Арифметическое сложение
    """
    return operator.add(a, b)


@jsonrpc.method('calc.sub')
def sub(a: float, b: float) -> float:
    """
    Арифметическое вычитание
    """
    return operator.sub(a, b)


@jsonrpc.method('calc.mul')
def mul(a: float, b: float) -> float:
    """
    Арифметическое умножение
    """
    return operator.mul(a, b)


@jsonrpc.method('calc.truediv')
def truediv(a: float, b: float) -> float:
    """
    Арифметическое деление
    """
    return operator.truediv(a, b)
