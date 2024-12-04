# from typing import Set, List, Dict
# from main import WordChecker, search_from_position
# from strands_solver.search import StrandsSearch
# from strands_solver.grid import StrandsState
# import time
# from itertools import product
#
#
# class PuzzleTest:
#     def __init__(self, grid: List[List[str]], target_words: Set[str], name: str = ""):
#         self.grid = grid
#         self.target_words = target_words
#         self.name = name or f"Puzzle with words: {target_words}"
#
#
# def run_puzzle(puzzle: PuzzleTest) -> Dict:
#     """Run a single puzzle and return statistics"""
#     start_time = time.time()
#
#     print(f"\nTesting: {puzzle.name}")
#     print("Grid:")
#     for row in puzzle.grid:
#         print(' '.join(row))
#     print(f"Target words: {puzzle.target_words}")
#
#     checker = WordChecker(puzzle.target_words, start_time)
#     solver = StrandsSearch(set(), min_word_length=4)  # Empty dictionary since we're using target words
#
#     height = len(puzzle.grid)
#     width = len(puzzle.grid[0])
#     all_positions = list(product(range(height), range(width)))
#
#     for pos in all_positions:
#         search_from_position(solver, puzzle.grid, checker, pos, timeout=3)
#         if len(checker.found_words) == checker.total_words:
#             break
#
#     end_time = time.time()
#     total_time = end_time - start_time
#
#     results = {
#         "puzzle_name": puzzle.name,
#         "total_time": total_time,
#         "found_words": checker.found_words,
#         "missing_words": puzzle.target_words - checker.found_words,
#         "success": len(checker.found_words) == len(puzzle.target_words)
#     }
#
#     return results
#
#
# # Define some test puzzles
# TEST_PUZZLES = [
#     PuzzleTest(
#         grid=[
#             ['A', 'L', 'C', 'P', 'E', 'A'],
#             ['C', 'R', 'E', 'L', 'O', 'C'],
#             ['S', 'T', 'O', 'U', 'G', 'C'],
#             ['C', 'R', 'E', 'R', 'E', 'K'],
#             ['H', 'S', 'U', 'S', 'P', 'E'],
#             ['U', 'I', 'D', 'E', 'N', 'U'],
#             ['S', 'M', 'C', 'T', 'L', 'M'],
#             ['T', 'A', 'R', 'D', 'S', 'P']
#         ],
#         target_words={"CLUESUSPECTS", "SCARLET", "MUSTARD", "PEACOCK", "GREEN", "PLUM", "ORCHID"},
#         name="Clue Puzzle"
#     ),
#     PuzzleTest(
#         grid=[
#             ['O', 'N', 'A', 'H', 'O', 'R'],
#             ['G', 'R', 'T', 'C', 'E', 'O'],
#             ['B', 'L', 'A', 'V', 'O', 'T'],
#             ['A', 'T', 'P', 'H', 'C', 'I'],
#             ['O', 'X', 'A', 'N', 'A', 'V'],
#             ['T', 'O', 'F', 'D', 'B', 'T'],
#             ['T', 'R', 'E', 'F', 'E', 'G'],
#             ['O', 'L', 'T', 'A', 'L', 'O']
#         ],
#         target_words={"TANGO", "VICTOR", "ECHO", "BRAVO", "NATOALPHABET", "FOXTROT", "GOLF", "DELTA"},
#         name="NATO Puzzle"
#     )
# ]
#
#
# def run_all_tests():
#     """Run all test puzzles and display results"""
#     total_start = time.time()
#     results = []
#
#     for puzzle in TEST_PUZZLES:
#         result = run_puzzle(puzzle)
#         results.append(result)
#
#         print(f"\nResults for {result['puzzle_name']}:")
#         print(f"Time taken: {result['total_time']:.2f} seconds")
#         print(f"Found words: {result['found_words']}")
#         if result['missing_words']:
#             print(f"Missing words: {result['missing_words']}")
#         print(f"Success: {result['success']}")
#         print("-" * 50)
#
#     total_time = time.time() - total_start
#     successful = sum(1 for r in results if r['success'])
#
#     print("\nOverall Results:")
#     print(f"Total puzzles: {len(TEST_PUZZLES)}")
#     print(f"Successful solves: {successful}")
#     print(f"Total time: {total_time:.2f} seconds")
#
#     return results
#
#
# if __name__ == "__main__":
#     run_all_tests()