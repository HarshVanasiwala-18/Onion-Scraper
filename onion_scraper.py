import requests
import csv
import random
from itertools import cycle
from termcolor import colored
import string
import os

target_links = []

def get_tor_session():
    session = requests.session()
    session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                        'https': 'socks5h://127.0.0.1:9050'}
    return session

def torSearcher(url):
    session = get_tor_session()
    try:
        print("Getting ...", url)
        result = session.get(url).text
        filename = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
        with open('Onion Sites' + '/' + filename + '.html',"w+", encoding="utf-8") as newthing:
            newthing.write(result)
    except KeyboardInterrupt:
        print("\n[!] Keyboard Interrupt Detected. Exiting...")
        exit()
    except:
        print(f'[!] {url} :is not a valid onion site')

def start():
    print(colored('[#]Tor Browser\Browser\TorBrowser\Tor.exe Do not forget to start Tor.exe', 'red', attrs=['reverse', 'blink']))
    #Please enter the path of the file containing the tor.exe: Tor Browser\Browser\TorBrowser\Tor\tor.exe
    os.startfile(r'C:\Users\harsh\OneDrive\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe')
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
