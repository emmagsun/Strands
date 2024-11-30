# from typing import List, Set, Tuple, Optional
# from dataclasses import dataclass
# import heapq
# from .grid import StrandsState  # Using relative import

from strands_solver.grid import StrandsState
from strands_solver.heuristics import HEURISTICS, BasicHeuristic
from typing import List, Set, Tuple, Optional
from dataclasses import dataclass
import heapq

@dataclass
class SearchNode:
    state: StrandsState
    g_score: float = 0  # Cost so far
    h_score: float = 0  # Heuristic estimate
    parent: Optional['SearchNode'] = None

    @property
    def f_score(self) -> float:
        return self.g_score + self.h_score

    def __lt__(self, other: 'SearchNode') -> bool:
        return self.f_score < other.f_score

class StrandsSearch:
    def __init__(self, dictionary: Set[str], min_word_length: int = 4, heuristic_type: str = 'semantic'):
        self.dictionary = dictionary
        self.min_word_length = min_word_length
        self.found_words = set()

        # Get heuristic class from dictionary, default to basic if not found
        heuristic_class = HEURISTICS.get(heuristic_type, BasicHeuristic)
        self.heuristic = heuristic_class()

    def is_valid_word(self, word: str) -> bool:
        """Check if word is in dictionary and meets length requirement"""
        return len(word) >= self.min_word_length and word in self.dictionary

    def calculate_heuristic(self, word: str) -> float:
        return self.heuristic.calculate(word, self.dictionary, self.found_words)

# THIS WORKED
# class StrandsSearch:
#     def __init__(self, dictionary: Set[str], min_word_length: int = 4):
#         self.dictionary = dictionary
#         self.min_word_length = min_word_length
#
#     def is_valid_word(self, word: str) -> bool:
#         """Check if word is in dictionary and meets length requirement"""
#         return len(word) >= self.min_word_length and word in self.dictionary
#
#     def calculate_heuristic(self, word: str) -> float:
#         """
#         Calculate heuristic score for a word.
#         Lower score is better.
#         """
#         # Aggressive pruning for longer paths
#         if len(word) > 8:  # Adjust this number based on typical Strands word length
#             return float('inf')
#
#         # Count how many dictionary words start with this prefix
#         potential_words = sum(1 for dict_word in self.dictionary
#                               if dict_word.startswith(word))
#
#         if potential_words == 0:
#             return float('inf')  # No words possible, prune this path
#
#         # More aggressive scoring
#         if len(word) < 4:
#             return 1000
#
#         # Strongly prefer words of typical Strands length (4-8 letters)
#         if word in self.dictionary:
#             if 4 <= len(word) <= 8:
#                 return -len(word) * 2
#             else:
#                 return 0
#
#         # Penalize very long prefixes that aren't words
#         if len(word) > 6 and word not in self.dictionary:
#             return 500
#
#         return -potential_words / len(word)  # Balance potential words with length

    # def search_with_timeout(self, grid, check_word_callback, start_pos, timeout_checker):
    #     """A* search from a specific starting position with timeout"""
    #     initial_state = StrandsState(grid)
    #     initial_state.make_move(start_pos)
    #
    #     start_node = SearchNode(initial_state)
    #     queue = [start_node]
    #     heapq.heapify(queue)
    #
    #     found_words = set()
    #
    #     while queue:
    #         # Check timeout
    #         if timeout_checker():
    #             print(f"Timeout reached for position {start_pos}")
    #             return found_words
    #
    #         current = heapq.heappop(queue)
    #         current_word = current.state.get_current_word()
    #
    #         if self.is_valid_word(current_word):
    #             if check_word_callback(current_word):
    #                 found_words.add(current_word)
    #
    #         if not timeout_checker():  # Check timeout before exploring neighbors
    #             current_pos = current.state.current_path[-1]
    #             for next_pos in current.state.get_neighbors(current_pos):
    #                 # Create new state with this move
    #                 new_state = StrandsState(grid)
    #                 new_state.current_path = current.state.current_path.copy()
    #                 new_state.used_positions = current.state.used_positions.copy()
    #                 new_state.make_move(next_pos)
    #
    #                 # Create new search node
    #                 new_node = SearchNode(
    #                     state=new_state,
    #                     g_score=current.g_score + 1,
    #                     parent=current
    #                 )
    #
    #                 # Calculate heuristic score
    #                 new_word = new_state.get_current_word()
    #                 new_node.h_score = self.calculate_heuristic(new_word)
    #
    #                 heapq.heappush(queue, new_node)
    #
    #     return found_words

    # def search_with_timeout(self, grid, check_word_callback, start_pos, timeout_checker, used_positions):
    #     """A* search from a specific starting position with timeout"""
    #     initial_state = StrandsState(grid)
    #     initial_state.make_move(start_pos)
    #
    #     start_node = SearchNode(initial_state)
    #     queue = [start_node]
    #     heapq.heapify(queue)
    #
    #     found_words = set()
    #
    #     while queue:
    #         if timeout_checker():
    #             return found_words
    #
    #         current = heapq.heappop(queue)
    #         current_word = current.state.get_current_word()
    #
    #         if self.is_valid_word(current_word):
    #             # NEW: Set current path before checking word
    #             check_word_callback.current_path = current.state.current_path
    #             if check_word_callback(current_word):
    #                 found_words.add(current_word)
    #
    #         if not timeout_checker():
    #             current_pos = current.state.current_path[-1]
    #             # NEW: Pass used_positions to get_neighbors
    #             for next_pos in current.state.get_neighbors(current_pos, used_positions):
    #                 new_state = StrandsState(grid)
    #                 new_state.current_path = current.state.current_path.copy()
    #                 new_state.used_positions = current.state.used_positions.copy()
    #                 new_state.make_move(next_pos)
    #
    #                 new_node = SearchNode(
    #                     state=new_state,
    #                     g_score=current.g_score + 1,
    #                     parent=current
    #                 )
    #
    #                 new_word = new_state.get_current_word()
    #                 new_node.h_score = self.calculate_heuristic(new_word)
    #
    #                 heapq.heappush(queue, new_node)
    #
    #     return found_words

    def search_with_timeout(self, grid, checker, start_pos, timeout_checker, used_positions):
        """A* search from a specific starting position with timeout"""
        initial_state = StrandsState(grid)
        initial_state.make_move(start_pos)

        start_node = SearchNode(initial_state)
        queue = [start_node]
        heapq.heapify(queue)

        found_words = set()

        while queue:
            if timeout_checker():
                return found_words

            current = heapq.heappop(queue)
            current_word = current.state.get_current_word()

            if self.is_valid_word(current_word):
                # Set current path on the checker object
                checker.current_path = current.state.current_path
                if checker.is_correct_word(current_word):
                    found_words.add(current_word)

            if not timeout_checker():
                current_pos = current.state.current_path[-1]
                for next_pos in current.state.get_neighbors(current_pos, used_positions):
                    new_state = StrandsState(grid)
                    new_state.current_path = current.state.current_path.copy()
                    new_state.used_positions = current.state.used_positions.copy()
                    new_state.make_move(next_pos)

                    new_node = SearchNode(
                        state=new_state,
                        g_score=current.g_score + 1,
                        parent=current
                    )

                    new_word = new_state.get_current_word()
                    new_node.h_score = self.calculate_heuristic(new_word)

                    heapq.heappush(queue, new_node)

        return found_words

    def search(self, grid: List[List[str]], check_word_callback) -> Set[str]:
        """
        Original search method - kept for compatibility.
        Better to use search_with_timeout for new code.
        """
        found_words = set()

        # Try starting from each position
        for start_row in range(len(grid)):
            for start_col in range(len(grid[0])):
                # Initialize search from this position
                start_pos = (start_row, start_col)
                initial_state = StrandsState(grid)
                initial_state.make_move(start_pos)

                # Priority queue for A* search
                start_node = SearchNode(initial_state)
                queue = [start_node]
                heapq.heapify(queue)

                while queue:
                    current = heapq.heappop(queue)
                    current_word = current.state.get_current_word()

                    # Check if current word is valid
                    if self.is_valid_word(current_word):
                        if check_word_callback(current_word):
                            found_words.add(current_word)

                    # Explore neighbors
                    current_pos = current.state.current_path[-1]
                    for next_pos in current.state.get_neighbors(current_pos):
                        # Create new state with this move
                        new_state = StrandsState(grid)
                        new_state.current_path = current.state.current_path.copy()
                        new_state.used_positions = current.state.used_positions.copy()
                        new_state.make_move(next_pos)

                        # Create new search node
                        new_node = SearchNode(
                            state=new_state,
                            g_score=current.g_score + 1,
                            parent=current
                        )

                        # Calculate heuristic score
                        new_word = new_state.get_current_word()
                        new_node.h_score = self.calculate_heuristic(new_word)

                        heapq.heappush(queue, new_node)

        return found_words