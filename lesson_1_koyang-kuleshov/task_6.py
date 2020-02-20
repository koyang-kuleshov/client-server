#Создать текстовый файл test_file.txt, заполнить его тремя строками:
#«сетевое программирование», «сокет», «декоратор». Проверить кодировку файла
#по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое
STRINGS = ['сетевое программирование', 'сокет', 'декоратор']
with open('test.txt', 'w') as f_write:
    for string in STRINGS:
        f_write.writelines(f'{ string }\n')
print(f'Кодировка файла: { f_write.encoding }')
with open('test.txt', encoding='utf-8') as f_read:
    for spam in f_read.readlines():
        print(spam, end='')
