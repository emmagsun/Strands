import pytest
from strands_solver.grid import StrandsState


def test_grid_initialization():
    grid = [
        ['A', 'B', 'C'],
        ['D', 'E', 'F'],
        ['G', 'H', 'I']
    ]
    state = StrandsState(grid)
    assert state.grid == grid
    assert len(state.current_path) == 0
    assert len(state.used_positions) == 0


def test_get_neighbors():
    grid = [
        ['A', 'B', 'C'],
        ['D', 'E', 'F'],
        ['G', 'H', 'I']
    ]
    state = StrandsState(grid)

    # Test middle position (1,1)
    middle_neighbors = state.get_neighbors((1, 1))
    expected_middle = {
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 2),
        (2, 0), (2, 1), (2, 2)
    }
    assert middle_neighbors == expected_middle


def test_word_formation():
    grid = [
        ['C', 'A', 'T'],
        ['D', 'O', 'G'],
        ['S', 'I', 'T']
    ]
    state = StrandsState(grid)
    state.make_move((0, 0))  # C
    state.make_move((0, 1))  # A
    state.make_move((0, 2))  # T
    assert state.get_current_word() == "CAT"

# from strands_solver import StrandsState
# def test_get_neighbors():
#     """Test the get_neighbors method"""
#     grid = [
#         ['A', 'B', 'C'],
#         ['D', 'E', 'F'],
#         ['G', 'H', 'I']
#     ]
#
#     state = StrandsState(grid)
#     middle_neighbors = state.get_neighbors((1, 1))
#     expected_middle = {
#         (0,0), (0,1), (0,2),
#         (1,0),        (1,2),
#         (2,0), (2,1), (2, 2)
#     }
#
#     assert middle_neighbors == expected_middle
#
#     # Test corner position (0,0) - should have 3 neighbors
#     corner_neighbors = state.get_neighbors((0, 0))
#     expected_corner = {(0, 1), (1, 0), (1, 1)}
#     assert corner_neighbors == expected_corner