import chess.pgn
import sys
import pyinputplus as pyip
from match_class import GameInterestingAttributes

def is_interesting(game):
    game_data = GameInterestingAttributes(game)
    score = game_data.score()
    if score == 0:
        return None
    return [score, game_data.interesting_parts()]

def sort_games(games):
    games = sorted(games,key=lambda x: x[0], reverse=True)
    organized_games = []
    for game in games:
        game = game[1]
        organized_game = [game["site"]]
        for reason in game.keys():
            if reason in GameInterestingAttributes.bool_reasons:
                organized_game.append(reason)
            if reason in GameInterestingAttributes.non_bool_reasons:
                organized_game.append(str(reason)+". look for move number"+str(game[reason]))
        organized_games.append(organized_game)
    return organized_games

def checking_all_games(file):
    game_file = open(file)
    how_many_games = game_file.read().count("Event")
    game_file.seek(0)
    interstring_counter = 0
    interesting_games=[]
    for i in range (how_many_games):
        game = chess.pgn.read_game(game_file)
        interesting = is_interesting(game)
        if interesting is not None:
            interstring_counter+=1
            interesting_games.append(interesting)
    game_file.close()
    print (str(interstring_counter)+"/"+str(how_many_games),"interesting")
    for game in sort_games(interesting_games):
        print (game)

def get_filename():
    if len(sys.argv)>1:
        filename = sys.argv[1]
    else:
        filename = pyip.inputFilepath("please enter a path",mustExist=True)
    return filename

checking_all_games(get_filename())