GOOGLE_API = "AIzaSyDGPJ-tePfXppA69rLUalbv31NSfR88CFA"

import requests
import json
from pprint import pprint


def get_url(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API}&cx=0384ce638bbd143e5&q={query}&num=1"
    response = requests.get(url)
    data = json.loads(response.text)

    print(data)

    if data["searchInformation"]["totalResults"] == "0":
        return ""

    link = data["items"][0]["link"]
    return link


def main():
    # links = []
    # load the json file
    with open("data/movies.json", "r", encoding="utf-8") as f:
        movies = json.load(f)

    # get the last id
    with open("scraping/last_id.txt", "r", encoding="utf-8") as f:
        last_id = int(f.read())

    for movie in movies:
        if movie["id"] <= last_id:
            continue

        query = f"apple tv {movie['title']}"
        link = get_url(query.lower())

        # save link to a csv file
        with open("scraping/links.csv", "a", encoding="utf-8") as f:
            f.write(f"{movie['id']},{link}\n")

        with open("scraping/last_id.txt", "w", encoding="utf-8") as f:
            f.write(str(movie["id"]))


if __name__ == "__main__":
    main()
