# Starter code from https://stackoverflow.com/questions/46759492/syllable-count-in-python
def syllable_count(input):
    if not input:
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

# import re
#
# def syllable_count(word):
#     return len(
#         re.findall('(?!e$)[aeiouy]+', word, re.I) +
#         re.findall('^[^aeiouy]*e$', word, re.I)
#     )


print(syllable_count("Mmm, baby I don't understand this"))
print(syllable_count("took i'm of my money bitch her from his"))
print(syllable_count("You're changing, I can't stand it"))
print(syllable_count("My heart cant take"))
print(syllable_count("take"))

print("yoyoyo")
