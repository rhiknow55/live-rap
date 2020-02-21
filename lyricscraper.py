# 1. Go through the given link and look for the href links to actual songs
# 2. For each href link to a song, scrape just the lyrics
# 2.1 Can be done via class names again!
# 3. Store each song into a text file with appropriate name
# 4. Don't download if the song is over threshold non-english words. Because many songs have words that are not proper english words
# 4.1 Uses a downloaded set of english words to check each token

import requests
import urllib.request
from bs4 import BeautifulSoup # a tool for parsing json and xml

from nltk import word_tokenize

import os

WORDS = "words.txt"
ENGLISH_LYRICS_THRESHOLD = 0.3 # Pretty good threshold!

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
    english_words = setup_words_set()
    songs = []
    for songlink in hrefs:
        # First check if song is already downloaded
        soup = make_soup(songlink)
        songname = soup.find("h1").text
        fullfilepath = filepath + songname + ".txt"
        if os.path.isfile(fullfilepath):
            print(fullfilepath, " already exists! Skipping.")
            continue

        # Parse the lyrics
        lyrics = ""

        verses = soup.find_all("p", class_="verse")
        for verse in verses:
            lyrics += (verse.text + "\n" + "\n")

        # Check if enough english words
        tokens = word_tokenize(lyrics)
        count = 0
        for t in tokens:
            word = t.lower()
            if word in english_words:
                count += 1

        nonenglishratio = 1 - count / len(tokens)

        # Skip song if it's not english
        if nonenglishratio > ENGLISH_LYRICS_THRESHOLD:
            print("Skipping non-english song: ", songname)
            continue

        # Save the file
        songs.append(lyrics)

        print("Successfully scraped lyrics of ", songname, "!")
        write_file(fullfilepath, lyrics)

# Step 3
lyricsfolder = "/lyrics/"
filepath = os.path.dirname(os.path.realpath(__file__)) + lyricsfolder

def write_file(fullfilepath, text):
    with open(fullfilepath, "w+") as f:
        f.write(text)


def setup_words_set():
    res = {}
    with open(WORDS, "r") as f:
        res = set(word.strip().lower() for word in f)

    return res


if __name__ == '__main__':
    main()
    print("Finished scraping lyrics!")
