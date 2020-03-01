"""принимает сообщение клиента;
формирует ответ клиенту;
отправляет ответ клиенту;
имеет параметры командной строки:
-p <port> — TCP-порт для работы (по умолчанию использует 7777);
-a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные
адреса)."""


import argparse
from time import time
from socket import socket, AF_INET, SOCK_STREAM
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRES, MAX_CONNECTIONS
from common.utils import get_message, send_message


pars_str = argparse.ArgumentParser('Считывает TCP-порт и IP-адрес')
pars_str.add_argument('-a', type=str, default=DEFAULT_IP_ADDRES,
                      help='IP-адрес')
pars_str.add_argument('-p', type=int, default=DEFAULT_PORT, help='TCP-порт')
pars_str.add_argument('-u', type=int, default=MAX_CONNECTIONS,
                      help='Количество пользователей на сервере')
ADDRES = pars_str.parse_args().a
PORT = pars_str.parse_args().p
USERS = pars_str.parse_args().u

SERV = socket(AF_INET, SOCK_STREAM)
SERV.bind(('', PORT))
SERV.listen(USERS)
while True:
    client, addr = SERV.accept()

print(f'\nСервер запущен на {PORT} порту, количество пользователей {USERS}')
