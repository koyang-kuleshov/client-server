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


def write_order_to_json(item, quantity, price, buyer, date):
    """Функция записывает данные в json-файл"""
    dict_to_json = dict()
    dict_to_json['item'] = item
    dict_to_json['quantity'] = quantity
    dict_to_json['price'] = price
    dict_to_json['buyer'] = buyer
    dict_to_json['date'] = date
    with open('orders.json', 'w', encoding='utf-8') as f_write:
        json.dump(dict_to_json, f_write, indent=4)


write_order_to_json('Laptop', 1, 599, 'John', '24-02-2020')
