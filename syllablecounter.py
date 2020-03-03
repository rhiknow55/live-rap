invalidtokens = [",", "(", ")", ";", "?", "!", ".", ":", "[", "]", "©"]

# Starter code from https://stackoverflow.com/questions/46759492/syllable-count-in-python
# input must be a single word, otherwise it cannot detect endswith()
def syllable_count(input):
    if not input or input in invalidtokens:
        return 0

    word = input.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e") and not word.endswith("le"):
        count -= 1
    if count == 0:
        count += 1
    return count

# import pronouncing
#
# # Input has to be a single word
# def syllable_count(input):
#     # Gets a list of phonetics
#     phones = pronouncing.phones_for_word(input)
#
#     return pronouncing.syllable_count(phones[0])

# Above failed because uses CMU word dictionary, which means certain words in lyrics don't exist
