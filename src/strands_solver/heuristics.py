from abc import ABC, abstractmethod
from typing import Set
from nltk.corpus import wordnet


class BaseHeuristic(ABC):
    @abstractmethod
    def calculate(self, word: str, dictionary: Set[str], found_words: Set[str] = None) -> float:
        pass


class NoHeuristic(BaseHeuristic):
    """Simple heuristic that only checks basic constraints"""

    def calculate(self, word: str, dictionary: Set[str], found_words: Set[str] = None) -> float:
        if len(word) < 4:
            return 1000
        return 0


# In heuristics.py:
class BasicHeuristic(BaseHeuristic):
    """Your current heuristic implementation"""
    def calculate(self, word: str, dictionary: Set[str], found_words: Set[str] = None) -> float:
        # Aggressive pruning for longer paths
        if len(word) > 8:  # Adjust this number based on typical Strands word length
            return float('inf')

        # Count how many dictionary words start with this prefix

        potential_words = len(dictionary.keys(word))
        # potential_words = sum(1 for dict_word in dictionary
        #                     if dict_word.startswith(word))

        if potential_words == 0:
            return float('inf')  # No words possible, prune this path

        # More aggressive scoring
        if len(word) < 4:
            return 1000

        # Strongly prefer words of typical Strands length (4-8 letters)
        if word in dictionary:
            if 4 <= len(word) <= 8:
                return -len(word) * 2
            else:
                return 0

        # Penalize very long prefixes that aren't words
        if len(word) > 6 and word not in dictionary:
            return 500

        return -potential_words / len(word)  # Balance potential words with length
class SemanticHeuristic(BaseHeuristic):
    """Heuristic that combines basic scoring with semantic similarity"""

    def calculate(self, word: str, dictionary: Set[str], found_words: Set[str] = None) -> float:
        # Start with basic heuristic score
        basic_score = BasicHeuristic().calculate(word, dictionary)

        # If basic heuristic pruned this path, return immediately
        if basic_score == float('inf'):
            return float('inf')

        # If no found words yet or word not in dictionary, return basic score
        if not found_words or word not in dictionary:
            return basic_score

        # Add semantic similarity bonus
        similarity = self._get_semantic_similarity(word, found_words)
        semantic_bonus = similarity * 10  # Adjust this weight as needed

        return basic_score - semantic_bonus

    def _get_semantic_similarity(self, word: str, found_words: Set[str]) -> float:
        max_similarity = 0
        word = word.lower()

        word_synsets = wordnet.synsets(word)
        if not word_synsets:
            return 0

        for found_word in found_words:
            found_synsets = wordnet.synsets(found_word.lower())
            if not found_synsets:
                continue

            for syn1 in word_synsets:
                for syn2 in found_synsets:
                    try:
                        similarity = syn1.path_similarity(syn2)
                        if similarity and similarity > max_similarity:
                            max_similarity = similarity
                    except:
                        continue

        return max_similarity


# Dictionary of available heuristics
HEURISTICS = {
    'none': NoHeuristic,
    'basic': BasicHeuristic,
    'semantic': SemanticHeuristic
}


# THIS STUFF WORKED
# def calculate_heuristic(self, word: str) -> float:
#     """
#     Calculate heuristic score for a word.
#     Lower score is better.
#     """
#     # Only prune really long paths
#     if len(word) > 10:  # Changed from 8 to 10
#         return float('inf')
#
#     # Count how many dictionary words start with this prefix
#     potential_words = sum(1 for dict_word in self.dictionary
#                           if dict_word.startswith(word))
#
#     if potential_words == 0:
#         return float('inf')  # No words possible, prune this path
#
#     # More lenient scoring for word length
#     if len(word) < 4:
#         return 1000
#
#     # Accept any dictionary word between 4-10 letters
#     if word in self.dictionary:
#         if 4 <= len(word) <= 10:
#             return -len(word)  # Simple length bonus, not doubled anymore
#         else:
#             return 0
#
#     # Less aggressive penalty for longer non-word prefixes
#     if len(word) > 8 and word not in self.dictionary:
#         return 200  # Reduced penalty
#
#     return -potential_words / len(word)  # Balance potential words with length