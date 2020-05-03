import requests
from bs4 import BeautifulSoup
import pprint
import pandas as pd
import time
from random import randint

# instantiates the prettyprint module
pp = pprint.PrettyPrinter()

# will store individual items we pull out of each iteration
rank = []
name = []
date = []
genre = []
score = []

# create dictionary to store our data before converting into pandas.DataFrame
albums = {}
albums.update({'rank': rank, 'name': name, 'date': date, 'genre': genre, 'score': score})

# will change the page number in the desired URL
pages = [str(i) for i in range(1, 21)]

# Preparing the monitoring of the loop
start_time = time.time()
requestn = 0

for number in pages:
    # var the URL to scrape
    URL = 'https://www.albumoftheyear.org/ratings/6-highest-rated/all/{x}'.format(x=number)

    # send the page request
    page = requests.get(URL)

    # pause the loop - for human-like appearance
    time.sleep(randint(8, 15))

    # Monitor the requests
    requestn += 1
    elapsed_time = time.time() - start_time
    print('Requests: ', requestn, 'Elapsed Time: ', elapsed_time)

    # instantiate a BS object with our page content for it to parse over
    soup = BeautifulSoup(page.text, 'html.parser')

    # you are looking for a div tag, with class=albumListRow
    # this will be the div we will be scraping 'within'
    album_name = soup.find_all('div', class_='albumListRow')

    # pulls out the items from the soup instance >> 'album name'
    for album in album_name:
        # the original rank had a . in it
        ranki = str(album.find('span', class_='albumListRank').text.replace('.', ''))
        rank.append(ranki)

        namei = album.a.text
        name.append(namei)

        datei = album.find('div', class_='albumListDate').text
        date.append(datei)
        if album.find('div', class_='albumListGenre') is None:
            genrei = 'Unknown'
            genre.append(genrei)
        else:
            genrei = album.find('div', class_='albumListGenre').text
            genre.append(genrei)
        scorei = album.find('div', class_='scoreValue').text
        score.append(scorei)

album_info = pd.DataFrame(albums)
album_info.to_csv('album_download.csv')
# ------------------------
