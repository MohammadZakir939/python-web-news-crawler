import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

topic = input("Enter topic: ").lower()

sites = input("Enter websites separated by commas: ").split(",")

headers = {"User-Agent": "Mozilla/5.0"}

results = []

for site in sites:

    site = site.strip()

    try:
        response = requests.get(site, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a"):

            title = link.get_text(" ", strip=True)
            url = link.get("href")

            if title and url and topic in title.lower():

                url = urljoin(site, url)

                if url not in [x["url"] for x in results]:

                    results.append({
                        "title": title,
                        "url": url
                    })

    except Exception as error:
        print("Error:", error)


print("\nNEWS RESULTS")
print("=" * 50)

for i, news in enumerate(results, 1):

    print(f"\n{i}. {news['title']}")
    print(news["url"])


with open("news_results.txt", "w", encoding="utf-8") as file:

    for i, news in enumerate(results, 1):

        file.write(f"{i}. {news['title']}\n")
        file.write(f"{news['url']}\n\n")

print("\nArticles found:", len(results))
print("Saved to news_results.txt")