import requests
from bs4 import BeautifulSoup
import csv

URL = "https://coty.brandquad.ru/lucp/4e1de2168d0d456784bcdd4d60305629/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
FILE = "prod.csv"  # путь сохранения файла


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, timeout=30, params=params)
    r.encoding = 'utf-8'
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find_all("a", class_="page")
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
    # print(pagination)


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="catalog__products_item")
    prod = []
    for item in items:
        prod.append({
            "title": item.find("span", class_="name").get_text(),
            "link": item.find("div", class_="text").find_next("a").get("href"),
            "brand": item.find("div", class_="text").find_next("a").get_text(),
            "shk": item.find("div", class_="text").find_next("a").find_next("a").get_text()
        })
    return prod


def save_file(items, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)  # убрал dialect=";"
        writer.writerow(["Название", "Ссылка", "Бренд", "ШК"])
        for item in items:
            writer.writerow([item["title"], item["link"], item["brand"], item["shk"]])


def parse():
    URL = input("Введите URL:")
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        prod = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f"Парсинг страницы {page} из {pages_count}...")
            html = get_html(URL, params={"page": page})
            prod.extend(get_content(html.text))
        save_file(prod, FILE)
        print(f"Получено {len(prod)} товаров")
    else:
        print("Ошибка сайта")


parse()
