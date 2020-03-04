# Ignore warnings until profanity is fixed
import warnings
warnings.filterwarnings("ignore")

from profanity_check import predict, predict_prob

profanitydict = {}

def is_profanity(input):
    if input in profanitydict.keys():
        return profanitydict[input]

    p1 = predict([input])

    # removing the last letter, in case a "s" is there
    p2 = predict([input[:-1]])

    isprofane = p1 or p2

    # Add to dict
    profanitydict[input] = isprofane

    return isprofane
