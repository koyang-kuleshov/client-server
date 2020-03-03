"""
сформировать presence-сообщение;
отправить сообщение серверу;
получить ответ сервера;
разобрать сообщение сервера;
параметры командной строки скрипта client.py <addr> [<port>]:
addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777."""


import argparse
import json
from time import time
from socket import socket, AF_INET, SOCK_STREAM
from common.variables import PRESENCE, DEFAULT_IP_ADDRES, DEFAULT_PORT, \
    USER, ACCOUNT_NAME, TIME, RESPONSE, ERROR, ACTION
from common.utils import get_message, send_message


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


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


def process_answer(message):
    """Обрабатывает сообщения сервера"""
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    pars_str = ThrowingArgumentParser('Считывает данные для подключения \
клиента')
    pars_str.add_argument(
        'addr',
        type=str,
        help='IP-адрес сервера, по умолчанию 127.0.0.1'
    )
    pars_str.add_argument('-port', type=int, help='Порт сервера, по умолчанию \
        7777')
    try:
        ADDRES = pars_str.parse_args().addr
        PORT = pars_str.parse_args().port
        if PORT < 1024 or PORT > 65535 or not isinstance(PORT, int):
            raise ValueError
    except ValueError:
        print('Номер порта должен быть в диапазоне от 1024 до 65535')
    except ArgumentParserError:
        print('Вы не указали IP-адрес, будет использован по умолчанию')
        ADDRES = DEFAULT_IP_ADDRES
        PORT = DEFAULT_PORT

    CLIENT = socket(AF_INET, SOCK_STREAM)
    CLIENT.connect((ADDRES, PORT))

    account_name = input('Введите имя пользователя для подключения\
( Enter - имя по умолчанию): ')
    if account_name == '':
        account_name = 'Guest'
    message_to_server = create_presence(account_name)
    send_message(CLIENT, message_to_server)
    try:
        server_answer = process_answer(get_message(CLIENT))
        print(f'Ответ сервера - {server_answer}')
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение от сервера')


if __name__ == '__main__':
    main()
