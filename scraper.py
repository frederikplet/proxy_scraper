from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests
import base64
import asyncio
import aiohttp
import math
import random
import logging

# Suppresing any warnings in terminal
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)

#https://www.proxy-list.download/HTTP

def proxylistdownload(url='https://www.proxy-list.download/HTTP'):
    response = requests.get(url)
    html_content = response.text  # Extract the HTML content from the response
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')  # find the first table in the HTML
    proxies = {}
    for row in table.find_all('tr'):  # iterate over each row in the table
        cells = row.find_all('td')  # get all the cells in the row
        if len(cells) > 1:  # if there are two cells, it's an IP/port pair
            ip = cells[0].text.strip()
            port = cells[1].text.strip()
            proxies[ip] = port
    #print('fetched ', len(proxies), ' from ', url)
    return proxies


#https://free-proxy-list.net/

def freeproxylist(url='https://free-proxy-list.net/'):
    response = requests.get(url)
    html_content = response.text  # Extract the HTML content from the response
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')  # find the first table in the HTML
    proxies = {}
    for row in table.find_all('tr'):  # iterate over each row in the table
        cells = row.find_all('td')  # get all the cells in the row
        if len(cells) > 1:  # if there are two cells, it's an IP/port pair
            ip = cells[0].text.strip()
            port = cells[1].text.strip()
            proxies[ip] = port
    #print('fetched ', len(proxies), ' from ', url)
    return proxies


#https://www.us-proxy.org/

def usproxy(url="https://www.us-proxy.org/"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxy_table = soup.find('table')
    proxies = {}
    for row in proxy_table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 2:
            ip = cells[0].text
            port = cells[1].text
            proxies[ip] = port
    #print('fetched ', len(proxies), ' from ', url)
    return proxies


#https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all

def proxyscrape():
    all_proxies = {}
    methods=['socks5', 'socks4', 'http']
    for method in methods:
        url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={method}&timeout=10000&country=all&ssl=all&anonymity=all"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.get_text()
        proxies_dict = {}
        lines = data.split("\n")
        for line in lines:
            if line.strip():
                proxy, port = line.split(":")
                proxies_dict[proxy] = int(port)
        all_proxies.update(proxies_dict)
    #print('fetched ', len(all_proxies), ' from ', "https://api.proxyscrape.com/")
    return all_proxies


#https://advanced.name/freeproxy

def advancedname():
    def decode_base64(encoded_string):
        return base64.b64decode(encoded_string).decode()
    url = "https://advanced.name/freeproxy"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    alive_proxies_count = [int(s) for s in soup.find('b').get_text().split() if s.isdigit()][0]
    pages_to_scrape = math.ceil(alive_proxies_count / 100)
    all_ip_port_dict = {}
    for page_number in range(1, pages_to_scrape + 1):
        url = f"https://advanced.name/freeproxy?page={page_number}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        ip_port_dict = {decode_base64(row.find_all('td')[1].get('data-ip')): decode_base64(row.find_all('td')[2].get('data-port'))
                        for row in soup.find('table').find_all('tr')[1:]
                        if len(row.find_all('td')) >= 3 and row.find_all('td')[1].get('data-ip') and row.find_all('td')[2].get('data-port')}
        all_ip_port_dict.update(ip_port_dict)
    #print('Fetched', len(all_ip_port_dict), 'from https://advanced.name/freeproxy')
    return all_ip_port_dict



def scrape_all():
    # Create a ThreadPoolExecutor for concurrent execution of proxy-fetching functions
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(proxylistdownload),
            executor.submit(freeproxylist),
            executor.submit(usproxy),
            executor.submit(proxyscrape),
            executor.submit(advancedname)
        ]

        # Wait for all the futures to complete
        concurrent_results = [future.result() for future in futures]

    # Merge all the dictionaries into a single one
    all_proxies = {}
    for proxies in concurrent_results:
        all_proxies.update(proxies)

    #print("Total proxies fetched:", len(all_proxies))
    return all_proxies


async def proxy_request(website, loop=None):
    async def get_page(proxy, url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, proxy=f"http://{proxy}", timeout=5) as response:
                    return await response.text()
            except Exception as e:
                return None

    dict_proxies = proxyscrape()
    tasks = []
    
    if loop is None:
        loop = asyncio.get_event_loop()

    async with aiohttp.ClientSession() as session:  # Create a single ClientSession for all requests
        for ip, port in dict_proxies.items():
            proxy = f"{ip}:{port}"
            tasks.append(get_page(proxy, website))

        for future in asyncio.as_completed(tasks):
            result = await future
            if result is not None:
                return result
    return None
