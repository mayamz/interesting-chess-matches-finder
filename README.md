# interesting-chess-matches-finder
reads pgn files and lists the interesting games, by determined order of interest.

this project takes a pgn file that describes one chess match or more, and prints the links of the interesting matches by order of interest.
you can run the code from pycharm or from the cmd. then you'll be asked to enter a file path for the pgn input. 

# requirements
in order to use this code, you'll need to install pyinputplus and python-chess. both can be installed with pip.

# criteria
the criteria to determines whether a game was interesting is pre-determined, but can be modified within the is_interesting function.
currently, a game is considered interesting if:
1. the game ends in a draw.
2. the white player crowned at least one pawn, but lost.
3. the black player lost the queen, but won.
4. the game's time control was high (higher than 10 minutes, or higher than 5 minutes with more than 5 minutes addition)
5. a high ranked player (Elo>2100) lost to a low ranked player (Elo<2100)
6. both the players are high ranked (Elo>2100)

# priorities
the interesting games are listed by decending interest. first by the number of criteria the game matched, then by decending 
interest of the critiria itself (1 - most important, 6 - least).
