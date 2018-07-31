# -*- coding: utf-8 -*-
# Author: Srpopty
# Time: 2018.6.12
# Chinese remainder theorem(CRT)

from functools import reduce


def Euclidean_ex(a, b):
    if b == 0:
        return 1, 0, a
    else:
        x, y, q = Euclidean_ex(b, a % b)
        x, y = y, (x - (a // b) * y)
        return x, y, q


def Int2Str(x):
    return hex(int(x))[2:-1].decode('hex')


def main():
    x = [
        257, 263, 269, 271,
        277, 281, 283, 293,
        307, 311, 313, 317,
        331, 337, 347, 349,
        353, 359, 367, 373
    ]

    y = [
        222, 82,  47,  96,
        197, 29,  122, 197,
        25,  8,   135, 175,
        174, 149, 77,  345,
        66,  112, 279, 129
    ]

    M = reduce(lambda a, b: a * b, x)
    Mi = [M//m for m in x]

    Ti = [Euclidean_ex(Mi[i], x[i])[0] for i in range(len(x))]

    result = 0
    for i in range(len(x)):
        result = (result + Mi[i] * Ti[i] * y[i]) % M

    print "flag{%s}" % Int2Str(result)


if __name__ == '__main__':
    main()
