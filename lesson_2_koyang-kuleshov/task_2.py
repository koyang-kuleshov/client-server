"""Есть файл orders в формате JSON с информацией о заказах. Написать скрипт,
автоматизирующий его заполнение данными.
Для этого:
a) Создать функцию write_order_to_json(), в которую передается 5 параметров — товар
(item), количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
b) Проверить работу программы через вызов функции write_order_to_json() с передачей
в нее значений каждого параметра"""
import json
import datetime


def read_order(file_n):
    """Функция читает исходный файл"""
    with open(file_n, 'r') as f_read:
        json_obj = json.load(f_read)
    return json_obj


def write_order_to_json(file_n, item, quantity, price, buyer, date):
    """Функция записывает данные в json-файл"""
    dict_to_json = dict()
    tmp_dict = dict()
    tmp_dict['item'] = item
    tmp_dict['quantity'] = quantity
    tmp_dict['price'] = price
    tmp_dict['buyer'] = buyer
    tmp_dict['date'] = date
    dict_to_json = read_order(file_n)
    dict_to_json['orders'].append(tmp_dict)
    with open(file_n, 'w') as f_write:
        json.dump(dict_to_json, f_write, indent=4)


FILE_JSON = 'orders.json'
now = datetime.datetime.now()
write_order_to_json(FILE_JSON, 'Laptop', 1, 599, 'John',
                    now.strftime('%H-%M-%S-%d-%m-%Y'))
