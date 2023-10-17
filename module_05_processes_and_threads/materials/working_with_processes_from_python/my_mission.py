from subprocess import PIPE
import subprocess
from time import time


def my_mission():
    start = time()
    process = []
    for _ in range(1, 11):

        proc = subprocess.Popen(
            "sleep 15 && echo 'My mission is done here!'",
            shell=True,
            stdout=PIPE,
            stderr=PIPE
        )

        print('Запущен процесс {}.'.format(proc.pid))
        process.append(proc)

    for proc in process:
        proc.wait()
        if b'My miss' in proc.stdout.read() and proc.returncode == 0:
            print('Процесс {} выполнен успешно.'.format(proc.pid))

    print('Время выполнения: {}'.format(time() - start))



if __name__ == '__main__':
    my_mission()
