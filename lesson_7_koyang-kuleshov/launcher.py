"""Запускает сервер и 1 клиентa по умолчанию"""

import argparse
import subprocess
from time import sleep
from sys import platform
from common.variables import MAX_CONNECTIONS


process = list()
number_of_client = argparse.ArgumentParser('Считывает количество клиентов \
                                           для запуска')
number_of_client.add_argument(
    '-n',
    type=int, default=MAX_CONNECTIONS,
    help='Введите количество клиентов для запуска -n=2, по умолчанию 6'
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
                f'python server.py',
                creationflags=subprocess.CREATE_NEW_CONSOLE)
            )
            for i in range(n // 3):
                name = 'Guest'+str(i + 1)
                process.append(subprocess.Popen(
                    f'python client.py -mode=send -name={name}',
                    creationflags=subprocess.CREATE_NEW_CONSOLE)
                )
            for i in range(n // 3):
                process.append(subprocess.Popen(
                    'python client.py -mode=listen',
                    creationflags=subprocess.CREATE_NEW_CONSOLE)
                )
        else:
            process.append(subprocess.Popen(
                f'xterm -e python server.py', stdout=subprocess.PIPE,
                stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True))
            sleep(1)
            for i in range(n // 3):
                name = 'Guest'+str(i + 1)
                process.append(subprocess.Popen(
                    f'xterm -e python client.py -mode=send -name={name}',
                    stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                    stderr=subprocess.STDOUT, shell=True)
                )
                sleep(1)
            for i in range(n // 3):
                process.append(subprocess.Popen(
                    'xterm -e python client.py -mode=listen',
                    stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                    stderr=subprocess.STDOUT, shell=True)
                )
                sleep(1)
    elif action == 'x' or action == 'х':
        while process:
            victim = process.pop()
            victim.kill()
