import requests
from bs4 import BeautifulSoup


def main():
    PAGE_LIMIT = 201

    for i in range(0, PAGE_LIMIT):
        actors = []
        START_ITEM = i * 50 + 1
        url = f"https://www.imdb.com/search/name/?match_all=true&start={START_ITEM}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            continue
        soup = BeautifulSoup(response.text, "html.parser")
        actor_el = soup.select(
            f"#main > div > div.lister-list > div > div.lister-item-content > h3 > a "
        )
        for actor in actor_el:
            actors.append(actor["href"])

        # append the list into a txt file
        with open("scraping/popular_actors.txt", "a", encoding="utf-8") as f:
            for actor in actors:
                f.write(f"{actor}\n")

        print(f"Page {i} done")


if __name__ == "__main__":
    main()
