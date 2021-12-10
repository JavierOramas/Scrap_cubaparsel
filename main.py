import requests
from bs4 import BeautifulSoup
import re
import csv
import json


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def extract_href(text):
    start = text.find('href=')+6
    text = text[start:]

    start = text.find('"')
    text = text[:start]
    return text


def extract_src(text):
    start = text.find('src=')+5
    text = text[start:]

    start = text.find('"')
    text = text[:start]
    return text


def dump_data(data: dict):
    with open('cubaparsel.json', 'w') as fp:
        json.dump(data, fp)


urls = ['https://cubaparcel.com/tienda/', 'https://cubaparcel.com/product-category/accesorios-de-autos/',
        'https://cubaparcel.com/product-category/combos/']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
payload = {
    'query': 'test'
}

links = []

for url in urls:
    response = requests.get(url, data=payload, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

links += soup.find_all('li', {"class": "product-category"})

for index, i in enumerate(links):
    links[index] = extract_href(str(i.find_all('a')[0]))

data = {}

for i in links:
    response = requests.get(i, data=payload, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    links_items = soup.find_all('li', {"class": "type-product"})

    for index, it in enumerate(links_items):
        links_items[index] = extract_href(str(it.find_all('a')[0]))

    for j in links_items:
        response = requests.get(j, data=payload, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = cleanhtml(str(soup.find('h1', {"class": "product_title"})))
        # title = 'test'
        price = cleanhtml(str(soup.find('p', {"class": "price"})))
        # price = 'test'
        description = cleanhtml(
            str(soup.find('div', {"class": "woocommerce-Tabs-panel--description"})))
        # description = 'test'
        img = extract_src(
            str(soup.find('figure', {"class": "woocommerce-product-gallery__wrapper"})))
        # img = 'test'

        if not cleanhtml(str(i)) in data:
            data[cleanhtml(str(i))] = {}
        if not cleanhtml(str(title)) in data[cleanhtml(str(i))]:
            data[cleanhtml(str(i))][cleanhtml(str(title))] = {}

        data[cleanhtml(str(i))][cleanhtml(str(title))] = {
            "title": title, "price": price, "description": description, "img": img}

dump_data(data)
