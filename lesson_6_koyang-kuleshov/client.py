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
import logging
import logs.client_log_config
from unit_tests.decorators import Log


CLIENT_LOG = logging.getLogger('client.log')


class ArgumentParserError(Exception):
    CLIENT_LOG.info('Не указан обязательный параметр')
    print('Не указан обязательный параметр')


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


@Log()
def create_presence(account_n):
    """Создание запроса о присутствии клиента на сервере"""
    CLIENT_LOG.debug('Создание запроса о присутствии клиента на сервере')
    out = {
        ACTION: PRESENCE,
        TIME: time(),
        USER: {
            ACCOUNT_NAME: account_n
        }
    }
    return out


@Log()
def process_answer(message):
    """Обрабатка сообщения сервера"""
    CLIENT_LOG.debug('Обрабатка сообщения сервера')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            CLIENT_LOG.info(f'Получен ответ от сервера {message}')
            return '200 : OK'
        CLIENT_LOG.error(f'Получен ответ от сервера {message}')
        return f'400 : {message[ERROR]}'
    CLIENT_LOG.critical(f'Некорректный ответ сервера {ValueError}')
    raise ValueError


def client_main():
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
        CLIENT_LOG.debug('Разбираются параметры командой строки при вызове')
        ADDRES = pars_str.parse_args().addr
        PORT = pars_str.parse_args().port
        if PORT < 1024 or PORT > 65535 or not isinstance(PORT, int):
            CLIENT_LOG.info('Порт задан не верно')
            raise ValueError
    except ValueError:
        print('Номер порта должен быть в диапазоне от 1024 до 65535')
    except ArgumentParserError:
        print('Вы не указали IP-адрес, будет использован по умолчанию')
        CLIENT_LOG.debug('Устанавливаются параметры соединения по умолчанию')
        ADDRES = DEFAULT_IP_ADDRES
        PORT = DEFAULT_PORT

    CLIENT = socket(AF_INET, SOCK_STREAM)
    CLIENT.connect((ADDRES, PORT))

    account_name = input('Введите имя пользователя для подключения\
( Enter - имя по умолчанию): ')
    if account_name == '':
        account_name = 'Guest'
    CLIENT_LOG.info(f'Имя пользователя: {account_name}')
    message_to_server = create_presence(account_name)
    send_message(CLIENT, message_to_server)
    try:
        server_answer = process_answer(get_message(CLIENT))
        print(f'Ответ сервера - {server_answer}')
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение от сервера')


if __name__ == '__main__':
    client_main()
