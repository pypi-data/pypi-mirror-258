# word_unscrambler.py

import enchant
from itertools import permutations

def unscramble(scrambled_word):
    """
    Unscrambles a word by generating all permutations of its letters
    and checking if each permutation corresponds to a valid English word.

    Args:
        scrambled_word (str): The scrambled word to unscramble.

    Returns:
        set: A set of valid unscrambled words.
    """
    scrambled_word = scrambled_word.lower()
    if not(scrambled_word.isalpha()):
        raise ValueError("May only contain letters")
    # Initialize the English dictionary
    dictionary = enchant.Dict("en_US")

    # Generate all permutations of the letters
    all_permutations = set(permutations(scrambled_word))

    # Check each permutation for valid words
    valid_words = set()
    for perm in all_permutations:
        word = "".join(perm)
        if dictionary.check(word):
            valid_words.add(word)

    return valid_words

if __name__ == "__main__":
    scrambled_input = input("Enter a scrambled word: ")
    valid_words = unscramble_word(scrambled_input)

    if valid_words:
        print(f"Valid words: {', '.join(valid_words)}")
    else:
        print("No valid words found.")
