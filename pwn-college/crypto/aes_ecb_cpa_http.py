import string
import requests as req
from bs4 import BeautifulSoup


url = 'http://challenge.localhost/'
flag = 'pwn.college{'
dic = string.ascii_letters + string.digits + string.punctuation
#to avoid server error from query ''', can mitigate with urlencoding but i cba
dic = dic.replace("'","")
index = 13

while '}' not in flag:
    for char in dic:
        query_param=f"SUBSTR(flag,{index},1)"
        r1=req.get(url,params={'query':query_param})
        soup = BeautifulSoup(r1.text,'html.parser')
        b64flag_c = soup.find_all('pre')[1].text.strip()

        query_param=f"'{char}'"
        r2=req.get(url,params={'query':query_param})
        soup = BeautifulSoup(r2.text,'html.parser')
        b64plain = soup.find_all('pre')[1].text.strip()

        if b64plain == b64flag_c:
            flag += char
            print("Current flag:", flag)
            break

    index += 1


print("Flag found:", flag)
