from typing import List, Set, Tuple


class StrandsState:
    def __init__(self, grid: List[List[str]]):
        self.grid = grid
        self.current_path: List[Tuple[int, int]] = []  # List of (row, col) positions
        self.used_positions: Set[Tuple[int, int]] = set()  # Set of used positions
        self.found_words: Set[str] = set()  # Set of confirmed correct words

    # def get_neighbors(self, pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
    def get_neighbors(self, pos: Tuple[int, int], global_used_positions: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        neighbors = set()
        row, col = pos
        height, width = len(self.grid), len(self.grid[0])

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row = row + dr
                new_col = col + dc

                # Check if position is valid and not used in any found words
                if (0 <= new_row < height and
                        0 <= new_col < width and
                        (new_row, new_col) not in self.used_positions and
                        (new_row, new_col) not in global_used_positions):
                    neighbors.add((new_row, new_col))

        return neighbors

    #     neighbors = set()
    #     row, col = pos
    #     height, width = len(self.grid), len(self.grid[0])
    #
    #     # Check all 8 adjacent positions (including diagonals)
    #     for dr in [-1, 0, 1]:
    #         for dc in [-1, 0, 1]:
    #             if dr == 0 and dc == 0:  # Skip the position itself
    #                 continue
    #             new_row = row + dr
    #             new_col = col + dc
    #
    #             # Check if position is valid (in bounds and not used)
    #             if (0 <= new_row < height and
    #                     0 <= new_col < width and
    #                     (new_row, new_col) not in self.used_positions):
    #                 neighbors.add((new_row, new_col))
    #
    #     return neighbors

    def get_current_word(self) -> str:
        """Get the word formed by current path"""
        return ''.join(self.grid[r][c] for r, c in self.current_path)

    def make_move(self, pos: Tuple[int, int]) -> None:
        """Add a new position to the current path"""
        self.current_path.append(pos)
        self.used_positions.add(pos)

    def undo_move(self) -> None:
        """Remove the last position from current path"""
        if self.current_path:
            last_pos = self.current_path.pop()
            self.used_positions.remove(last_pos)