import subprocess
import sys


def run_program():
    res = subprocess.run(['python', 'test_program.py'], input=b'some input\notherinput', stdout=sys.stderr)
    print(res, file=sys.stderr)


if __name__ == '__main__':
    run_program()
