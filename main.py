from strands_solver.grid import StrandsState
from strands_solver.search import StrandsSearch
from typing import Set
from nltk.corpus import wordnet
import nltk
import time
from itertools import product
import marisa_trie

def load_dictionary() -> Set[str]:
    """Load dictionary using WordNet"""
    try:
        nltk.find('corpora/wordnet')
    except LookupError:
        print("Downloading WordNet...")
        nltk.download('wordnet')

    print("Loading WordNet dictionary...")
    words = set()
    for word in wordnet.words():
        word = word.upper()
        if len(word) >= 4 and word.isalpha():
            words.add(word)

    return marisa_trie.Trie(words)


def main():
    total_start_time = time.time()

    grid = [
        ['H', 'U', 'A', 'N', 'R', 'K'],
        ['L', 'A', 'M', 'M', 'E', 'A'],
        ['S', 'T', 'D', 'P', 'E', 'T'],
        ['O', 'R', 'C', 'E', 'I', 'B'],
        ['K', 'I', 'G', 'H', 'O', 'O'],
        ['N', 'A', 'N', 'A', 'R', 'I'],
        ['I', 'O', 'A', 'N', 'G', 'B'],
        ['L', 'G', 'N', 'P', 'O', 'B']
    ]

    target_words = {"HUMAN", "MEERKAT", "BIPEDAL", "OSTRICH", "KANGAROO", "PANGOLIN", "GIBBON"}
    excluded_positions = set()

    print("\nSolving for grid:")
    for row in grid:
        print(' '.join(row))

    dictionary = load_dictionary()
    print(f"Loaded {len(dictionary)} words from WordNet")

    solver = StrandsSearch(dictionary, min_word_length=4, heuristic_type='basic')
    found_words = set()

    max_iterations = 7
    max_total_time = 500

    for iteration in range(max_iterations):
        print(f"\nIteration {iteration + 1}/{max_iterations}")
        print(f"Still looking for: {target_words - found_words}")

        all_positions = list(product(range(len(grid)), range(len(grid[0]))))

        for pos in all_positions:
            if time.time() - total_start_time > max_total_time:
                print("\nMaximum total time reached!")
                break

            new_words = solver.search_from_position(grid, pos, target_words, excluded_positions, timeout=3)
            found_words.update(new_words)

            if len(found_words) == len(target_words):
                break

        if len(found_words) == len(target_words):
            break

    total_time = time.time() - total_start_time
    print("\nSearch complete!")
    print(f"Found words: {found_words}")
    print(f"Missing words: {target_words - found_words}")
    print(f"Total words found: {len(found_words)}/{len(target_words)}")
    print(f"Total time elapsed: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()