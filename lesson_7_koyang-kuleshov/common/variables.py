"""Константы"""
from logging import DEBUG

DEFAULT_PORT = 7777
DEFAULT_IP_ADDRES = '127.0.0.1'
MAX_CONNECTIONS = 2
MAX_PACKAGE_LENGTH = 1024
ENCODING = 'UTF-8'
LOGGING_LEVEL = DEBUG


# JIM protocol

ACTION = 'action'
TO = 'to'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
MESSAGE = 'message'

PRESENCE = 'presence'
MSG = 'msg'
SENDER = 'sender'
QUIT = 'quit'
AUTHENTICATE = 'authenticate'
JOIN = 'join'
LEAVE = 'leave'
RESPONSE = 'response'
ERROR = 'error'
