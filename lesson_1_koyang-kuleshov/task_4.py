"""Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode)"""
WORDS = ['разработка', 'администрирование', 'protocol', 'standard']
for word in WORDS:
    spam_encode = word.encode('utf-8')
    print(spam_encode)
    spam_decode = spam_encode.decode('utf-8')
    print(spam_decode)
