"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""
import sys
import traceback
from types import TracebackType
from typing import Type, Literal, IO
from io import IOBase


class Redirect:
    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.old_stdout = None
        self.old_stderr = None

    def __enter__(self):
        if isinstance(self.stdout, IOBase):
            self.old_stdout = sys.stdout
            sys.stdout = self.stdout

        if isinstance(self.stderr, IOBase):
            self.old_stderr = sys.stderr
            sys.stderr = self.stderr
        return self

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:

        if isinstance(self.stdout, IOBase):
            sys.stdout = self.old_stdout
        if isinstance(self.stderr, IOBase):
            sys.stderr.write(traceback.format_exc())
            sys.stderr = self.old_stderr
            return True
