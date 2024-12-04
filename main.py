from strands_solver.search import StrandsSearch, StrandsGroupSearch
from nltk.corpus import wordnet
import nltk
import time
import marisa_trie
from src.strands_solver.puzzle_configs import PUZZLE_CONFIGS
from enum import Enum
from typing import Set, Any

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

class SearchMethod(Enum):
    GROUP = "group"
    ITERATIVE = "iterative"


def solve_puzzle(
        puzzle_name: str,
        dictionary: Set[str],
        search_method: SearchMethod,
        max_time: int = 300,
        max_solutions: int = 5,
        max_iterations: int = 7
) -> Any:
    """
    Solve a puzzle using either group or iterative search method.
    """
    if puzzle_name not in PUZZLE_CONFIGS:
        raise ValueError(f"Puzzle '{puzzle_name}' not found in configurations")

    config = PUZZLE_CONFIGS[puzzle_name]
    grid = config["grid"]
    target_words = config["target_words"]
    hint_words = config.get("hint_words", set())

    print(f"\nSolving puzzle: {puzzle_name}")
    print("=" * 50)
    print("\nGrid:")
    for row in grid:
        print(' '.join(row))

    if search_method == SearchMethod.ITERATIVE:
        solver = StrandsGroupSearch(
            dictionary=dictionary,
            target_words=target_words,
            hint_words=hint_words,
            min_word_length=4
        )
        return solver.find_word_groups(grid=grid, max_time=max_time)
    else:
        solver = StrandsSearch(dictionary, min_word_length=4, heuristic_type='basic')
        return solver.search_iterative(grid, target_words, max_iterations, max_time)


def main():
    print("Strands Word Solver")
    print("=" * 50)

    dictionary = load_dictionary()
    print(f"Loaded {len(dictionary)} words from WordNet")

    # Configure solver settings
    search_method = SearchMethod.GROUP  # Switch between GROUP and ITERATIVE here
    puzzles_to_solve = list(PUZZLE_CONFIGS.keys())
    # puzzles_to_solve = ["world piece"]
    max_solutions = 1
    total_start_time = time.time()
    for puzzle_name in puzzles_to_solve:
        try:
            results = solve_puzzle(puzzle_name, dictionary, search_method)

            if search_method == SearchMethod.GROUP:
                print(f"\nFound {len(results)} potential groups")
                for i, group in enumerate(results[:max_solutions]):
                    print(f"\nSolution {i + 1}:")
                    print("-" * 20)
                    for word, path in zip(group.words, group.paths):
                        path_str = ' -> '.join(f"({r},{c})" for r, c in path)
                        print(f"{word:10} : {path_str}")
            else:
                print(f"\nFound words: {results}")

        except Exception as e:
            print(f"\nError solving puzzle '{puzzle_name}': {str(e)}")

    total_time = time.time() - total_start_time
    print(f"\nTotal time for all puzzles: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()









