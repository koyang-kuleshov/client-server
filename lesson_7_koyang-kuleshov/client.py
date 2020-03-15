"""
сформировать presence-сообщение;
отправить сообщение серверу;
получить ответ сервера;
разобрать сообщение сервера;
параметры командной строки скрипта client.py <addr> [<port>]:
addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777."""


import argparse
import logging
from socket import socket, AF_INET, SOCK_STREAM
from time import time
import sys
from datetime import datetime

from common.utils import send_message, get_message
from common.variables import PRESENCE, DEFAULT_IP_ADDRES, DEFAULT_PORT, \
    USER, ACCOUNT_NAME, TIME, RESPONSE, ERROR, ACTION, TO, MSG, MESSAGE, SENDER
from decorators import Log


CLIENT_LOG = logging.getLogger('client.log')


def parse_comm_line():
    pars_str = argparse.ArgumentParser('Считывает данные для подключения \
клиента')
    pars_str.add_argument('-mode', type=str, help='Считывает режим работы \
клиента')
    pars_str.add_argument(
        '-a',
        type=str,
        help='IP-адрес сервера, по умолчанию 127.0.0.1'
    )
    pars_str.add_argument('-port', type=int, help='Порт сервера, по \
умолчанию 7777')
    pars_str.add_argument('-name', type=str, help='Получает имя клиента')
    CLIENT_LOG.info('Разбираются параметры командой строки при вызове')
    port = pars_str.parse_args().port
    account_n = pars_str.parse_args().name
    addr = pars_str.parse_args().a
    mode = pars_str.parse_args().mode
    if port is None:
        CLIENT_LOG.info('Порт задан не верно')
        port = DEFAULT_PORT
    elif port < 1024 or port > 65535 or port:
        CLIENT_LOG.info('Порт задан не верно. Устанавливается порт 7777.')
        port = DEFAULT_PORT
    if addr is None:
        CLIENT_LOG.info('Устанавливается IP-адрес по умолчанию.')
        addr = DEFAULT_IP_ADDRES
    if mode is None:
        CLIENT_LOG.info('Устанавливается режим на прослушивание.')
        mode = 'listen'
    elif mode not in {'send', 'listen'}:
        CLIENT_LOG.info('Задан не правильный режим. Устанавливается режим на \
прослушивание')
        mode = 'listen'

    if account_n is None:
        CLIENT_LOG.info('Устанавливается имя по умолчанию "Guest".')
        account_n = 'Guest'
    return addr, port, mode, account_n


@Log()
def create_presence(account_n):
    """Создание запроса о присутствии клиента на сервере"""
    CLIENT_LOG.debug('Создание запроса о присутствии клиента на сервере')
    out = {
        ACTION: PRESENCE,
        TO: '',
        TIME: time(),
        USER: {
            ACCOUNT_NAME: account_n
        }
    }
    return out


@Log()
def get_user_answer(message):
    """Обрабатка сообщения сервера"""
    CLIENT_LOG.debug('Обрабатка сообщения сервера')
    if ACTION in message and message[ACTION] == MSG:
        time_mess = datetime.fromtimestamp(message[TIME]).strftime("%H:%M:%S")
        user_msg = f'[{time_mess}] \
{message[SENDER]}: {message[MESSAGE]}'
        print(f'{user_msg}')
        CLIENT_LOG.info(f'{user_msg}')
    else:
        CLIENT_LOG.debug(f'Некорректное сообщение от сервера: {message}')


@Log()
def create_message(sock, account_n):
    CLIENT_LOG.info('Создание сообщения пользователя')
    print(f'Имя пользователя: {account_n}')
    message = input('Введите сообщение( для выхода введите !!!): ')
    if message == '!!!':
        sock.close()
        CLIENT_LOG.info('Завершение работы по команде пользователя')
        sys.exit(1)
    out = {
        ACTION: MSG,
        TO: '',
        TIME: time(),
        USER: {
            ACCOUNT_NAME: account_n
        },
        MESSAGE: message
    }
    CLIENT_LOG.info('Сформировано сообщение')
    return out


def client_main():
    ADDRES, PORT, MODE, account_name = parse_comm_line()
    if MODE == 'listen':
        print('Режим работы: приём сообщений')
    else:
        print('Режим работы: отправка сообщений')

    CLIENT = socket(AF_INET, SOCK_STREAM)
    CLIENT.connect((ADDRES, PORT))
    while True:
        if MODE == 'send':
            try:
                send_message(CLIENT, create_message(CLIENT, account_name))
            except (ConnectionResetError, ConnectionError,
                    ConnectionAbortedError):
                CLIENT_LOG.error(f'Соединение с сервером {ADDRES} было \
потеряно')
                print('Не удалось декодировать сообщение от сервера')
                sys.exit(1)
        else:
            try:
                get_user_answer(get_message(CLIENT))
            except (ConnectionResetError, ConnectionError,
                    ConnectionAbortedError):
                CLIENT_LOG.error(f'Соединение с сервером {ADDRES} было \
потеряно')
                print('Не удалось декодировать сообщение от сервера')
                sys.exit(1)


if __name__ == '__main__':
    client_main()
