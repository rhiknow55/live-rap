
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
TODO: Perhaps censor profanity?

TODO: Prettier read me with screenshots (of non profane lyrics!)

Uses:
TweetTokenizer
gensim
bs4 from BeautifulSoup

re
num2words
