from base64 import b64encode, b64decode
from pwn import *
import string

p = process("/challenge/run")

flag = 'pwn.college{'
dic = string.ascii_letters + string.digits + string.punctuation

index = 12

while '}' not in flag:
    for char in dic:
        p.sendafter(b"Choose an action?\n", b"1\n")
        p.sendafter(b"Data? ", (char.encode() + b"\n"))
        p.recvuntil(b"Result: ")
        b64plain = p.recvline().strip().decode()

        p.sendafter(b"Choose an action?\n", b"2\n")
        p.sendafter(b"Index? ", (str(index) + "\n").encode())
        p.sendafter(b"Length? ", b"1\n")
        p.recvuntil(b"Result: ")
        b64flag_c = p.recvline().strip().decode()

        if b64plain == b64flag_c:
            flag += char
            print("Current flag:", flag)
            break

    index += 1

p.close()

print("Flag found:", flag)
