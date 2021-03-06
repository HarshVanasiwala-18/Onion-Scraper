import requests
import csv
import random
import re
from itertools import cycle
from termcolor import colored
import onion_scraper
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# https://httpbin.org/ip
# http://ip-api.com/json/

def ua():
    user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577", "Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
                       "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13", "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27", "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"]

    user_agent = random.choice(user_agent_list)

    headers = {'User-Agent': user_agent}
    
    return headers

def get_proxy():
    driver = webdriver.Chrome('chromedriver_win32\chromedriver.exe')
    driver.get('https://free-proxy-list.net/')
    content = driver.page_source
    print('-'*50)
    print('-'*50)
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find_all('div')
    ip_table = pd.read_html(str(table))[0]
    final_ips = ip_table["IP Address"].astype(str) + ":" + ip_table["Port"].astype(str)
    final_ips.to_csv('proxylists.csv', index = False, header = False)

    proxylist = []

    with open('proxylists.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            proxylist.append(row[0])

    return proxylist

def main():
    proxy = get_proxy()
    proxy_pool = cycle(proxy)
    yourquery = input("Enter your query: ")
    print('-'*50)
    if " " in yourquery:
        yourquery = yourquery.replace(" ","+")

    url = "https://ahmia.fi/search/?q={}".format(yourquery)

    print('-'*50)

    ROOT_DIR = 'Onion Sites'
    project_dir = ROOT_DIR + '/'
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)

    for i in range(1, 301):
        proxy = next(proxy_pool)
        userAgent = ua()
        try:
            print("\r[*] Request : " + str(i), end = '')
            try:
                response = requests.get(url, headers = userAgent, proxies = {'http': proxy, 'https': proxy})
                try:
                    if response.status_code == 200:
                        request_url = requests.get(url, headers = userAgent, proxies = {'http': proxy, 'https': proxy})
                        content = request_url.text
                        regexquery = "\w+\.onion"
                        mineddata = re.findall(regexquery, content)
                        filename = "onionsites.csv"
                        print("\nSaving to ... ", filename)
                        mineddata = list(dict.fromkeys(mineddata))

                        with open(filename,"w+") as _:
                            print("")
                        for k in mineddata:
                            with open(filename,"a") as newfile:
                                k  = k + "\n"
                                newfile.write(k)
                        print("All the files written to a text file : \n", filename)
                        break
                    else:
                        print('\n[!] Proxy not working......Please try another proxy')
                except KeyboardInterrupt:
                    print("\n[!]Keyboard Interrupt Detected. Exiting...")
            except KeyboardInterrupt:
                print('\n[!] Exiting...')
                exit()
            except:
                print("\n[!] Skipping. Connnection error")
        except KeyboardInterrupt:
            print("\n[!]Keyboard Interrupt Detected. Exiting...")
            exit()


if __name__ == "__main__":
    print(colored('[#]This program is searching for Onion sites.', 'red', attrs=['reverse', 'blink']))
    print(colored('[#]It will search for the query you entered.', 'red', attrs=['reverse', 'blink']))
    print(colored('[#]It will save the results to a text file.', 'red', attrs=['reverse', 'blink']))
    print(colored('[#]ahmia.fi is the search engine using for onion sites.', 'red', attrs=['reverse', 'blink']))
    print(colored('[#]You can use below links to search for onion sites.\n', 'red', attrs=['reverse', 'blink']))
    print('# reddit/r/onions\n# hidden answers\n# dread\n# galaxy3\n# ahmia.fi\n# duckduckgo\n')
    print(colored('[#]Note : Program will take Time.......Hold yourself', 'red', attrs=['reverse', 'blink']))
    print('-'*50)
    main()
    onion_scraper.start()
