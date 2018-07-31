import flag


def check_key(key):
    assert key.startswith("flag{")
    assert key.endswith("}")
    return key[5:-1]


def generate(a, b):
    with open("cipher.txt", "w") as f:
        for i in range(len(b)):
            f.write(str(a % b[i]) + "\n")


def main():
    key = check_key(flag.flag)
    x = int(key.encode("hex"), 16)
    y = [
        0x101, 0x107, 0x10d, 0x10f, 0x115,
        0x119, 0x11b, 0x125, 0x133, 0x137,
        0x139, 0x13d, 0x14b, 0x151, 0x15b,
        0x15d, 0x161, 0x167, 0x16f, 0x175
    ]
    generate(x, y)


if __name__ == '__main__':
    main()
