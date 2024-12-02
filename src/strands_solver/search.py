from typing import Set, List, Tuple, Optional
from dataclasses import dataclass
import heapq
import time
from nltk.corpus import wordnet
import nltk
from itertools import product
import marisa_trie

#hi

from strands_solver.heuristics import HEURISTICS, BasicHeuristic


@dataclass
class SearchNode:
    state: 'StrandsState'
    g_score: float = 0
    h_score: float = 0
    parent: Optional['SearchNode'] = None

    @property
    def f_score(self) -> float:
        return self.g_score + self.h_score

    def __lt__(self, other: 'SearchNode') -> bool:
        return self.f_score < other.f_score


class StrandsState:
    def __init__(self, grid: List[List[str]]):
        self.grid = grid
        self.current_path: List[Tuple[int, int]] = []
        self.used_positions: Set[Tuple[int, int]] = set()

    def make_move(self, pos: Tuple[int, int]) -> None:
        self.current_path.append(pos)
        self.used_positions.add(pos)

    def get_current_word(self) -> str:
        return ''.join(self.grid[r][c] for r, c in self.current_path)

    def get_neighbors(self, pos: Tuple[int, int], excluded_positions: Set[Tuple[int, int]], dictionary) -> List[
        Tuple[int, int]]:
        if excluded_positions is None:
            excluded_positions = set()

        row, col = pos
        neighbors = []
        current_word = self.get_current_word()

        for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < len(self.grid) and
                    0 <= new_col < len(self.grid[0]) and
                    (new_row, new_col) not in self.used_positions and
                    (new_row, new_col) not in excluded_positions):

                # Check if adding this letter forms a valid prefix
                potential_word = current_word + self.grid[new_row][new_col]
                # Use trie's prefixes method to check if this could form a word
                if dictionary.keys(potential_word):  # This returns an iterator of words with this prefix
                    neighbors.append((new_row, new_col))

        return neighbors

class StrandsSearch:
    def __init__(self, dictionary: Set[str], min_word_length: int = 4, heuristic_type: str = 'basic'):
        self.dictionary = dictionary
        self.min_word_length = min_word_length
        self.found_words = set()

        # Get heuristic class from dictionary, default to basic if not found
        heuristic_class = HEURISTICS.get(heuristic_type, BasicHeuristic)
        self.heuristic = heuristic_class()

    def is_valid_word(self, word: str) -> bool:
        return len(word) >= self.min_word_length and word in self.dictionary

    def calculate_heuristic(self, word: str) -> float:
        return self.heuristic.calculate(word, self.dictionary, self.found_words)

    def search_from_position(self, grid: List[List[str]], start_pos: Tuple[int, int],
                             target_words: Set[str], excluded_positions: Set[Tuple[int, int]],
                             timeout: int = 2) -> Set[str]:
        """Search from a specific starting position with timeout"""
        if start_pos in excluded_positions:
            return set()

        start_time = time.time()

        def timeout_checker():
            return time.time() - start_time > timeout

        print(f"\nTrying start position: ({start_pos[0]}, {start_pos[1]}) - letter {grid[start_pos[0]][start_pos[1]]}")

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

            if self.is_valid_word(current_word) and current_word in target_words:
                current_time = time.time() - start_time
                path = [f"({r},{c})" for r, c in current.state.current_path]
                print(f"\n[{current_time:.2f}s] Found word: {current_word}")
                print(f"Path: {' -> '.join(path)}")
                found_words.add(current_word)
                self.found_words.add(current_word)  # Update found_words for heuristic
                excluded_positions.update(current.state.current_path)

            if not timeout_checker():
                current_pos = current.state.current_path[-1]
                for next_pos in current.state.get_neighbors(current_pos, excluded_positions, self.dictionary):
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
