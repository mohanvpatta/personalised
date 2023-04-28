import requests
import pandas as pd
from bs4 import BeautifulSoup


def extract_thumbnail_url():
    df = pd.read_csv("scraping/links.csv")

    # open the last id
    with open("scraping/last_thumbnail_id.txt", "r", encoding="utf-8") as f:
        last_id = int(f.read())

    for index, row in df.iterrows():
        if row["id"] <= last_id:
            continue

        url = row["link"]
        if url == "" or url == " ":
            continue

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        try:
            img_url = soup.select(
                "body > main > div.loading-inner > div > div.preview-product-header__wrapper > div.preview-product-header__image__wrapper > div > div > picture > source:nth-child(2)"
            )[0]["srcset"].split(" ")[0]
        except IndexError:
            with open("scraping/img_errors.txt", "a", encoding="utf-8") as f:
                f.write(f"{row['id']}\n")
            continue

        print(img_url)

        # save link to a csv file
        with open("scraping/thumbnails.csv", "a", encoding="utf-8") as f:
            f.write(f"{row['id']},{img_url}\n")

        with open("scraping/last_thumbnail_id.txt", "w", encoding="utf-8") as f:
            f.write(str(row["id"]))


def download_thumbnails():
    df = pd.read_csv("thumbnails.csv")

    # open last download id
    with open("scraping/last_download_id.txt", "r", encoding="utf-8") as f:
        last_id = int(f.read())

    for index, row in df.iterrows():
        if row["id"] <= last_id:
            continue
        url = row["link"]
        if url == "" or url == " ":
            continue

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            with open("scraping/img_errors.txt", "a", encoding="utf-8") as f:
                f.write(f"{row['id']}\n")
            continue

        with open(f"scraping/posters/{row['id']}-0.jpg", "wb") as f:
            f.write(response.content)

        print(f"Downloaded {row['id']}")

        # save the last download id
        with open("scraping/last_download_id.txt", "w", encoding="utf-8") as f:
            f.write(str(row["id"]))


def main():
    download_thumbnails()


if __name__ == "__main__":
    main()
