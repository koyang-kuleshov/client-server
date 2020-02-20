"""Определить, какие из слов «attribute», «класс», «функция», «type» невозможно
записать в байтовом типе."""
WORDS = ['attribute', 'класс', 'функция', 'type']
for word in WORDS:
    try:
        spam = eval(f'b"{word}"')
    except SyntaxError:
        print(f'Слово "{word}" невозможно перевести в байты')
