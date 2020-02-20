# 1. Go through the given link and look for the href links to actual songs
# 2. For each href link to a song, scrape just the lyrics
# 2.1 Can be done via class names again!
# 3. Store each song into a text file with appropriate name

import requests
import urllib.request
from bs4 import BeautifulSoup # a tool for parsing json and xml

import os

def main():
    # Step 1
    url = "https://www.metrolyrics.com/top100-hiphop.html"
    soup = make_soup(url)

    # Get all the valid hrefs to scrape
    validatags = soup.find_all("a", class_=["song-link hasvidtoplyric", "title hasvidtoplyriclist"])
    hrefs = [tag.get('href') for tag in validatags]

    get_lyrics(hrefs)


def make_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup



# Step 2 + 3
def get_lyrics(hrefs):
    songs = []
    for songlink in hrefs:
        lyrics = ""
        soup = make_soup(songlink)

        verses = soup.find_all("p", class_="verse")
        for verse in verses:
            lyrics += (verse.text + "\n" + "\n")

        # Save the file
        songs.append(lyrics)

        songname = soup.find("h1").text
        # TODO: check if file exists first
        fullfilepath = filepath + songname + ".txt"
        if os.path.isfile(fullfilepath):
            print(fullfilepath, " already exists!")
        else:
            print("Scraping lyrics of ", songname, "!")
            write_file(fullfilepath, lyrics)

# Step 3
lyricsfolder = "/lyrics/"
filepath = os.path.dirname(os.path.realpath(__file__)) + lyricsfolder

def write_file(fullfilepath, text):
    with open(fullfilepath, "w+") as f:
        f.write(text)


if __name__ == '__main__':
    main()
    print("Finished scraping lyrics!")
