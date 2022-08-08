import re
import requests

from bs4 import BeautifulSoup
from typing import Tuple
from urllib.parse import urljoin

from files import save_image, save_to_csv
from progress.bar import IncrementalBar
from typings import Product
from utils import get_star_rating

BASE_URL = "http://books.toscrape.com/"


def join_url(url: str) -> str:
    """Join the url with the base url."""
    return urljoin(BASE_URL, url)


def scrap_product(url: str) -> Product:
    """Scrap a product page."""
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    product_page_url = url

    title = soup.find("div", class_="product_main").find("h1").text

    try:
        product_description = soup.select_one(
            "div#product_description ~ p").text
    except:
        product_description = None

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


def scrap_page(url: str, csv_name="products.csv") -> None:
    """Scrap a page containing multiple products."""
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    try:
        current = soup.find("li", class_="current").text
    except AttributeError:
        current = "Page 1 of 1"

    products = soup.find_all("article", class_="product_pod")

    bar = IncrementalBar(current.strip() + " - " + csv_name, max=len(products))

    for i, product in enumerate(products):
        product_url = product.find("a")["href"]
        product = scrap_product(urljoin(url, product_url))
        save_to_csv(product, csv_name.strip())

        image_data = requests.get(product[8]).content
        save_image(image_data, csv_name, product[1] + ".jpg")

        bar.next()
    bar.finish()

    next_page = soup.find("li", class_="next")
    if next_page:
        next_page_url = next_page.find("a")["href"]
        scrap_page(urljoin(url, next_page_url), csv_name)


def scrap_categories() -> Tuple[str, str]:
    """Scrap the categories."""
    data = requests.get(BASE_URL)
    soup = BeautifulSoup(data.text, "html.parser")

    categories = soup.find("ul", class_="nav").find("ul").find_all("li")

    return [(category.find("a").text.strip(), category.find("a")["href"]) for category in categories]
