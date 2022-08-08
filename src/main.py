from files import change_image_folder, change_out_folder, change_save_images, clear_image_folder, clear_out_folder, create_out_folder
from scrapping import join_url, scrap_categories, scrap_page


def main():
    output_folder = input("Enter the output folder path (default: /out): ")

    if output_folder.strip() != "":
        change_out_folder(output_folder)

    image_folder = input("Enter the image folder path (default: /out/images): ")

    if image_folder.strip() != "":
        change_image_folder(image_folder)

    clear_folder = input("Empty the output folder (y/n)? ")
    if clear_folder.strip().lower() == "y":
        clear_out_folder()
        clear_image_folder()

    save_images = input("Save images (y/n) (default: y)? ")
    if save_images.strip().lower() == "n":
        change_save_images(False)

    create_out_folder()

    categories = scrap_categories()

    for category_name, category_url in categories:
        scrap_page(join_url(category_url), category_name)


if __name__ == "__main__":
    main()
