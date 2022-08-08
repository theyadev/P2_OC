import os
import requests
import re

from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "http://books.toscrape.com/"


def get_star_rating(value: str):
    if value == "One":
        return 1
    elif value == "Two":
        return 2
    elif value == "Three":
        return 3
    elif value == "Four":
        return 4
    elif value == "Five":
        return 5
    else:
        return 0


def csv_exists(name):
    return os.path.exists(name)


def create_csv(name):
    with open(name, "w") as file:
        file.write("product_page_url,title,product_description,universal_product_code,price_exclude_tax,price_include_tax,number_available,category,image_url,star_rating\n")


def save_to_csv(product, csv_name="products.csv"):
    if not csv_exists(csv_name):
        create_csv(csv_name)

    (product_page_url, title, product_description, universal_product_code, price_exclude_tax,
     price_include_tax, number_available, category, image_url, star_rating) = product

    with open(csv_name, "a") as file:
        file.write(f"{product_page_url},{title},{product_description},{universal_product_code},{price_exclude_tax},{price_include_tax},{number_available},{category},{image_url},{star_rating}\n")


def scrap_product(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    product_page_url = url

    title = soup.find("div", class_="product_main").find("h1").text
    product_description = soup.select_one("div#product_description ~ p").text
    universal_product_code = soup.find("th", text="UPC").find_next("td").text
    price_exclude_tax = soup.find(
        "th", text="Price (excl. tax)").find_next("td").text
    price_include_tax = soup.find(
        "th", text="Price (incl. tax)").find_next("td").text

    string_available = soup.find(
        "th", text="Availability").find_next("td").text
    number_available = re.findall("\d+", string_available)[0]

    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text

    image = soup.find("img")["src"]
    image_url = "https://books.toscrape.com/" + image

    string_star_rating = soup.find("p", class_="star-rating")['class'][1]
    star_rating = get_star_rating(string_star_rating)

    product = (product_page_url, title, product_description, universal_product_code,
               price_exclude_tax, price_include_tax, number_available, category, image_url, star_rating)

    return product


def scrap_page(url, csv_name="products.csv"):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    current = soup.find("li", class_="current").text

    print(current)

    products = soup.find_all("article", class_="product_pod")

    for i, product in enumerate(products):
        print(f"{i+1}/{len(products)}")
        product_url = product.find("a")["href"]
        product = scrap_product(urljoin(url, product_url))
        save_to_csv(product)

    next_page = soup.find("li", class_="next")
    if next_page:
        next_page_url = next_page.find("a")["href"]
        scrap_page(urljoin(url, next_page_url))


def main():
    scrap_page(
        "http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html")


if __name__ == "__main__":
    main()
