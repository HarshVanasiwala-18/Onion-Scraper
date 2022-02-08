import requests
import csv
import random
from itertools import cycle
from termcolor import colored
import string

def get_tor_session():
    session = requests.session()
    session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                        'https': 'socks5h://127.0.0.1:9050'}
    return session

def torSearcher(url):

    session = get_tor_session()
    print("Getting ...", url)

    try:
        result = session.get(url).text
        filename = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
        with open(f"{filename}.html","w+", encoding="utf-8") as newthing:
            newthing.write(result)
    except:
        print("[!] Invalid URL")

def start():
    print(colored('[#]Tor Browser\Browser\TorBrowser\Tor.exe Do not forget to start Tor.exe', 'red', attrs=['reverse', 'blink']))

    onionlist = []

    with open('onionsites.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            onionlist.append(row[0])
    
    i = 0
    try:
        for i in onionlist:
            site = 'http://' + i
            i =+ 1
            torSearcher(site)
    except KeyboardInterrupt:
        print("\n[!] Keyboard Interrupt Detected. Exiting...")