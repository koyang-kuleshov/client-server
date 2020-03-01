"""
сформировать presence-сообщение;
отправить сообщение серверу;
получить ответ сервера;
разобрать сообщение сервера;
параметры командной строки скрипта client.py <addr> [<port>]:
addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777."""


import argparse
from time import time
from common.variables import ACTION, PRESENCE, DEFAULT_IP_ADDRES, DEFAULT_PORT\
    , USER, ACCOUNT_NAME, TIME, RESPONSE, ERROR
from socket import socket, AF_INET, SOCK_STREAM


def create_presence(account_n):
    """Создаёт запрос о присутствии клиента на сервере"""
    out = {
        ACTION: PRESENCE,
        TIME: time(),
        USER: {
            ACCOUNT_NAME: account_n
        }
    }
    return out


pars_str = argparse.ArgumentParser('Считывает данные для подключения клиента')
pars_str.add_argument('addr', type=str, default=DEFAULT_IP_ADDRES,
                      help='\
                      IP-адрес сервера, по умолчанию 127.0.0.1')
pars_str.add_argument('port', type=int, default=DEFAULT_PORT, help='\
                      Порт сервера, по умолчанию 7777')
args = pars_str.parse_args()

CLIENT = socket(AF_INET, SOCK_STREAM)
CLIENT.bind(args.addr, args.port)
CLIENT.listen(1)

while True:
    action = input('с - подкючиться к серверу\nd - отключиться от сервера\n\
q - выйти')
    if action == 'c' or action == 'с':
        account_name = input('Введите имя пользователя: ')
        if account_name == '':
            create_presence('Guest')
        else:
            create_presence(account_name)
    elif action == 'd':
        disconnect()
    elif action == 'q':
        break

print(args.addr, args.port, sep='\n')
