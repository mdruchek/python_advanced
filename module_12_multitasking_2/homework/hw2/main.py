import subprocess
import shlex
import getpass


def process_count(username: str) -> int:
    # количество процессов, запущенных из-под
    # текущего пользователя username
    res = subprocess.run(f'ps -U {username} --no-headers | wc -l', shell=True, capture_output=True).stdout
    return int(res)


def total_memory_usage(root_pid: int) -> float:
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах
    command = shlex.split(f'ps --ppid {root_pid} -o pmem=')
    res = subprocess.run(command, capture_output=True).stdout
    return round(sum(map(float, res.decode().split())), 1)


if __name__ == '__main__':
    print(process_count(getpass.getuser()))
    print(total_memory_usage(1241))
