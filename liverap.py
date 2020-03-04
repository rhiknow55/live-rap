# custom imports
from syllablecounter import syllable_count
from misc import is_number
import rhymefinder as rf
import profanitydetector as profanity

# normal imports
from nltk.tokenize import TweetTokenizer
tokenizer = TweetTokenizer()
from random import randint
import os
import string
from num2words import num2words

# word2vec imports
from gensim.models import Word2Vec

# contractions
# We want ONLY to make the translation if the syllable count is wrong
contractions = {
# "aren't": "are not", # 2, 3
# "can't": "cannot", # 1, 2
# "can't've": "cannot have",
# "'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
#"he'd": "he would",
#"he'd've": "he would have",
#"he'll": "he will",
#"he'll've": "he will have",
#"how'd": "how did",
#"how'd'y": "how do you",
#"how'll": "how will",
#"i'd've": "I would have",
#"i'll": "I will",
#"i'll've": "I will have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
#"it'll": "it will",
#"it'll've": "it will have",
#"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
#"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
#"shan't": "shall not",
#"sha'n't": "shall not",
#"shan't've": "shall not have",
#"she'd": "she would",
#"she'd've": "she would have",
#"she'll": "she will",
#"she'll've": "she will have",
#"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
#"so've": "so have",
#"so's": "so is",
"that'd": "that would",
"that'd've": "that would have",
#"that's": "that is",
#"there'd": "there would",
#"there'd've": "there would have",
#"there's": "there is",
#"they'd": "they would",
#"they'd've": "they would have",
#"they'll": "they will",
#"they'll've": "they will have",
"they're": "they are",
#"they've": "they have",
#"to've": "to have",
"wasn't": "was not",
#"we'd": "we would",
#"we'd've": "we would have",
#"we'll": "we will",
#"we'll've": "we will have",
#"we're": "we are",
#"we've": "we have",
#"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
#"what's": "what is",
"what've": "what have",
#"when's": "when is",
"when've": "when have",
#"where'd": "where did",
#"where's": "where is",
#"where've": "where have",
#"who'll": "who will",
#"who'll've": "who will have",
#"who's": "who is",
#"who've": "who have",
#"why's": "why is",
#"why've": "why have",
"will've": "will have",
#"won't": "will not",
#"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
#"y'all": "you all",
#"y'all'd": "you all would",
#"y'all'd've": "you all would have",
#"y'all're": "you all are",
#"y'all've": "you all have",
#"you'd": "you would",
#"you'd've": "you would have",
#"you'll": "you will",
#"you'll've": "you will have",
#"you're": "you are",
#"you've": "you have"
}

LYRICS_DIRECTORY = "lyrics/"
MODELS_DIRECTORY = "models/"
CREATIONS_DIRECTORY = "/creations/"
invalidtokens = [",", "(", ")", ";", "?", "!", ".", ":", "[", "]", "©", "-"]

# Rhyming
rhymedictionary = {}

# Variable variables
binaryname = "lyric_model1.bin"
referencesong = "XXXTENTACION - Changes Lyrics.txt"
sparsity_threshold = 10 # Number of times a word is presented to be included in model
topn = 5 # Number of similar words to check

modelbinarypath = MODELS_DIRECTORY + binaryname

def main():
    if os.path.isfile(modelbinarypath):
        while True:
            p = input("> Model " + modelbinarypath + " exists, press (o) to override and make a new model, or (l) to load existing model.\n")
            if p == "o":
                print("Overriding with new model.")
                model = create_model()
                break
            elif p == "l":
                print("Loading existing model.")
                model = Word2Vec.load(modelbinarypath)
                break
    else:
        model = create_model()

    print(model)

    # Create rap
    lyrics = create_rap(referencesong, model)

    # Save liverap into a text file
    save_liverap(referencesong, lyrics)



def create_model():
    # Import training data, which are text files
    all_files = os.listdir(LYRICS_DIRECTORY)
    txt_files = [f for f in all_files if f[-4:] == ".txt"]

    lines = [] # list of lines (strings)
    for filename in txt_files:
        with open(LYRICS_DIRECTORY + filename) as f:
            sublines = [line.rstrip("\n") for line in f] # rstrip removes the newline and spaces at the right of that string
        lines += sublines

    tokenized_sentences = [] # list of lists, where the inner list has tokenized sentences
    for line in lines:
        tokens = tokenizer.tokenize(line) # TODO: Could use a different tokenizer, since this one splits the single quotes
        lowertokens = [token.lower() for token in tokens]
        filteredtokens = clean_tokens(lowertokens)
        tokenized_sentences.append(filteredtokens)

    # Create word2vec model
    model = Word2Vec(tokenized_sentences, min_count=sparsity_threshold)
    model.save(modelbinarypath)

    # Create rhyme dictionary
    create_rhyme_dict(model)

    return model

# Clean the words
def clean_tokens(tokens):
    # Gets the contraction or default (which is just the word) if doesn't exist
    res = [contractions.get(word, word) for word in tokens]

    # Replace numbers to words
    res = [num2words(int(word)) if is_number(word) else word for word in res]

    # remove invalid tokens
    res = [word for word in res if all(it not in word for it in invalidtokens)]

    res = [word for word in res if word != "'"]

    # Remove profanity
    res = [word for word in res if not profanity.is_profanity(word)]

    return res


def create_rhyme_dict(model):
    vocab = list(model.wv.vocab)
    print(vocab)

    for i in range(len(vocab)):
        for j in range(i+1, len(vocab)):
            if rf.is_rhyme(vocab[i], vocab[j]):
                # Add to both elements' lists
                add_to_rhyme_dict(vocab[i], vocab[j])
                add_to_rhyme_dict(vocab[j], vocab[i])

def add_to_rhyme_dict(word, rhymingword):
    if word not in rhymedictionary.keys():
        rhymedictionary[word] = []

    rhymedictionary[word].append(rhymingword)

# -----------------------

def create_rap(filename, model):
    fullpath = LYRICS_DIRECTORY + filename
    with open(fullpath) as f:
        lines = [line.rstrip("\n") for line in f]

    # Count the syllables in each line by tokenizing into words
    syllables = []
    for line in lines:
        tokens = tokenizer.tokenize(line)

        count = 0
        for word in tokens:
            count += syllable_count(word)

        syllables.append(count)

    # Now create the rap lyric lines by picking words that fit the syllable count
    finalsentences = []
    for syl in syllables:
        total = syl

        # Pick words from model
        chosen = []
        vocab = list(model.wv.vocab)
        index = randint(0, len(vocab) - 1)
        word = vocab[index]

        i = 0
        while total:
            count = syllable_count(word)
            if total >= count:
                total -= count
                chosen.append(word)
                i = 0
            else:
                if i < topn - 1:
                    i += 1
                else:
                    word = "a"
                    continue

            word = model.wv.most_similar(positive=chosen, topn=topn)[i][0] # Need to access the first element of a tuple in a list

        finalsentences.append(chosen)

    # Format the final sentences into a string
    lyrics = ""
    for sentence in finalsentences:
        line = ""
        for word in sentence:
            line += (" " + word)

        lyrics += (line + "\n")

    return lyrics

# Save new liverap to file
def save_liverap(filename, content):
    fullpath = os.path.dirname(os.path.realpath(__file__)) + CREATIONS_DIRECTORY + "liverap - " + filename
    with open(fullpath, "w+") as f:
        f.write(content)

    print("liverap file saved as ", fullpath)

if __name__ == "__main__":
    main()
    print("Completed creating liverap!")
