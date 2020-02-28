"""Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить кодировку файла
по умолчанию. Принудительно открыть файл в формате Unicode и вывести его
содержимое"""
STRINGS = ['сетевое программирование', 'сокет', 'декоратор']
with open('test.txt', 'w') as f_write:
    for string in STRINGS:
        f_write.writelines(f'{ string }\n')
enc = f_write.encoding
print(f'Кодировка файла: {enc}')
try:
    with open('test.txt', encoding='UTF-8') as f_read:
        for spam in f_read.readlines():
            print(spam, end='')
except UnicodeDecodeError:
    with open('test.txt') as f_read:
        enc = f_read.encoding
        for spam in f_read.readlines():
            print(spam.encode(enc).UTF('UTF-8'), end='')
