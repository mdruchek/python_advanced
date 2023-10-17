import subprocess
from subprocess import PIPE, TimeoutExpired


def sleep_exit():
    proc = subprocess.Popen(
        'sleep 10 && exit 1',
        shell=True,
        stdout=PIPE,
        stderr=PIPE
    )

    print('Запущен процесс {}'.format(proc.pid))
    try:
        proc.wait(timeout=9)
    except TimeoutExpired:
        print('Прошло 9сек, процесс не завершён')
    proc.wait()
    print('Завершён процесс {pid} со статусом {code}'.format(pid=proc.pid, code=proc.returncode))


if __name__ == '__main__':
    sleep_exit()
