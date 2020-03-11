"""Запускает сервер и 1 клиентa по умолчанию"""

import argparse
import subprocess
from sys import platform
from common.variables import DEFAULT_IP_ADDRES, DEFAULT_PORT, MAX_CONNECTIONS


process = list()
number_of_client = argparse.ArgumentParser('Считывает количество клиентов \
                                           для запуска')
number_of_client.add_argument(
    '-n',
    type=int, default=MAX_CONNECTIONS,
    help='Введите количество клиентов для запуска -n=3, по умолчанию 2'
)
n = number_of_client.parse_args().n
while True:
    action = input('q - выход\ns - запустить сервер и клиенты\n\
x - закрыть все окна\nВведите действие: ')
    if action == 'q':
        break
    elif action == 's':
        if platform != 'linux':
            process.append(subprocess.Popen(
                f'python server.py -a={DEFAULT_IP_ADDRES} -p={DEFAULT_PORT} \
                -u=n',
                creationflags=subprocess.CREATE_NEW_CONSOLE)
            )
            for i in range(n):
                name = 'Guest'+str(i + 1)
                process.append(subprocess.Popen(
                    f'python client.py -m -mode=send -name={name}',
                    creationflags=subprocess.CREATE_NEW_CONSOLE)
                )
            for i in range(n):
                process.append(subprocess.Popen(
                    'python client.py -m -mode=listen',
                    creationflags=subprocess.CREATE_NEW_CONSOLE)
                )
        else:
            process.append(subprocess.Popen(f'python server.py \
-a={DEFAULT_IP_ADDRES} -p={DEFAULT_PORT} -u=n', shell=True))
            for i in range(n):
                name = 'Guest'+str(i + 1)
                process.append(subprocess.Popen(
                    f'python client.py -m -mode=send -name={name}',
                    shell=True)
                )
            for i in range(n):
                process.append(subprocess.Popen(
                    'python client.py -m -mode=listen',
                    shell=True)
                )
    elif action == 'x' or action == 'х':
        while process:
            victim = process.pop()
            victim.kill()
