"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""
import sys
from types import TracebackType
from typing import Type, Literal, IO


class Redirect:
    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        self.stdout = stdout
        self.stderr = stderr

        if self.stderr:
            self.old_stderr = sys.stderr
            sys.stderr = self.stderr

    def __enter__(self):
        if self.stdout:
            self.old_stdout = sys.stdout
            sys.stdout = self.stdout

        if self.stderr:
            self.old_stderr = sys.stderr
            sys.stderr = self.stderr

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:

        if self.stdout:
            sys.stdout = self.old_stdout
        if self.stderr:
            sys.stderr = self.old_stderr
