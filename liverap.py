# custom imports
from syllablecounter import syllable_count
from tsneplotter import tsne_plot

# normal imports
from nltk.tokenize import word_tokenize
from random import randint
import os

# word2vec imports
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot

directory = "lyrics/"

def create_model():
    # Import training data, which are text files
    all_files = os.listdir(directory)
    txt_files = [f for f in all_files if f[-4:] == ".txt"]

    lines = []
    for filename in txt_files:
        with open(directory + filename) as f:
            sublines = [line.rstrip("\n") for line in f] # rstrip removes the newline and spaces at the right of that string
        lines += sublines

    sentences = [] # list of lists, where the inner list has tokenized sentences
    for line in lines:
        tokens = word_tokenize(line) # TODO: Could use a different tokenizer, since this one splits the single quotes
        lowertokens = [token.lower() for token in tokens]
        sentences.append(lowertokens)

    # Create word2vec model
    model = Word2Vec(sentences, min_count=2)
    # print(model)

    # Later if I continue training on model instead of re modelling every time
    # model.save('models/raplyrics.txt')

    # print(model.wv.most_similar(positive=['rap'], negative=[], topn=5))

    # tsne_plot(model)

    return model

model = create_model()


def create_rap(filename, model):
    with open(filename) as f:
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

        while total:
            count = syllable_count(word)
            if total >= count:
                total -= count
                chosen.append(word)

            word = model.wv.most_similar(positive=chosen, topn=1)[0][0] # Need to access the first element of a tuple in a list

        finalsentences.append(chosen)

    print(finalsentences[0])

create_rap("lyrics/eminem-rap-god.txt", model)
