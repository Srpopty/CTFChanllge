# -*- coding: utf-8 -*-
# Author: Srpopty
# Time: 2018.6.12
# Exploit of Poem
from string import ascii_letters

VaildChar = ascii_letters + ' \n,.'


def GetFreq(string):
    freq = 0
    for ch in string:
        freq += 1 if ch in VaildChar else 0
    return freq


def GetCipher(filename):
    with open(filename, 'rb') as f:
        return (''.join([line for line in f.readlines()])).decode('base64')


def GetPlainFromPool(pool, cipher):
    pool_length = len(pool)
    return ''.join([pool[i % pool_length][i / pool_length] for i in range(len(cipher))])


def DecryptPool(cipher):
    plain = ''
    key = ''
    freq = 0
    for ch in range(256):
        _plain = ''.join([chr(ord(c) ^ ch) for c in cipher])
        _freq = GetFreq(_plain)
        if _freq > freq:
            plain, freq, key = _plain, _freq, chr(ch)
    return plain, key, freq


def Decrypt(key_size, cipher):
    cipher_pool = [""] * key_size
    plain_pool = cipher_pool[:]
    key = ''
    freq = 0

    for i in range(len(cipher)):
        cipher_pool[i % key_size] += cipher[i]

    for i in range(key_size):
        plain_pool[i], _key, _freq = DecryptPool(cipher_pool[i])
        freq += _freq
        key += _key

    return GetPlainFromPool(plain_pool, cipher), key, freq


def main():
    key_min_length, key_max_length = 1, 50
    freq = 0
    key = ''
    plain = ''
    cipher = GetCipher('cipher.txt')

    for key_size in range(key_min_length, key_max_length):
        _plain, _key, _freq = Decrypt(key_size, cipher)
        if _freq > freq:
            freq, key, plain = _freq, _key, _plain

    print '[*] Frequency: ' + str(freq)
    print '[*] Key: ' + key
    print '[*] Plain:\n' + plain
    print ''
    print 'flag{%s}' % key


if __name__ == '__main__':
    main()
