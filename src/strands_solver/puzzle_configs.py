
PUZZLE_CONFIGS = {
    "animals": {
        "grid": [
            ['H', 'U', 'A', 'N', 'R', 'K'],
            ['L', 'A', 'M', 'M', 'E', 'A'],
            ['S', 'T', 'D', 'P', 'E', 'T'],
            ['O', 'R', 'C', 'E', 'I', 'B'],
            ['K', 'I', 'G', 'H', 'O', 'O'],
            ['N', 'A', 'N', 'A', 'R', 'I'],
            ['I', 'O', 'A', 'N', 'G', 'B'],
            ['L', 'G', 'N', 'P', 'O', 'B']
        ],
        "target_words": {"HUMAN", "MEERKAT", "BIPEDAL", "OSTRICH", "KANGAROO", "PANGOLIN", "GIBBON"},
        "hint_words": {"BIPEDAL"}
    },
    # Add more puzzles here with the same structure
    "In my kingdom": {
        "grid": [
            ['A', 'I', 'I', 'L', 'G', 'E'],
            ['M', 'D', 'N', 'M', 'Y', 'N'],
            ['O', 'A', 'F', 'A', 'U', 'Y'],
            ['T', 'H', 'X', 'S', 'M', 'P'],
            ['P', 'Y', 'O', 'O', 'S', 'E'],
            ['R', 'O', 'L', 'N', 'M', 'C'],
            ['E', 'D', 'S', 'U', 'I', 'S'],
            ['R', 'S', 'A', 'L', 'C', 'E']
        ],
        "target_words": {"TAXONOMY", "CLASS", "DOMAIN", "FAMILY", "GENUS", "ORDER", "PHYLUM", "SPECIES"},
        "hint_words": {"TAXONOMY", "PHYLUM", "GENUS"}
    },

    "Strategy game" : {
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
        "target_words": {"BISHOP", "BOARD", "KING", "KNIGHT", "PAWN", "QUEEN", "ROOK", "TIMER", "CHECKMATE"},
        "hint_words": set("CHECKMATE")

    }


}