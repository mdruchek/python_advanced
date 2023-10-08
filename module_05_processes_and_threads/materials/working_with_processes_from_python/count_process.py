import subprocess
import sys


def count_process():
    processes = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE, text=True).stdout.read()
    count_process = len(processes.split('\n')) - 1
    print(count_process)


if __name__ == '__main__':
    count_process()
