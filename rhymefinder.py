import pronouncing
from random import randint

def rhyme_words(input):
    words = pronouncing.rhymes(input)

    if not words:
        return False

    # choose randomly
    index = randint(0, len(words) - 1)
    return words[index]


def is_rhyme(input1, input2):
    words = pronouncing.rhymes(input1)

    if words:
        return input2 in words

    return False



# from Phyme import Phyme
#
# ph = Phyme()
#
# def rhyme_words(input):
#     return ph.get_perfect_rhymes(input)
