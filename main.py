from strands_solver.grid import StrandsState
from strands_solver.search import StrandsSearch, StrandsGroupSearch
from typing import Set
from nltk.corpus import wordnet
import nltk
import time
from itertools import product
import marisa_trie
from src.strands_solver.puzzle_configs import PUZZLE_CONFIGS

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


# ALLOWING MULTIPLE PUZZLES

# def solve_puzzle(puzzle_name: str, dictionary, max_search_time: int = 300, max_solutions: int = 5):
#     """Solve a specific puzzle from the configurations"""
#     if puzzle_name not in PUZZLE_CONFIGS:
#         raise ValueError(f"Puzzle '{puzzle_name}' not found in configurations")
#
#     config = PUZZLE_CONFIGS[puzzle_name]
#     grid = config["grid"]
#     target_words = config["target_words"]
#     hint_words = config["hint_words"]
#
#     print(f"\nSolving puzzle: {puzzle_name}")
#     print("=" * 50)
#     print("\nGrid:")
#     for row in grid:
#         print(' '.join(row))
#
#     print(f"\nLooking for {len(target_words)} non-overlapping words")
#     print(f"Target words: {sorted(target_words)}")
#
#     solver = StrandsGroupSearch(
#         dictionary=dictionary,
#         target_words=target_words,
#         hint_words=hint_words,
#         min_word_length=4
#     )
#
#     print("\nStarting search...")
#     start_time = time.time()
#     groups = solver.find_word_groups(
#         grid=grid,
#         max_time=max_search_time
#     )
#
#     total_time = time.time() - start_time
#     print("\nSearch complete!")
#     print("=" * 50)
#     print(f"Found {len(groups)} potential groups in {total_time:.2f} seconds")
#
#     for i, group in enumerate(groups[:max_solutions]):
#         print(f"\nSolution {i + 1}:")
#         print("-" * 20)
#         group_score = solver.heuristic.calculate_group_score(group)
#         print(f"Score: {group_score:.3f}")
#
#         for word, path in zip(group.words, group.paths):
#             path_str = ' -> '.join(f"({r},{c})" for r, c in path)
#             print(f"{word:10} : {path_str}")
#
#     return groups
#
# def main():
#     print("Strands Word Group Solver")
#     print("=" * 50)
#
#     # Load dictionary once for all puzzles
#     dictionary = load_dictionary()
#     print(f"Loaded {len(dictionary)} words from WordNet")
#
#     # Show available puzzles
#     print("\nAvailable puzzles:")
#     for puzzle_name in PUZZLE_CONFIGS:
#         print(f"- {puzzle_name}")
#
#     # You can either solve specific puzzles or all of them
#     puzzles_to_solve = ["Strategy game"]  # Modify this list to solve specific puzzles
#     # puzzles_to_solve = PUZZLE_CONFIGS.keys()  # Uncomment to solve all puzzles
#
#     total_start_time = time.time()
#     for puzzle_name in puzzles_to_solve:
#         try:
#             solve_puzzle(puzzle_name, dictionary)
#         except Exception as e:
#             print(f"\nError solving puzzle '{puzzle_name}': {str(e)}")
#
#     total_time = time.time() - total_start_time
#     print(f"\nTotal time for all puzzles: {total_time:.2f} seconds")
#
#
# if __name__ == "__main__":
#     main()

# Define puzzle configurations

def solve_puzzle(puzzle_name: str, dictionary, max_iterations: int = 7, max_total_time: int = 500):
    """Solve a specific puzzle from the configurations"""
    if puzzle_name not in PUZZLE_CONFIGS:
        raise ValueError(f"Puzzle '{puzzle_name}' not found in configurations")

    config = PUZZLE_CONFIGS[puzzle_name]
    grid = config["grid"]
    target_words = config["target_words"]

    print(f"\nSolving puzzle: {puzzle_name}")
    print("=" * 50)

    print("\nGrid:")
    for row in grid:
        print(' '.join(row))

    solver = StrandsSearch(dictionary, min_word_length=4, heuristic_type='basic')
    found_words = set()
    excluded_positions = set()
    total_start_time = time.time()

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

    return found_words


def main():
    print("Strands Word Solver")
    print("=" * 50)

    dictionary = load_dictionary()
    print(f"Loaded {len(dictionary)} words from WordNet")

    # Show available puzzles
    print("\nAvailable puzzles:")
    for puzzle_name in PUZZLE_CONFIGS:
        print(f"- {puzzle_name}")

    # You can either solve specific puzzles or all of them
    puzzles_to_solve = ["Strategy game"]  # Modify this list to solve specific puzzles
    # puzzles_to_solve = PUZZLE_CONFIGS.keys()  # Uncomment to solve all puzzles

    total_start_time = time.time()
    for puzzle_name in puzzles_to_solve:
        try:
            solve_puzzle(puzzle_name, dictionary)
        except Exception as e:
            print(f"\nError solving puzzle '{puzzle_name}': {str(e)}")

    total_time = time.time() - total_start_time
    print(f"\nTotal time for all puzzles: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()

# Define puzzle configurations
PUZZLE_CONFIGS = {
    "Strategy game": {
        "grid": [
            ['O', 'O', 'C', 'K', 'H', 'T'],
            ['K', 'R', 'E', 'H', 'N', 'G'],
            ['D', 'O', 'B', 'C', 'S', 'I'],
            ['T', 'R', 'A', 'K', 'I', 'H'],
            ['I', 'G', 'M', 'B', 'P', 'O'],
            ['M', 'E', 'N', 'A', 'N', 'W'],
            ['N', 'R', 'U', 'I', 'T', 'A'],
            ['E', 'E', 'Q', 'K', 'E', 'P']
        ],
        "target_words": {"BISHOP", "BOARD", "KING", "KNIGHT", "PAWN", "QUEEN", "ROOK", "TIMER", "CHECKMATE"}
    },
    # Add other puzzles here
}


def solve_puzzle(puzzle_name: str, dictionary, max_iterations: int = 7, max_total_time: int = 500):
    """Solve a specific puzzle from the configurations"""
    if puzzle_name not in PUZZLE_CONFIGS:
        raise ValueError(f"Puzzle '{puzzle_name}' not found in configurations")

    config = PUZZLE_CONFIGS[puzzle_name]
    grid = config["grid"]
    target_words = config["target_words"]

    print(f"\nSolving puzzle: {puzzle_name}")
    print("=" * 50)

    print("\nGrid:")
    for row in grid:
        print(' '.join(row))

    solver = StrandsSearch(dictionary, min_word_length=4, heuristic_type='basic')
    found_words = set()
    excluded_positions = set()
    total_start_time = time.time()

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

    return found_words


def main():
    print("Strands Word Solver")
    print("=" * 50)

    dictionary = load_dictionary()
    print(f"Loaded {len(dictionary)} words from WordNet")

    # Show available puzzles
    print("\nAvailable puzzles:")
    for puzzle_name in PUZZLE_CONFIGS:
        print(f"- {puzzle_name}")

    # You can either solve specific puzzles or all of them
    puzzles_to_solve = ["Strategy game"]  # Modify this list to solve specific puzzles
    # puzzles_to_solve = PUZZLE_CONFIGS.keys()  # Uncomment to solve all puzzles

    total_start_time = time.time()
    for puzzle_name in puzzles_to_solve:
        try:
            solve_puzzle(puzzle_name, dictionary)
        except Exception as e:
            print(f"\nError solving puzzle '{puzzle_name}': {str(e)}")

    total_time = time.time() - total_start_time
    print(f"\nTotal time for all puzzles: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()

# def main():
#     total_start_time = time.time()
#
#     # grid = [
#     #     ['H', 'U', 'A', 'N', 'R', 'K'],
#     #     ['L', 'A', 'M', 'M', 'E', 'A'],
#     #     ['S', 'T', 'D', 'P', 'E', 'T'],
#     #     ['O', 'R', 'C', 'E', 'I', 'B'],
#     #     ['K', 'I', 'G', 'H', 'O', 'O'],
#     #     ['N', 'A', 'N', 'A', 'R', 'I'],
#     #     ['I', 'O', 'A', 'N', 'G', 'B'],
#     #     ['L', 'G', 'N', 'P', 'O', 'B']
#     # ]
#     #
#     # target_words = {"HUMAN", "MEERKAT", "BIPEDAL", "OSTRICH", "KANGAROO", "PANGOLIN", "GIBBON"}
#
#     grid = [['O', 'O', 'C', 'K', 'H', 'T'],
#     ['K', 'R', 'E', 'H', 'N', 'G'],
#     ['D', 'O', 'B', 'C', 'S', 'I'],
#     ['T', 'R', 'A', 'K', 'I', 'H'],
#     ['I', 'G', 'M', 'B', 'P', 'O'],
#     ['M', 'E', 'N', 'A', 'N', 'W'],
#     ['N', 'R', 'U', 'I', 'T', 'A'],
#     ['E', 'E', 'Q', 'K', 'E', 'P']]
#     target_words = {"BISHOP", "BOARD", "KING", "KNIGHT", "PAWN", "QUEEN", "ROOK", "TIMER", "CHECKMATE"}
#
#     excluded_positions = set()
#
#     print("\nSolving for grid:")
#     for row in grid:
#         print(' '.join(row))
#
#     dictionary = load_dictionary()
#     print(f"Loaded {len(dictionary)} words from WordNet")
#
#     solver = StrandsSearch(dictionary, min_word_length=4, heuristic_type='basic')
#     found_words = set()
#
#     max_iterations = 7
#     max_total_time = 500
#
#     for iteration in range(max_iterations):
#         print(f"\nIteration {iteration + 1}/{max_iterations}")
#         print(f"Still looking for: {target_words - found_words}")
#
#         all_positions = list(product(range(len(grid)), range(len(grid[0]))))
#
#         for pos in all_positions:
#             if time.time() - total_start_time > max_total_time:
#                 print("\nMaximum total time reached!")
#                 break
#
#             new_words = solver.search_from_position(grid, pos, target_words, excluded_positions, timeout=3)
#             found_words.update(new_words)
#
#             if len(found_words) == len(target_words):
#                 break
#
#         if len(found_words) == len(target_words):
#             break
#
#     total_time = time.time() - total_start_time
#     print("\nSearch complete!")
#     print(f"Found words: {found_words}")
#     print(f"Missing words: {target_words - found_words}")
#     print(f"Total words found: {len(found_words)}/{len(target_words)}")
#     print(f"Total time elapsed: {total_time:.2f} seconds")


# if __name__ == "__main__":
#     main()


# def main2():
#     grid = [
#         ['H', 'U', 'A', 'N', 'R', 'K'],
#         ['L', 'A', 'M', 'M', 'E', 'A'],
#         ['S', 'T', 'D', 'P', 'E', 'T'],
#         ['O', 'R', 'C', 'E', 'I', 'B'],
#         ['K', 'I', 'G', 'H', 'O', 'O'],
#         ['N', 'A', 'N', 'A', 'R', 'I'],
#         ['I', 'O', 'A', 'N', 'G', 'B'],
#         ['L', 'G', 'N', 'P', 'O', 'B']
#     ]
#
#     target_words = {"HUMAN", "MEERKAT", "BIPEDAL", "OSTRICH", "KANGAROO", "PANGOLIN", "GIBBON"}
#     required_word_count = len(target_words)
#
#     print("\nSolving for grid:")
#     for row in grid:
#         print(' '.join(row))
#
#     print(f"\nLooking for {required_word_count} words that don't share positions\n")
#
#     dictionary = load_dictionary()
#     print(f"Loaded {len(dictionary)} words from WordNet")
#
#     solver = StrandsGroupSearch(dictionary, required_word_count)
#     start_time = time.time()
#
#     groups = solver.find_word_groups(grid)
#
#     total_time = time.time() - start_time
#     print("\nSearch complete!")
#     print(f"Found {len(groups)} potential groups of {required_word_count} words")
#
#     for i, group in enumerate(groups):
#         print(f"\nGroup {i + 1}:")
#         for word, path in zip(group.words, group.paths):
#             path_str = ' -> '.join(f"({r},{c})" for r, c in path)
#             print(f"{word}: {path_str}")
#
#     print(f"\nTotal time elapsed: {total_time:.2f} seconds")
#
#
#     # if __name__ == "__main__":
#     #     main2()

# ALL AT ONCE

# def main():
#     total_start_time = time.time()
#
#     # Example grid
#     grid = [
#         ['H', 'U', 'A', 'N', 'R', 'K'],
#         ['L', 'A', 'M', 'M', 'E', 'A'],
#         ['S', 'T', 'D', 'P', 'E', 'T'],
#         ['O', 'R', 'C', 'E', 'I', 'B'],
#         ['K', 'I', 'G', 'H', 'O', 'O'],
#         ['N', 'A', 'N', 'A', 'R', 'I'],
#         ['I', 'O', 'A', 'N', 'G', 'B'],
#         ['L', 'G', 'N', 'P', 'O', 'B']
#     ]
#
#     # Target words - these are only used for semantic guidance, not validation
#     target_words = {"HUMAN", "MEERKAT", "BIPEDAL", "OSTRICH", "KANGAROO", "PANGOLIN", "GIBBON"}
#     hint_words = {"BIPEDAL"}
#
#     # Print problem setup
#     print("\nStrands Word Group Solver")
#     print("=" * 50)
#     print("\nGrid:")
#     for row in grid:
#         print(' '.join(row))
#
#     print(f"\nLooking for {len(target_words)} non-overlapping words")
#     print(f"Using target words for semantic guidance: {sorted(target_words)}")
#
#     # Load dictionary
#     print("\nInitializing solver...")
#     print("Loading dictionary...")
#     dictionary = load_dictionary()
#     print(f"Loaded {len(dictionary)} words from WordNet")
#
#     # Create solver
#     solver = StrandsGroupSearch(
#         dictionary=dictionary,
#         target_words=target_words,
#         hint_words=hint_words,
#         min_word_length=4
#     )
#
#     # Set search parameters
#     max_search_time = 300  # 5 minutes
#     max_solutions = 5
#
#     print(f"\nSearch parameters:")
#     print(f"- Maximum search time: {max_search_time} seconds")
#     print(f"- Maximum solutions to find: {max_solutions}")
#     print(f"- Minimum word length: {solver.min_word_length}")
#
#     # Run search
#     print("\nStarting search...")
#     groups = solver.find_word_groups(
#         grid=grid,
#         max_time=max_search_time
#     )
#
#     # Print results
#     total_time = time.time() - total_start_time
#     print("\nSearch complete!")
#     print("=" * 50)
#     print(f"Found {len(groups)} potential groups in {total_time:.2f} seconds")
#
#     # Print top solutions
#     for i, group in enumerate(groups[:max_solutions]):
#         print(f"\nSolution {i + 1}:")
#         print("-" * 20)
#         group_score = solver.heuristic.calculate_group_score(group)
#         print(f"Score: {group_score:.3f}")
#
#         for word, path in zip(group.words, group.paths):
#             path_str = ' -> '.join(f"({r},{c})" for r, c in path)
#             print(f"{word:10} : {path_str}")
#
#     # Print statistics
#     if not groups:
#         print("\nNo valid solutions found.")
#     else:
#         print("\nStatistics:")
#         print("-" * 20)
#         print(f"Total solutions found: {len(groups)}")
#         print(f"Average words per group: {sum(len(g.words) for g in groups) / len(groups):.1f}")
#         print(f"Average score: {sum(g.score for g in groups) / len(groups):.3f}")
#
#     print(f"\nTotal time elapsed: {total_time:.2f} seconds")


# if __name__ == "__main__":
#     main()