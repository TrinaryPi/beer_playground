from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

bsr_url = "https://beersmithrecipes.com/toprated/0"  # page 1
max_pages = 10
recipes_per_page = 21
# iterate through the top 10 pages of toprated beers
for x in range(1, max_pages):
    bsr_url = bsr_url[:-1] + "%d" % x
    bsr_html = urlopen(bsr_url)
    soup = BeautifulSoup(bsr_html, 'lxml')
    recipe_links = soup.find_all('h4')
    for h4 in recipe_links:
        for link in h4.find_all('a'):
            print(link.get('href'))
