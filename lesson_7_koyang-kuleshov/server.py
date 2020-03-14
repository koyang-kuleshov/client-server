"""принимает сообщение клиента;
формирует ответ клиенту;
отправляет ответ клиенту;
имеет параметры командной строки:
-p <port> — TCP-порт для работы (по умолчанию использует 7777);
-a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные
адреса)."""


import argparse
import logging
from select import select
from socket import socket, AF_INET, SOCK_STREAM
from time import time
import sys

from common.utils import get_message, send_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRES, MAX_CONNECTIONS,\
    ACTION, PRESENCE, TIME, USER, RESPONSE, ERROR, TO, SENDER, MESSAGE, MSG, \
    ACCOUNT_NAME
from decorators import log


SERV_LOG = logging.getLogger('server.log')


def parse_comm_line():
    pars_str = argparse.ArgumentParser('Считывает TCP-порт и IP-адрес')
    pars_str.add_argument(
        '-a',
        type=str,
        default=DEFAULT_IP_ADDRES,
        help='IP-адрес'
    )
    pars_str.add_argument('-p', type=int, default=DEFAULT_PORT, help='Порт')
    pars_str.add_argument(
        '-u',
        type=int,
        default=MAX_CONNECTIONS,
        help='Количество пользователей на сервере'
    )
    try:
        SERV_LOG.debug('Разбираются параметры командой строки при вызове')
        addr = pars_str.parse_args().a
        port = pars_str.parse_args().p
        conn = pars_str.parse_args().u
        if port < 1024 or port > 65535 or not isinstance(port, int):
            SERV_LOG.info('Порт задан не верно')
            raise ValueError
    except ValueError:
        SERV_LOG.info('Порт задан по умолчанию')
        print('Номер порта должен быть в диапазоне от 1024 до 65535')
    return addr, port, conn


@log
def do_answer(message, message_list, client):
    """Обрабатывает сообщение от клиента и готовит ответ"""
    SERV_LOG.debug('Обработка сообщения от клиента и подготовка ответа')
    if ACTION in message and message[ACTION] == PRESENCE and TO in message \
            and TIME in message and USER in message:
        SERV_LOG.debug('Ответ подготовлен: {RESPONSE: 200}')
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MSG and TIME in message \
            and MESSAGE in message:
            # and MESSAGE in message and message[USER][ACCOUNT_NAME] in message:
        message_list.append((message[USER][ACCOUNT_NAME], message[MESSAGE]))
        SERV_LOG.debug(f'Ответ подготовлен: {message[USER][ACCOUNT_NAME]}, \
{message[MESSAGE]}')
        return
    else:
        SERV_LOG.debug("Ответ подготовлен: {RESPONSE: 400\nERROR: \
'Bad Request'}")
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


def server_main():
    """Запускает сервер"""
    SERV_LOG.debug('Запуск сервера')
    ADDRES, PORT, CONNECTIONS = parse_comm_line()
    SERV = socket(AF_INET, SOCK_STREAM)
    SERV.bind((ADDRES, PORT))
    SERV.listen(CONNECTIONS)
    SERV.settimeout(0.5)
    print(f'Сервер запущен {ADDRES}:{PORT}')
    clients = []
    messages = []
    while True:
        try:
            client, client_addr = SERV.accept()
        except OSError:
            pass
        else:
            SERV_LOG.info(f'Подключился клиент: {client_addr}')
            clients.append(client)

        read_clients_lst = []
        send_clients_lst = []
        err_lst = []
        try:
            if clients:
                read_clients_lst, send_clients_lst, err_lst = select(
                    clients, clients, [], 0)
        except OSError:
            pass
        if read_clients_lst:
            for client_with_message in read_clients_lst:
                try:
                    do_answer(
                        get_message(client_with_message),
                        messages, client_with_message)
                except:
                    SERV_LOG.info(
                        f'Клиент {client_with_message.getpeername()}'
                        f' отключился от сервера')
                    clients.remove(client_with_message)
                    sys.exit(1)
        if messages and send_clients_lst:
            message = {
                ACTION: MSG,
                SENDER: messages[0][0],
                TIME: time(),
                MESSAGE: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_clients_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    SERV_LOG.info(f'Клиент {waiting_client.getpeername()} \
отключился от сервера.')
                    clients.remove(waiting_client)
                    sys.exit(1)


if __name__ == '__main__':
    server_main()
