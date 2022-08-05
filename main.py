import requests
import re

from bs4 import BeautifulSoup

def scrape_page(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, "html.parser")

    product_page_url = url
    title = soup.find("div", class_="product_main").find("h1").text
    product_description = soup.select_one("div#product_description ~ p").text
    universal_product_code = soup.find("th", text="UPC").find_next("td").text
    price_exclude_tax = soup.find("th", text="Price (excl. tax)").find_next("td").text
    price_include_tax = soup.find("th", text="Price (incl. tax)").find_next("td").text

    string_available = soup.find("th", text="Availability").find_next("td").text
    number_available = re.findall("\d+", string_available)[0]

    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text
    
    image = soup.find("img")["src"]
    image_url = "https://books.toscrape.com/" + image

    print(category)
    print(title)
    print(image_url)


def main():
    scrape_page("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")

if __name__ == "__main__":
   main()