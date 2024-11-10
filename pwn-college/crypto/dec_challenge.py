from Crypto.Util.strxor import strxor

def xor_encrypt(s, key):
    return strxor(s.encode(),key.encode()).decode()

while True:
    s = input("Enter Encrypted String (or 'exit' to quit): ")
    if s == "exit":
        break
    key = input("Enter the key: ")
    result = xor_encrypt(s, key)
    print(f"XOR result: {result}")

