from pwn import *
from Crypto.Util.strxor import strxor
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes

# Connect to the challenge process
p = process("/challenge/run")

# Receive c1 (flag ciphertext)
p.recvuntil(b"Flag Ciphertext (b64): ")
c1 = p.recvline().strip() 
c1_bytes = b64decode(c1)  # Decode c1 immediately to get its length

# Generate a random plaintext of the same length as c1
plaintext = get_random_bytes(len(c1_bytes))
plaintext_b64 = b64encode(plaintext)

# Send the new plaintext and receive c2
p.sendlineafter(b"Plaintext (b64): ", plaintext_b64) 
p.recvuntil(b"Ciphertext (b64): ")
c2 = p.recvline().strip()
p.kill()

# Decode c2 from Base64
c2_bytes = b64decode(c2)

# Print lengths for debugging
print(f"Length of c1_bytes: {len(c1_bytes)}")
print(f"Length of c2_bytes: {len(c2_bytes)}")
print(f"Length of plaintext: {len(plaintext)}")

# Ensure lengths are the same
assert len(c1_bytes) == len(c2_bytes), "Lengths of c1 and c2 do not match!"
assert len(c1_bytes) == len(plaintext), "Lengths of c1 and plaintext do not match!"

# XOR: c1 ^ c2 ^ plaintext to get the flag
flag_bytes = strxor(c1_bytes, strxor(c2_bytes, plaintext))

# Decode flag to string and print it
flag = flag_bytes.decode(errors='ignore')  # Use 'ignore' to skip non-UTF-8 characters if needed
print(flag)
