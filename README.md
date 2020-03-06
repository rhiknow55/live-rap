# live-rap

## Introduction: What is live-rap?
live-rap began as a Bcgamejam2020 idea that wasn't finished (or really touched) during the jam.

The theme was "Prevail" and I brainstormed on what idea wouldn't possibly be done by anyone else - and boom, I decided to look up the anagrams for the word!

So I came upon "live rap", and this stuck to me.


## What does it do?

The purpose of the program is to "create" new rap lyrics based off of a large set of training lyrics.

It scrapes lyrics of raps that qualify as English lyrics and creates a word2vec model based on the words belonging to the lyrics.

Then it trains the word tokens by:
1. Replacing contractions with incorrect syllable count detection
2. Replacing numbers with words
3. Removing invalid tokens, usually punctuation
4. Removing profanity

Once the training is complete, given a song, live-rap TM will create lyrics of the correct syllable count and rhyme that you can now sing during karaoke (causing confusion and awe to everyone else)!


## How to use?

First install the dependencies via:
pip install --user --requirement requirements.txt

then run:
python liverap.py





## Changelog + Scrap work

Task 1: Make rap lyrics from other lyrics
1. Download a bunch of popular rap song lyrics, and train a word2vec (CBOW or skip gram) model based on that corpus
2. Take a new song lyric (and the background track) and keep count of line number and the # of syllables in each line
3. Create the lyrics so that each line makes sense (randomly choose a word? and make a sentence?)


Task 2: Rap lyrics from topic
1. Use a corpus of words that's public first to train a model OR use a trained model (idk if there is in word2vec)
2. Create lyrics that make sense FIRSTLY within that sentence given a topic
2.1 Then perhaps expand so that the entire stanzas make sense together


OPTIONAL:
TODO: Make the lyrics rhyme, so make sure the last word of the sentence rhymes and then work backwards
- Whenever building the model, also create a dictionary of (word in model) to (words that rhyme with that word)
- Use this dictionary to choose words so that they rhyme
- Also when creating lyrics, make sure the lines that rhyme in the OG lyrics also rhyme in the new lyrics
  - make a grouping of rhymes dict, which all rhyme to the key. The values is a list of the line #s
- Now build the sentence from end to front



DONE: Use a diff tokenizer that doesn't split single quotes (TreeTokenizer)
https://stackoverflow.com/questions/34714162/preventing-splitting-at-apostrophies-when-tokenizing-words-using-nltk?lq=1


DONE: Make a rap lyric scraper quickly to speed up process
For now just manually


DONE: Clean the data more (ex. remove some numbers, brackets, punctuation)

DONE: replace numbers - https://stackoverflow.com/questions/40040177/search-and-replace-numbers-with-words-in-file

DONE: remove non english

DONE: punctuation

DONE: omit some contraction replacements that dont impact syllables (ex. ain't)

TODO: Scrape more songs to have larger model

DONE: Perhaps censor profanity?

TODO: Prettier read me with screenshots (of non profane lyrics!)
