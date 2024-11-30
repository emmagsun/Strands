from strands_solver.grid import StrandsState
from strands_solver.search import StrandsSearch
from typing import Set
from nltk.corpus import wordnet
import nltk
import time
from itertools import product


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
        # Convert to uppercase and filter by length
        word = word.upper()
        if len(word) >= 4 and word.isalpha():  # Only pure letters, no hyphens etc
            words.add(word)
    return words


# class WordChecker:
#     def __init__(self, target_words: Set[str], start_time: float):
#         self.target_words = {word.upper() for word in target_words}  # Convert to uppercase
#         self.checked_words = {}
#         self.found_words = set()
#         self.total_words = len(target_words)
#         self.start_time = start_time
#         print(f"Looking for {self.total_words} words: {self.target_words}")
#
#     def is_correct_word(self, word: str) -> bool:
#         if len(word) < 4:
#             return False
#
#         if word in self.checked_words:
#             return self.checked_words[word]
#
#         # Automatically check against target words
#         is_correct = word in self.target_words
#         self.checked_words[word] = is_correct
#
#         if is_correct:
#             elapsed_time = time.time() - self.start_time
#             self.found_words.add(word)
#             print(f"\nFound word: {word} (Time elapsed: {elapsed_time:.2f} seconds)")
#             print(f"Current found words ({len(self.found_words)}/{self.total_words}): {self.found_words}")
#             if len(self.found_words) == self.total_words:
#                 print(f"\nFound all words! Success! Total time: {elapsed_time:.2f} seconds")
#                 print(f"Final found words: {self.found_words}")
#                 exit(0)
#
#         return is_correct

class WordChecker:
    def __init__(self, target_words: Set[str], start_time: float):
        self.target_words = {word.upper() for word in target_words}
        self.checked_words = {}
        self.found_words = set()
        self.used_positions = set()  # NEW: Track all used positions
        self.current_path = []       # NEW: Track current path being checked
        self.total_words = len(target_words)
        self.start_time = start_time
        print(f"Looking for {self.total_words} words: {self.target_words}")

    def is_correct_word(self, word: str) -> bool:
        if len(word) < 4:
            return False

        if word in self.checked_words:
            return self.checked_words[word]

        # Automatically check against target words
        is_correct = word in self.target_words
        self.checked_words[word] = is_correct

        if is_correct:
            self.found_words.add(word)
            # NEW: Add current path positions to used positions
            self.used_positions.update(self.current_path)
            elapsed_time = time.time() - self.start_time
            print(f"\nFound word: {word} (Time elapsed: {elapsed_time:.2f} seconds)")
            print(f"Current found words ({len(self.found_words)}/{self.total_words}): {self.found_words}")
            print(f"Positions now excluded: {self.used_positions}")  # NEW: Show excluded positions
            if len(self.found_words) == self.total_words:
                print(f"\nFound all words! Success! Total time: {elapsed_time:.2f} seconds")
                print(f"Final found words: {self.found_words}")
                exit(0)

        return is_correct
# def search_from_position(solver, grid, checker, start_pos, timeout=2):
#     """Search from a specific starting position with timeout"""
#     start_time = time.time()
#
#     def timeout_checker():
#         if time.time() - start_time > timeout:
#             print(f"Timeout reached for position {start_pos}")
#             return True
#         return False
#
#     print(f"\nTrying start position: ({start_pos[0]}, {start_pos[1]}) - letter {grid[start_pos[0]][start_pos[1]]}")
#     found = solver.search_with_timeout(grid, checker.is_correct_word, start_pos, timeout_checker)
#     return found
def search_from_position(solver, grid, checker, start_pos, timeout=2):
    """Search from a specific starting position with timeout"""
    # Skip if position is already used
    if start_pos in checker.used_positions:
        return set()

    start_time = time.time()

    def timeout_checker():
        if time.time() - start_time > timeout:
            return True
        return False

    print(f"\nTrying start position: ({start_pos[0]}, {start_pos[1]}) - letter {grid[start_pos[0]][start_pos[1]]}")
    # Pass the whole checker object instead of just the method
    found = solver.search_with_timeout(grid, checker, start_pos, timeout_checker, checker.used_positions)
    return found

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

    height = len(grid)
    width = len(grid[0])

    print("\nSolving for grid:")
    for row in grid:
        print(' '.join(row))

    dictionary = load_dictionary()
    print(f"Loaded {len(dictionary)} words from WordNet")

    solver = StrandsSearch(dictionary, min_word_length=4, heuristic_type='semantic')
    checker = WordChecker(target_words, total_start_time)
    # checker = WordChecker(target_words, total_start_time)
    # solver = StrandsSearch(dictionary, min_word_length=4)

    print("\nSearching for words automatically...")

    max_iterations = 7  # Number of times to try all positions
    max_total_time = 500  # 5 minutes maximum

    for iteration in range(max_iterations):
        print(f"\nIteration {iteration + 1}/{max_iterations}")
        print(f"Still looking for: {target_words - checker.found_words}")

        # Try all starting positions
        all_positions = list(product(range(height), range(width)))
        # Randomize positions each iteration to try different paths
        import random
        random.shuffle(all_positions)

        for pos in all_positions:
            if time.time() - total_start_time > max_total_time:
                print("\nMaximum total time reached!")
                break

            search_from_position(solver, grid, checker, pos, timeout=3)  # Increased timeout

            # Print remaining words occasionally
            if random.random() < 0.1:  # 10% chance to print status
                print(f"Still looking for: {target_words - checker.found_words}")

        if len(checker.found_words) == checker.total_words:
            break

    total_time = time.time() - total_start_time
    print("\nSearch complete!")
    print(f"Found words: {checker.found_words}")
    print(f"Missing words: {target_words - checker.found_words}")
    print(f"Total words found: {len(checker.found_words)}/{checker.total_words}")
    print(f"Total time elapsed: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()

