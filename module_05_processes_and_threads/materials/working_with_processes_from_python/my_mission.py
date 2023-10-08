import shlex
import subprocess


def my_mission():
    command = shlex.split('sleep 15 && echo "My mission is done here!"')
    proc = subprocess.Popen('sleep 15; echo "My mission is done here!"',
                            shell=True, stdout=subprocess.PIPE, text=True).stdout.read()


if __name__ == '__main__':
    my_mission()
