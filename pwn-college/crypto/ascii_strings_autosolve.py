from pwn import *
from Crypto.Util.strxor import strxor

# Connect to the challenge process
p = process("/challenge/run")

# Loop through the challenge rounds
for n in range(1, 10):
    # Receive the encrypted string and the key
    p.recvuntil(b"- Encrypted String: ")
    encrypted_str = p.recvline().strip().decode()
    
    p.recvuntil(b"- XOR Key String: ")
    xor_key = p.recvline().strip().decode()

    # Decrypt the string
    decrypted_str = strxor(encrypted_str.encode(), xor_key.encode()).decode()

    # Send the decrypted string as the answer
    p.sendlineafter(b"- Decrypted String? ", decrypted_str)

# Receive the flag
print(p.recvall().decode())
