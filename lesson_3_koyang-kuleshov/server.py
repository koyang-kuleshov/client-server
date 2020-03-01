"""принимает сообщение клиента;
формирует ответ клиенту;
отправляет ответ клиенту;
имеет параметры командной строки:
-p <port> — TCP-порт для работы (по умолчанию использует 7777);
-a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные
адреса)."""


import json
import argparse
import datetime
from socket import socket, AF_INET, SOCK_STREAM
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRES, MAX_CONNECTIONS,\
    ACTION, PRESENCE, TIME, USER, RESPONSE, ERROR, ACCOUNT_NAME
from common.utils import get_message, send_message


def do_answer(message):
    """Обрабатывает сообщение от клиента и готовит ответ"""
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message:
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    """Запускает сервер"""
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
        ADDRES = pars_str.parse_args().a
        PORT = pars_str.parse_args().p
        CONNECTIONS = pars_str.parse_args().u
        if PORT < 1024 or PORT > 65535 or not isinstance(PORT, int):
            raise ValueError
    except ValueError:
        print('Номер порта должен быть в диапазоне от 1024 до 65535')

    SERV = socket(AF_INET, SOCK_STREAM)
    SERV.bind((ADDRES, PORT))
    SERV.listen(CONNECTIONS)
    while True:
        client, addr = SERV.accept()
        try:
            client_message = get_message(client)
            response = do_answer(client_message)
            send_message(client, response)
            client.close()
            spam_time = datetime.datetime.fromtimestamp(
                client_message[TIME])
            print(f'{spam_time.strftime("%H:%M:%S")}\
 : Пользователь {client_message[USER][ACCOUNT_NAME]} подключился')
        except (ValueError, json.JSONDecodeError):
            print('Принято некорректное сообщение от клиента')
            client.close()


if __name__ == '__main__':
    main()
