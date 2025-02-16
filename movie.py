import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_movies(year):
    url = f'https://www.imdb.com/search/title/?year={year}&title_type=feature&sort=popularity,asc'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {year}, Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    movies = []
    for item in soup.find_all('div', class_='lister-item mode-advanced'):
        title = item.h3.a.text
        try:
            rating = item.find('div', class_='inline-block ratings-imdb-rating').strong.text
        except AttributeError:
            rating = 'N/A'
        movies.append([year, title, rating])
    return movies

all_movies = []
for year in range(1898, 2024):  # Adjust the end year as needed
    print(f"Scraping movies for the year {year}...")
    movies = scrape_movies(year)
    all_movies.extend(movies)
    time.sleep(1)  # Be respectful and avoid overwhelming the server

with open('top_movies.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Year', 'Title', 'Rating'])
    writer.writerows(all_movies)
