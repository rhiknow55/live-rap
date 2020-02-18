Task 1: Make rap lyrics from other lyrics
1. Download a bunch of popular rap song lyrics, and train a word2vec (CBOW or skip gram) model based on that corpus
2. Take a new song lyric (and the background track) and keep count of line number and the # of syllables in each line
3. Create the lyrics so that each line makes sense (randomly choose a word? and make a sentence?)


Task 2: Rap lyrics from topic
1. Use a corpus of words that's public first to train a model OR use a trained model (idk if there is in word2vec)
2. Create lyrics that make sense FIRSTLY within that sentence given a topic
2.1 Then perhaps expand so that the entire stanzas make sense together


OPTIONAL:
Make the lyrics rhyme, so make sure the last word of the sentence rhymes and then work backwards


TODO: Use a diff tokenizer that doesn't split single quotes
https://stackoverflow.com/questions/49499770/nltk-word-tokenizer-treats-ending-single-quote-as-a-separate-word/49506436#49506436


TODO: Make a rap lyric scraper quickly to speed up process
For now just manually


TODO: Clean the data more (ex. remove some numbers, brackets, punctuation)
