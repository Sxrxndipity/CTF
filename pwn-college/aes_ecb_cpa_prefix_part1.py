from base64 import b64encode, b64decode
from pwn import *
import string

#the plaintext we send gets padded automatically



flag = '}'

dic = string.ascii_letters + string.digits + string.punctuation
attempts=0
index = 2
p = process('./run')
n_restart=0
slice=-1

while (len(flag) != 16):
    if (attempts==10):
        n_restart+=1
        p.kill()
        p = process("./run")
        #print("number restart: ",n_restart)
    for char in dic:
        data = char + flag
        print("Your plaintext is : ",data)
        p.writeafter(b"Choice? ",b"1\n")
        p.writeafter(b"Data? ",data.encode() +b"\n")
        p.recvuntil(b"Result: ")
        b64plain = p.recvline().strip().decode()
        print("Your encrypted plaintext is",b64plain)
        attempts+=1
        print("attempt: ",attempts)

        p.writeafter(b"Choice? ",b"2\n")
        if len(flag)%16 == 0:
            index=1
        payload = "a"*(7+index)
        p.writeafter(b"Data? ",payload.encode() + b"\n")
        p.recvuntil(b"# of blocks: ")
        last_block = p.recvline().strip().decode()
        
        last_block =last_block.replace(".",":")
        p.recvuntil(b"Block " +last_block.encode())
        b64flag_c = p.recvline().strip().decode()
        print("encrypted b64 flag is : ",b64flag_c)
        attempts+=1
        print("attempt: ",attempts)

        if (attempts==10):
            attempts=0
            n_restart+=1
            p.close()
            p = process("./run")
            print("number restart: ",n_restart)
        if (b64plain == b64flag_c):
            flag = char + flag
            index+=1
            print("character found! new flag is: ",flag)
            break

p.close() 
