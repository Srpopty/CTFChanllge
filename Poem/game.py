import flag
import re


def check_key(key):
    assert key.startswith("flag{")
    assert key.endswith("}")
    key = key[5:-1]
    assert len(key) > 1 and len(key) < 50
    return key


def check_plain(plain):
    assert re.match('[A-Za-z\s]*', plain) is not None
    return plain


def encryt(key, plain):
    cipher = ""
    for i in range(len(plain)):
        cipher += chr(ord(key[i % len(key)]) ^ ord(plain[i]))
    return cipher


def get_plain():
    plain = ""
    with open("plain.txt") as f:
        while True:
            line = f.readline()
            if line:
                plain += line
            else:
                break
    return plain


def main():
    key = check_key(flag.flag)
    plain = check_plain(get_plain())
    cipher = encryt(key, plain)
    with open("cipher.txt", "w") as f:
        f.write(cipher.encode("base64"))


if __name__ == "__main__":
    main()
