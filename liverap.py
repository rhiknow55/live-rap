# custom imports
from syllablecounter import syllable_count
from tsneplotter import tsne_plot

# normal imports
from nltk.tokenize import word_tokenize
from random import randint
import os
import string

# word2vec imports
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot

LYRICS_DIRECTORY = "lyrics/"
MODELS_DIRECTORY = "models/"
CREATIONS_DIRECTORY = "/creations/"
punctuations = [",", "'", ")", ";", "?", ".", ":", "]"]

# Variable variables
binaryname = "lyric_model1.bin"
referencesong = "XXXTENTACION - Changes Lyrics.txt"
sparsity_threshold = 10 # Number of times a word is presented to be included in model
topn = 5 # Number of similar words to check


def main():
    fullpath = MODELS_DIRECTORY + binaryname
    if os.path.isfile(fullpath):
        p = input("Model " + fullpath + " exists, press (y) to load, or (n) to override and make new model.\n")
        if p:
            model = Word2Vec.load(fullpath)
        else:
            model = create_model()
    else:
        model = create_model()

    model.save(fullpath)
    print(model)

    # Create rap
    lyrics = create_rap(referencesong, model)

    # Save liverap into a text file
    save_liverap(referencesong, lyrics)



def create_model():
    # Import training data, which are text files
    all_files = os.listdir(LYRICS_DIRECTORY)
    txt_files = [f for f in all_files if f[-4:] == ".txt"]

    lines = []
    for filename in txt_files:
        with open(LYRICS_DIRECTORY + filename) as f:
            sublines = [line.rstrip("\n") for line in f] # rstrip removes the newline and spaces at the right of that string
        lines += sublines

    sentences = [] # list of lists, where the inner list has tokenized sentences
    for line in lines:
        tokens = word_tokenize(line) # TODO: Could use a different tokenizer, since this one splits the single quotes
        lowertokens = [token.lower() for token in tokens]
        filteredtokens = cleantokens(lowertokens)
        sentences.append(filteredtokens)

    # Create word2vec model
    model = Word2Vec(sentences, min_count=sparsity_threshold)
    return model

# Clean the words
# 1. Remove non english words
# 2. Replace numbers
# 3. Remove punctuations
def cleantokens(tokens):
    out = s.translate(string.maketrans("",""), string.punctuation)


def create_rap(filename, model):
    fullpath = LYRICS_DIRECTORY + filename
    with open(fullpath) as f:
        lines = [line.rstrip("\n") for line in f]

    # Count the syllables in each line by tokenizing into words
    syllables = []
    for line in lines:
        tokens = word_tokenize(line)

        count = 0
        for word in tokens:
            count += syllable_count(word)

        syllables.append(count)

    print("lines len: ", len(lines), " | syllables len: ", len(syllables))

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

            word = model.wv.most_similar(positive=chosen, topn=topn)[i][0] # Need to access the first element of a tuple in a list

        finalsentences.append(chosen)

    # Format the final sentences into a string
    lyrics = ""
    for sentence in finalsentences:
        line = ""
        for word in sentence:
            space = " "
            # Add space before word if it does not have punctuation
            for p in punctuations:
                if p in word:
                    space = ""
                    break

            line += (space + word)

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
