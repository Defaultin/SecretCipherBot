__all__ = ('post_encryption', 'post_decryption', 'update_alphabet')

import random

alphabet_list = ['\n'] + [chr(i) for i in range(32, 127)] + [chr(i) for i in range(
    1024, 1119)] + ['Ä', 'Ö', 'Ü', 'ß', 'ä', 'ö', 'ü'] + [chr(i) for i in range(8208, 8224)]

alphabet = {key: value for key, value in zip(
    range(len(alphabet_list)), alphabet_list)}


def update_alphabet(*, random_update=False):
    alist = alphabet_list[::]
    global alphabet
    if random_update:
        random.shuffle(alist)
    alphabet = {key: value for key, value in zip(range(len(alist)), alist)}


def comparator(value, key):
    len_key = len(key)
    dic, iter, full = {}, 0, 0
    for i in value:
        dic[full] = [i, key[iter]]
        full += 1
        iter += 1
        if (iter >= len_key):
            iter = 0
    return dic


def text_to_code(text):
    list_code, lent = [], len(text)
    for w in range(lent):
        for value in alphabet:
            if text[w] == alphabet[value]:
                list_code.append(value)
    return list_code


def code_to_text(code):
    list_code, lent = [], len(code)
    for i in range(lent):
        for value in alphabet:
            if code[i] == value:
                list_code.append(alphabet[value])
    return list_code


def encoder(value, key):
    dic = comparator(value, key)
    lis = []
    for v in dic:
        go = (dic[v][0]+dic[v][1]) % len(alphabet)
        lis.append(go)
    return lis


def decoder(value, key):
    dic = comparator(value, key)
    lis = []
    for v in dic:
        go = (dic[v][0]-dic[v][1]+len(alphabet)) % len(alphabet)
        lis.append(go)
    return lis


def pre_encryption(text, key):
    key_code = text_to_code(key)
    text_code = text_to_code(text)
    shifre = encoder(text_code, key_code)
    return ''.join(code_to_text(shifre))


def pre_decryption(shifre, key):
    key_code = text_to_code(key)
    text_code = text_to_code(shifre)
    text = decoder(text_code, key_code)
    return ''.join(code_to_text(text))


def post_encryption(start_text, key):
    key_length, text_length = str(len(key)), len(start_text)
    text = pre_encryption(start_text, key)
    shifre = ''
    for i in range(text_length-1):
        shifre += pre_encryption(text[i], text[i+1])
    shifre += pre_encryption(text[-1], key_length)
    if shifre.endswith(' ') or shifre.startswith(' '):
        start_text = start_text + '\n'
        key_length, text_length = str(len(key)), len(start_text)
        text = pre_encryption(start_text, key)
        shifre = ''
        for i in range(text_length-1):
            shifre += pre_encryption(text[i], text[i+1])
        shifre += pre_encryption(text[-1], key_length)
    elif shifre.endswith('\n') or shifre.startswith('\n'):
        start_text = start_text + ' '
        key_length, text_length = str(len(key)), len(start_text)
        text = pre_encryption(start_text, key)
        shifre = ''
        for i in range(text_length-1):
            shifre += pre_encryption(text[i], text[i+1])
        shifre += pre_encryption(text[-1], key_length)
    return shifre


def post_decryption(shifre, key):
    key_length, text_length = str(len(key)), len(shifre)
    text = ''
    text += pre_decryption(shifre[-1], key_length)
    for i in reversed(range(text_length-1)):
        text += pre_decryption(shifre[i], text[text_length-i-2])
    return pre_decryption(text[::-1], key)