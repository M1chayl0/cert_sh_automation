# Author: https://github.com/M1chayl0/

import requests
import json
import argparse
from bs4 import BeautifulSoup

def crtsh_search(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    response = requests.get(url)
    data = json.loads(response.content)
    subdomains = set()
    for item in data:
        subdomains.add(item["name_value"])
    return subdomains

def google_search(domain):
    url = f"https://www.google.com/search?q=site%3A{domain}&start=0"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    subdomains = set()
    for a in soup.find_all('a', href=True):
        if domain in a['href'] and a['href'].startswith('http'):
            subdomains.add(a['href'].split('/')[2])
    return subdomains

def find_subdomains(domain):
    subdomains = set()
    subdomains.update(crtsh_search(domain))
    subdomains.update(google_search(domain))
    return subdomains

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="The domain to search for subdomains")
    args = parser.parse_args()
    subdomains = find_subdomains(args.domain)
    for subdomain in subdomains:
        print(subdomain)
