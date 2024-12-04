from typing import Set, List, Tuple, Optional
from dataclasses import dataclass
import heapq
import time
from nltk.corpus import wordnet
import nltk
from itertools import product
import marisa_trie



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

    def search_iterative(self, grid: List[List[str]], target_words: Set[str],
                         max_iterations: int = 7, max_time: int = 500) -> Set[str]:
        """Iterative search method"""
        found_words = set()
        excluded_positions = set()
        total_start_time = time.time()

        for iteration in range(max_iterations):
            print(f"\nIteration {iteration + 1}/{max_iterations}")
            print(f"Still looking for: {target_words - found_words}")

            if time.time() - total_start_time > max_time:
                print("\nMaximum total time reached!")
                break

            all_positions = list(product(range(len(grid)), range(len(grid[0]))))
            for pos in all_positions:
                new_words = self.search_from_position(grid, pos, target_words, excluded_positions, timeout=3)
                found_words.update(new_words)
                if len(found_words) == len(target_words):
                    break

            if len(found_words) == len(target_words):
                break

        return found_words

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




##################


import gensim.downloader as gensim_downloader
from typing import Set, List, Tuple, Optional, Dict
from dataclasses import dataclass
import heapq
import time
from nltk.corpus import wordnet
import nltk
from itertools import product
import marisa_trie
import numpy as np


@dataclass
class WordGroup:
    words: List[str]
    paths: List[List[Tuple[int, int]]]
    used_positions: Set[Tuple[int, int]]
    score: float = 0

    def can_add_word(self, word: str, path: List[Tuple[int, int]]) -> bool:
        return not (self.used_positions & set(path))

    def add_word(self, word: str, path: List[Tuple[int, int]]):
        self.words.append(word)
        self.paths.append(path)
        self.used_positions.update(path)

    def copy(self) -> 'WordGroup':
        return WordGroup(
            words=self.words.copy(),
            paths=[path.copy() for path in self.paths],
            used_positions=self.used_positions.copy(),
            score=self.score
        )

    def __lt__(self, other: 'WordGroup'):
        return self.score < other.score


from collections import Counter
import nltk
from nltk.corpus import brown


class SemanticHeuristic:
    def __init__(self, target_words: Set[str]):
        self.target_words = target_words
        print("Loading word vectors...")
        self.word_vectors = gensim_downloader.load('word2vec-google-news-300')
        print("Word vectors loaded")

        # Pre-compute target word vectors
        self.target_vectors = {}
        for word in target_words:
            word_lower = word.lower()
            if word_lower in self.word_vectors:
                self.target_vectors[word] = self.word_vectors[word_lower]

        # Load word frequencies from Brown corpus
        print("Loading word frequencies...")
        try:
            words = brown.words()
        except LookupError:
            nltk.download('brown')
            words = brown.words()

        # Create frequency dictionary
        word_counts = Counter(word.lower() for word in words)
        total_words = sum(word_counts.values())

        # Convert to frequency
        self.word_frequencies = {
            word: count / total_words
            for word, count in word_counts.items()
        }
        print("Word frequencies loaded")

        # Set minimum frequency for unknown words
        self.min_frequency = 1.0 / total_words

        sorted_freqs = sorted(self.word_frequencies.values(), reverse=True)
        freq_threshold_idx = len(sorted_freqs) // 100  # top 1%
        self.freq_threshold = sorted_freqs[freq_threshold_idx]

    def get_word_frequency_score(self, word: str) -> float:
        """
        Get frequency-based score for a word.
        """
        if self.word_frequencies.get(word.lower(), self.min_frequency) > self.freq_threshold:
            return -np.log(self.freq_threshold) + 1

        return -np.log(self.word_frequencies.get(word.lower(), self.min_frequency))

    def calculate_group_score(self, group: WordGroup) -> float:
        """
        Calculate group score where LOWER is better.
        Combines semantic similarity and word frequency.
        """
        if not group.words:
            return float('inf')

        # Calculate semantic similarity score
        total_similarity = 0
        words_scored = 0

        for word in group.words:
            word_lower = word.lower()
            if word_lower in self.word_vectors:
                word_vec = self.word_vectors[word_lower]
                # Find max similarity to any target word
                word_score = max(
                    np.dot(word_vec, target_vec)
                    for target_vec in self.target_vectors.values()
                )
                total_similarity += word_score

            words_scored += 1

        # total_similarity = 0
        # num_pairs = 0

        # for i, word1 in enumerate(group.words):
        #     word1_lower = word1.lower()
        #     # Get vector for first word if it exists
        #     if word1_lower not in self.word_vectors:
        #         continue
        #
        #     word1_vec = self.word_vectors[word1_lower]
        #
        #     # Compare with all other words that come after it
        #     for word2 in group.words[i + 1:]:
        #         word2_lower = word2.lower()
        #         if word2_lower not in self.word_vectors:
        #             continue
        #
        #         word2_vec = self.word_vectors[word2_lower]
        #         similarity = np.dot(word1_vec, word2_vec)
        #         total_similarity += similarity
        #         num_pairs += 1

        avg_similarity = total_similarity / words_scored if words_scored > 0 else 0
        # avg_similarity = total_similarity / num_pairs if num_pairs > 0 else 0

        # Calculate frequency score (average of log frequencies)
        # breakpoint()
        freq_score = sum(self.get_word_frequency_score(word) for word in group.words) / len(group.words)

        size_penalty = (len(self.target_words) - len(group.words)) * 0.5
        length_penalty = sum(len(w) for w in group.words) * 0.1

        return (
                -avg_similarity * 1.0 +  # Higher similarity = lower score
                size_penalty * 0.1 +  # Fewer words = higher score
                -length_penalty * 0.5 +  # Longer words = higher score
                freq_score * 0.2  # Less common words = higher score
        )

        # Combine scores with weights
        # semantic_weight = 1.0
        # frequency_weight = 0.0
        # size_weight = 0.0
        # length_weight = 0.0
        #
        # size_penalty = (len(self.target_words) - len(group.words)) * size_weight
        # length_penalty = sum(len(w) for w in group.words) * length_weight
        #
        # # Note: Lower score is better
        # final_score = (
        #         -avg_similarity * semantic_weight +  # Negative because higher similarity is better
        #         avg_frequency_score * frequency_weight +
        #         size_penalty +
        #         length_penalty
        # )

        # return final_score


@dataclass
class WordWithPath:
    word: str
    path: List[Tuple[int, int]]
    positions: Set[Tuple[int, int]]


class StrandsGroupSearch:
    def __init__(self, dictionary: Set[str], hint_words, target_words: Set[str], min_word_length: int = 4):
        self.dictionary = dictionary
        self.min_word_length = min_word_length
        self.required_word_count = len(target_words)
        self.target_words = target_words
        self.found_groups: List[WordGroup] = []
        self.heuristic = SemanticHeuristic(hint_words)
        self.all_valid_words: List[WordWithPath] = []

    def is_valid_word(self, word: str) -> bool:
        return len(word) >= self.min_word_length and word in self.dictionary

    def precompute_words(self, grid: List[List[str]]):
        """Precompute all valid words and their paths in the grid"""
        height, width = len(grid), len(grid[0])
        print("Precomputing all valid words...")
        start_time = time.time()

        def explore(pos: Tuple[int, int], current_word: str, path: List[Tuple[int, int]], used: Set[Tuple[int, int]]):
            row, col = pos
            new_word = current_word + grid[row][col]
            new_path = path + [pos]

            # Check if this prefix could lead to any words using the trie
            if not self.dictionary.keys(new_word):
                return

            if self.is_valid_word(new_word):
                self.all_valid_words.append(WordWithPath(
                    word=new_word,
                    path=new_path,
                    positions=set(new_path)
                ))

            # Explore neighbors
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                new_row, new_col = row + dr, col + dc
                new_pos = (new_row, new_col)
                if (0 <= new_row < height and
                        0 <= new_col < width and
                        new_pos not in used):
                    explore(new_pos, new_word, new_path, used | {new_pos})

        # Start from each position
        for row in range(height):
            for col in range(width):
                if self.dictionary.keys(grid[row][col]):  # Only start if first letter could form word
                    explore((row, col), "", [], set())

        elapsed = time.time() - start_time
        print(f"Found {len(self.all_valid_words)} valid words in {elapsed:.2f} seconds")

    def get_compatible_words(self, used_positions: Set[Tuple[int, int]]) -> List[WordWithPath]:
        """Get all precomputed words that don't use any of the given positions"""
        return [
            word_info for word_info in self.all_valid_words
            if not (word_info.positions & used_positions)
        ]

    # def find_word_groups(self, grid: List[List[str]], max_time: int = 300) -> List[WordGroup]:
    #     """Find groups of N words using best-first search guided by semantic similarity"""
    #     start_time = time.time()
    #
    #     def is_timeout():
    #         return time.time() - start_time > max_time
    #
    #     # First, precompute all valid words
    #     if not self.all_valid_words:
    #         self.precompute_words(grid)
    #
    #     # Initialize search with empty group
    #     initial_group = WordGroup(words=[], paths=[], used_positions=set())
    #     queue = [(0, 0, initial_group)]  # (priority, tiebreaker, group)
    #     seen_words = set()
    #     counter = 1
    #
    #     while queue and not is_timeout():
    #         _, _, current_group = heapq.heappop(queue)
    #
    #         if len(current_group.words) == self.required_word_count:
    #             if set(current_group.words) == self.target_words:
    #                 elapsed = time.time() - start_time
    #                 print(f"\n[{elapsed:.2f}s] Found correct solution!")
    #                 print(f"Words: {current_group.words}")
    #                 self.found_groups = [current_group.copy()]
    #                 return self.found_groups
    #
    #             self.found_groups.append(current_group.copy())
    #             elapsed = time.time() - start_time
    #             print(f"\n[{elapsed:.2f}s] Found potential group: {current_group.words}")
    #             continue
    #
    #         # Get compatible words from precomputed list
    #         compatible_words = self.get_compatible_words(current_group.used_positions)
    #
    #         # Try adding each compatible word
    #         for word_info in compatible_words:
    #             new_group = current_group.copy()
    #             new_group.add_word(word_info.word, word_info.path)
    #
    #             # Check if we've seen this combination
    #             word_combo = frozenset(new_group.words)
    #             if word_combo in seen_words:
    #                 continue
    #             seen_words.add(word_combo)
    #
    #             # Score the new group
    #             score = self.heuristic.calculate_group_score(new_group)
    #             new_group.score = score
    #
    #             heapq.heappush(queue, (score, counter, new_group))
    #             counter += 1
    #
    #     return self.found_groups
    def find_word_groups(self, grid: List[List[str]], max_time: int = 300) -> List[WordGroup]:
        if not self.all_valid_words:
            self.precompute_words(grid)

        start_time = time.time()
        initial_group = WordGroup(words=[], paths=[], used_positions=set())

        # Initialize priority queue with (score, tiebreaker, group)
        # Remember: heapq is a min-heap, so lower scores are popped first
        queue = [(0, 0, initial_group)]
        seen_words = set()
        counter = 1

        print("\nStarting search...")
        last_report_time = time.time()
        groups_checked = 0

        while queue and (time.time() - start_time < max_time):
            # Progress reporting
            groups_checked += 1
            current_time = time.time()
            if current_time - last_report_time > 5:  # Report every 5 seconds
                print(f"[{current_time - start_time:.1f}s] Checked {groups_checked} groups, queue size: {len(queue)}")
                last_report_time = current_time

            score, _, current_group = heapq.heappop(queue)

            # Debug scoring occasionally
            if groups_checked % 1000 == 0:
                print(f"\nExample group score: {score:.3f}")
                print(f"Words: {current_group.words}")

            if len(current_group.words) == self.required_word_count:
                if set(current_group.words) == self.target_words:
                    print(f"\n[{current_time - start_time:.2f}s] Found correct solution!")
                    print(f"Words: {current_group.words}")
                    return [current_group]
                continue

            compatible_words = self.get_compatible_words(current_group.used_positions)
            # breakpoint()

            for word_info in compatible_words:
                new_group = current_group.copy()
                new_group.add_word(word_info.word, word_info.path)

                word_combo = frozenset(new_group.words)
                if word_combo in seen_words:
                    continue
                seen_words.add(word_combo)

                score = self.heuristic.calculate_group_score(new_group)
                new_group.score = score

                heapq.heappush(queue, (score, counter, new_group))
                counter += 1

        return self.found_groups