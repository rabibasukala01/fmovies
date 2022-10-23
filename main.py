import requests
from bs4 import BeautifulSoup
import random
import json
import time

# change as per the need
genre = 'war-politics'
file_name = genre


BASE_URL = 'https://fmoviesgo.to/genre/'

main = []
proxies = []

# proxy server
#
# with open('ips.txt', 'r') as f:
#     ips = f.readlines()

# for ip in ips:
#     proxy_server = {"http": f"http://{ip.strip()}",
#                     "https": f"https://{ip.strip()}",
#                     "ftp": f"ftp://{ip.strip()}", }
#     proxies.append(proxy_server)


# soup for page number getting
result = requests.get(f"{BASE_URL}{genre}")
soup = BeautifulSoup(result.text, "html.parser")
pg_number = soup.find_all('li', {'class': 'page-item'})
pg_number = pg_number[-1].find('a')['href'].split('=')[1]

for page in pg_number:
    # main url request based on pagination
    url = f"{BASE_URL}{genre}?page={pg_number}"
    # result = requests.get(url, proxies=proxies[random.randint(0, len(ips))])
    result = requests.get(url)

    # soup to find all div present
    soup = BeautifulSoup(result.text, "html.parser")

    movies = soup.find_all("div", {"class": "flw-item"})

    # looping through the all divs and finding all required elemnets
    for movie in movies:
        movie_link = movie.find("h2").find("a")['href']
        movie_main_link = "https://fmoviesgo.to"+movie_link

        movie_name = movie.find("h2").find("a")['title']

        # next page of a movie
        response = requests.get(movie_main_link)
        new_soup = BeautifulSoup(response.text, "html.parser")

        imdb = new_soup.find(
            'button', {"class": "btn btn-sm btn-radius btn-warning btn-imdb"}).text

        rows = new_soup.find_all('div', {'class': 'row-line'})
        released = rows[0].text.split(":")[1].strip()

        genres = rows[1].find_all('a')
        category = []
        for genre in genres:
            category.append(genre.text)

        casts = rows[2].find_all('a')
        actors = []
        for cast in casts:
            actors.append(cast.text)

        desc = new_soup.find('div', {'class': 'description'}).text.strip()

        informations = {
            'Name': movie_name,
            'description': desc,
            'Link': movie_main_link,
            'genre': category,
            'IMDB': imdb,
            'Released': released,
            'casts': actors
        }

        main.append(informations)
        time.sleep(1)

with open(f'{file_name}.json', 'w') as f:
    json.dump(main, f)
