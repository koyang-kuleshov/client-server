"""Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
результаты"""
import subprocess
from chardet import detect


NUMBER_ATTEMPTS = 5
ARGS = ['youtube.com', 'yandex.ru']
for site in ARGS:
    params = ['ping', site]
    SUBPROC_PING = subprocess.Popen(params, stdout=subprocess.PIPE)
    for counter, line in enumerate(SUBPROC_PING.stdout):
        encode_param = detect(line)
        if counter != 0:
            line = f'Попытка №{counter} {line.decode(encode_param["encoding"])}'
            print(line)
        else:
            print(line.decode(encode_param["encoding"]))
        if counter > NUMBER_ATTEMPTS:
            break
