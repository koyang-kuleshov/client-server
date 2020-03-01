"""Константы"""

DEFAULT_PORT = 7777
DEFAULT_IP_ADDRES = '127.0.0.1'
MAX_CONNECTIONS = 1
MAX_PACKAGE_LENGTH = 1024
ENCODING = 'UTF-8'


# JIM protocol

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

PRESENCE = 'presence'
MSG = 'msg'
QUIT = 'quit'
AUTHENTICATE = 'authenticate'
JOIN = 'join'
LEAVE = 'leave'
RESPONSE = 'response'
ERROR = 'error'
