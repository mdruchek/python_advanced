import subprocess
import shlex
import json
import re


def get_ip():
    command = shlex.split('curl -i -H "Accept: application/json" -X GET https://api.ipify.org?format=json')
    response = subprocess.run(command, stdout=subprocess.PIPE, text=True).stdout
    ip = re.search(r'\{"ip":\S*\}', response).group().split('"')[3]
    print(ip)

    return ip


if __name__ == '__main__':
    get_ip()