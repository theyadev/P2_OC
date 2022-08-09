import csv
import os
import shutil

from typings import Product


OUT_FOLDER = "out"
IMAGES_FOLDER = "out/images"
SAVE_IMAGES = True


def create_out_folder() -> None:
    """Create the output folder if it doesn't exist."""

    if not os.path.exists(OUT_FOLDER):
        os.mkdir(OUT_FOLDER)

    if not os.path.exists(IMAGES_FOLDER):
        os.mkdir(IMAGES_FOLDER)


def csv_exists(name: str) -> None:
    """Check if the csv file exists."""
    return os.path.exists(os.path.join(OUT_FOLDER, name))


def create_csv(name: str) -> None:
    """Create the csv file."""
    with open(os.path.join(OUT_FOLDER, name + ".csv"), "w") as file:
        file.write("product_page_url,title,product_description,universal_product_code,price_exclude_tax,price_include_tax,number_available,category,image_url,star_rating\n")


def save_to_csv(product: Product, csv_name="products") -> None:
    """Save the product to the csv file."""
    if not csv_exists(csv_name + ".csv"):
        create_csv(csv_name)

    (product_page_url, title, product_description, universal_product_code, price_exclude_tax,
     price_include_tax, number_available, category, image_url, star_rating) = product

    writer = csv.writer(open(os.path.join(OUT_FOLDER, csv_name + ".csv"), "a"))
    writer.writerow([product_page_url, title, product_description, universal_product_code,
                    price_exclude_tax, price_include_tax, number_available, category, image_url, star_rating])


def save_image(data: str, folder: str, name: str) -> None:
    """Save the image to the output folder."""
    folder_path = os.path.join(IMAGES_FOLDER, folder)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    with open(os.path.join(folder_path, name.replace("/", ".")), "wb") as file:
        file.write(data)


def clear_out_folder() -> None:
    """Clear the output folder."""
    if not os.path.exists(OUT_FOLDER):
        return

    for file in os.listdir(OUT_FOLDER):
        if file.endswith(".csv"):
            os.remove(os.path.join(OUT_FOLDER, file))


def clear_image_folder() -> None:
    """Clear the output folder."""
    if not os.path.exists(IMAGES_FOLDER):
        return

    for file in os.listdir(IMAGES_FOLDER):
        shutil.rmtree(os.path.join(IMAGES_FOLDER, file))


def change_out_folder(name: str) -> None:
    """Change the output folder."""
    global OUT_FOLDER
    OUT_FOLDER = name


def change_image_folder(name: str) -> None:
    """Change the output folder."""
    global IMAGES_FOLDER
    IMAGES_FOLDER = name


def change_save_images(value: bool) -> None:
    """Change the value of the save images flag."""
    global SAVE_IMAGES
    SAVE_IMAGES = value
