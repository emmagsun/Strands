
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

    },
    
    "What's so funny?": {
        "grid": [
            ['E', 'L', 'T', 'I', 'T', 'G'],
            ['K', 'W', 'R', 'E', 'T', 'U'],
            ['H', 'C', 'A', 'F', 'F', 'S'],
            ['R', 'I', 'U', 'H', 'U', 'L'],
            ['R', 'O', 'A', 'R', 'A', 'O'],
            ['T', 'T', 'O', 'R', 'O', 'H'],
            ['C', 'H', 'U', 'C', 'K', 'L'],
            ['E', 'R', 'H', 'O', 'O', 'T']
        ],
        "target_words": {"LAUGH", "CHORTLE", "GUFFAW", "ROAR", "TITTER", "CHUCKLE", "HOOT"},
        "hint_words": {"HILARIOUS"}
    },
    # Audrey - May
    "In a good workout": {
        "grid": [
            ['I', 'T', 'P', 'I', 'L', 'L'],
            ['C', 'A', 'I', 'E', 'W', 'E'],
            ['S', 'L', 'G', 'H', 'T', 'F'],
            ['R', 'S', 'E', 'S', 'I', 'T'],
            ['O', 'W', 'N', 'T', 'E', 'R'],
            ['E', 'R', 'I', 'M', 'D', 'A'],
            ['L', 'L', 'B', 'C', 'A', 'B'],
            ['E', 'K', 'I', 'S', 'E', 'L']
        ],
        "target_words": {"TREADMILL", "ELLIPTICAL", "ROWER", "WEIGHTS", "BIKE", "CABLES"},
        "hint_words": {"FITNESS"}
    },
    "Birdsong": {
        "grid": [
        ["E", "C", "E", "E", "T", "I"],
        ["E", "H", "W", "W", "H", "S"],
        ["R", "T", "S", "O", "L", "T"],
        ["C", "S", "D", "C", "N", "E"],
        ["B", "I", "R", "L", "U", "G"],
        ["P", "A", "R", "T", "C", "K"],
        ["R", "W", "C", "B", "R", "L"],
        ["I", "H", "E", "L", "I", "L"]
        ],
        "target_words": {
            "WARBLE", "CLUCK", "CHIRP", "TWEET", "WHISTLE", "TRILL", "SCREECH"
        },
        "hint_words": {
            "BIRDSONG"
        }
    },
    "Sounds delicious!": {
        "grid": [
        ["T", "E", "P", "H", "L", "A"],
        ["E", "M", "A", "O", "I", "C"],
        ["R", "I", "O", "M", "H", "R"],
        ["K", "L", "P", "E", "S", "I"],
        ["S", "A", "E", "H", "L", "S"],
        ["E", "O", "N", "O", "L", "T"],
        ["I", "T", "O", "E", "Y", "A"],
        ["M", "E", "M", "S", "E", "K"]
        ],
        "target_words": {
            "SERIAL", "CHILLY", "MEET", "STAKE", "PAIR", "TIME", "MOOSE", "LEAK"
        },
        "hint_words": {
            "HOMOPHONES"
        }
    },

    "Picture this": {
        "grid": [
            ['A', 'T', 'R', 'I', 'O', 'D'],
            ['R', 'E', 'M', 'P', 'E', 'R'],
            ['P', 'O', 'A', 'C', 'T', 'Y'],
            ['T', 'H', 'T', 'L', 'H', 'L'],
            ['I', 'M', 'O', 'I', 'P', 'E'],
            ['E', 'G', 'F', 'A', 'N', 'S'],
            ['R', 'I', 'R', 'H', 'A', 'L'],
            ['L', 'G', 'H', 'T', 'S', 'F']
        ],
        "target_words": {"FILTER", "LENS", "CAMERA", "FLASH", "TRIPOD", "TIMER", "LIGHT"},
        "hint_words": {"PHOTOGRAPHY"}
    },
    
    "This'll all blow over": {
        "grid": [
            ['A', 'P', 'L', 'E', 'T', 'N'],
            ['P', 'B', 'B', 'U', 'H', 'O'],
            ['E', 'T', 'B', 'E', 'G', 'O'],
            ['R', 'A', 'H', 'R', 'I', 'L'],
            ['F', 'E', 'W', 'W', 'E', 'L'],
            ['R', 'A', 'H', 'T', 'A', 'E'],
            ['T', 'I', 'G', 'A', 'B', 'Y'],
            ['S', 'L', 'H', 'S', 'L', 'E']
        ],
        "target_words": {"FEATHER", "BUBBLE", "BALLOON", "EYELASH", "STRAW", "PAPER"},
        "hint_words": {"LIGHTWEIGHT"}
},
"You can say that again!": {
        "grid": [
            ['O', 'M', 'R', 'T', 'U', 'T'],
            ['M', 'P', 'E', 'P', 'U', 'C'],
            ['P', 'R', 'U', 'E', 'C', 'O'],
            ['G', 'U', 'R', 'T', 'I', 'U'],
            ['G', 'O', 'A', 'I', 'N', 'C'],
            ['O', 'M', 'O', 'S', 'A', 'C'],
            ['A', 'M', 'N', 'C', 'N', 'A']
        ],
        "target_words": {"MURMUR", "COUSCOUS", "TUTU", "CANCAN", "POMPOM", "MAMA", "GOGO"},
        "hint_words": {"REPETITION"}
    },
    "Join the club!": {
        "grid": [
            ['E', 'U', 'T', 'T', 'E', 'L'],
            ['C', 'N', 'O', 'R', 'K', 'E'],
            ['B', 'C', 'K', 'L', 'U', 'Y'],
            ['S', 'A', 'C', 'E', 'T', 'H'],
            ['M', 'A', 'I', 'P', 'C', 'T'],
            ['A', 'N', 'D', 'W', 'I', 'O'],
            ['Y', 'N', 'N', 'S', 'M', 'A'],
            ['O', 'A', 'I', 'E', 'T', 'O']
        ],
        "target_words": {"TURKEY", "LETTUCE", "TOMATO", "MAYONNAISE", "BACON", "PICKLE"},
        "hint_words": {"SANDWICH"}
    },
     "On the grid": {
        "grid": [
            ['T', 'A', 'W', 'N', 'R', 'E'],
            ['E', 'R', 'H', 'T', 'E', 'T'],
            ['A', 'S', 'T', 'E', 'I', 'N'],
            ['S', 'A', 'T', 'L', 'B', 'T'],
            ['E', 'I', 'I', 'L', 'T', 'E'],
            ['L', 'H', 'P', 'C', 'I', 'R']
        ],
        "target_words": {"ELECTRIC", "WATER", "HEAT", "INTERNET", "CABLE", "TELEPHONE"},
        "hint_words": {"UTILITIES"}
    }



}