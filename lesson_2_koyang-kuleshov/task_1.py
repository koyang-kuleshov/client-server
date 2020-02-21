"""Написать скрипт, осуществляющий
выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и
формирующий новый «отчетный» файл в формате CSV.
Для этого:
a) Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы»,  «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список для
хранения данных отчета — например, main_data — и поместить в него названия
столбцов отчета в виде списка: «Изготовитель системы», «Название ОС»,
«Код продукта», «Тип системы». Значения для этих столбцов также оформить в
виде списка и поместить в файл main_data (также для каждого файла);
b) Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;
c) Проверить работу программы через вызов функции write_to_csv()"""
import csv
import re


def get_data():
    os_prod_list = list()
    os_name_list = list()
    os_code_list = list()
    os_type_list = list()
    main_data = [HEADER]
    REGEX = [r'Изготовитель системы:\s+', r'Название ОС:\s+',
             r'Код продукта:\s+', r'Тип системы:\s+']
    for spam_file in FILES:
        with open(spam_file, 'rb') as tmp_f:
            for line in tmp_f.readlines():
                enc = 'cp1251'
                line = line.decode(enc)
                line = line.encode('utf-8').decode('utf-8')
                for counter, reg in enumerate(REGEX):
                    spam_str = re.search(reg, line)
                    if spam_str is not None and counter == 0:
                        spam_str = re.split(r'\W{2,}', line)
                        os_prod_list.append(spam_str[1])
                    if spam_str is not None and counter == 1:
                        spam_str = re.split(r'\W{2,}', line)
                        os_name_list.append(spam_str[1])
                    if spam_str is not None and counter == 2:
                        spam_str = re.split(r'\W{2,}', line)
                        os_code_list.append(spam_str[1])
                    if spam_str is not None and counter == 3:
                        spam_str = re.split(r'\W{2,}', line)
                        os_type_list.append(spam_str[1])
    for counter in range(len(os_prod_list)):
        tmp_list = [os_prod_list[counter], os_name_list[counter],
                    os_code_list[counter], os_type_list[counter]]
        main_data.append(tmp_list)
    return main_data


def write_to_csv(file_obj):
    with open(file_obj, 'w') as f_writer:
        f_writer = csv.writer(f_writer, quoting=csv.QUOTE_ALL)
        for row in get_data():
            f_writer.writerow(row)


HEADER = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]
FILES = ['info_1.txt', 'info_2.txt', 'info_3.txt']
write_to_csv('main_data.csv')
