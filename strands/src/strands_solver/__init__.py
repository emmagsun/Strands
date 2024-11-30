from typing import List, Set, Tuple

class StrandsState:
    def __init__(self, grid):
        self.grid = grid
        self.current_path: List[Tuple[int, int]] = [] # List of tuples representing positions (row, col)
        self.used_positions: Set[Tuple[int, int]] = set()
        self.found_words: Set[str] = set()

    def get_neighbors(self, pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
        neighbors = set()
        row, col = pos[0], pos[1]
        width, height = len(self.grid[0]), len(self.grid)

        def in_bounds(row, col, width, height):
            return (row < width and row > 0 and col < height and col > 0)

        horizontal_movement = [-1, 0, 1]
        vertical_movement = [-1, 0, 1]

        for h in horizontal_movement:
            for v in vertical_movement:
                if h == 0 and v == 0:
                    continue
                new_row = row + h
                new_col = col + v

                if in_bounds(new_row, new_col, width, height) and (new_row, new_col) not in self.used_positions:
                    neighbors.add((new_row, new_col))

        return neighbors