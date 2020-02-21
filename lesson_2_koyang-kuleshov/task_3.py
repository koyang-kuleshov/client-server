"""Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
Для этого:
a) Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный словарь,
где значение каждого ключа — это целое число с юникод-символом, отсутствующим в
кодировке ASCII (например, €);
b) Реализовать сохранение данных в файл формата YAML — например, в файл
file.yaml. При этом обеспечить стилизацию файла с помощью параметра
default_flow_style, а также установить возможность работы с юникодом:
allow_unicode = True;
c) Реализовать считывание данных из созданного файла и проверить, совпадают ли
они с исходными"""
import yaml


def get_yaml():
    """Функция создаёт словарь для записи в файл"""
    list_to_dict = [['list_data_1', 'list_data_2'], 3,
                    {'key_1': 'data_1', 'key_2': 'data_2'}]
    yaml_dict = dict()
    for counter, item in enumerate(list_to_dict):
        yaml_dict[f'{counter}€'] = item
    return yaml_dict


def write_yaml(file_n):
    """Функция записывет файл в формате yaml"""
    with open(file_n, 'w') as f_write:
        yaml.dump(get_yaml(), f_write, default_flow_style=False,
                  allow_unicode=True)


def read_yaml(file_n):
    """Функция выводит содержимое файла в формате yaml"""
    with open(file_n, 'r') as f_read:
        print(f_read.read())


FILE_NAME = 'file.yaml'
write_yaml(FILE_NAME)
read_yaml(FILE_NAME)
