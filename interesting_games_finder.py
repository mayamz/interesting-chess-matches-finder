import chess.pgn
import sys
import pyinputplus as pyip

reasons = {
    "high rating players": 6,
    "high rated player lost": 5,
    "the players had a lot of time": 4,
    "black lost queen, but won": 3,
    "white crowned, but lost": 2,
    "draw": 1
}

def get_key(value):
    return (list(reasons.keys())[list(reasons.values()).index(value)])

def is_interesting(game):
    cases = set()
    if game.headers.get("Termination")== "Abandoned":
        return None

    if int(game.headers.get("WhiteElo")) > 2100 and int(game.headers.get("BlackElo")) > 2100:
        cases.add((reasons["high rating players"],0))

    if game.headers.get("Result") == "1/2-1/2":
        cases.add((reasons["draw"],0))

    time, addition = game.headers.get("TimeControl").split("+")
    if int (time)>=600:
        cases.add((reasons["the players had a lot of time"],0))
    if int(time)>=300 and int(addition)>=5:
        cases.add((reasons["the players had a lot of time"],0))

    if game.headers.get("Result") =="0-1": #black won, white lost
        if int(game.headers.get("WhiteElo")) > 2100 and int(game.headers.get("BlackElo")) <= 2100:
            cases.add((reasons["high rated player lost"],0))
        queen_place = chess.D8
        theres_a_queen = 0
        for i,move in enumerate(game.mainline_moves(),1):
            if theres_a_queen != 0:
                if move.to_square != theres_a_queen:
                    cases.add((reasons["white crowned, but lost"],int((i-1)/2+0.5)))
                theres_a_queen = 0
            if i%2==0:
                if move.from_square==queen_place:
                    queen_place=move.to_square
            else:
                if move.to_square==queen_place:
                    cases.add((reasons["black lost queen, but won"],i/2))
                    queen_place = -5
                if move.promotion == 5:
                    theres_a_queen = move.to_square

    elif game.headers.get("Result") =="1-0":
        if int(game.headers.get("BlackElo")) > 2100 and int(game.headers.get("WhiteElo")) <= 2100:
            cases.add((reasons["high rated player lost"],0))
    if len(cases)>0:
        cases = sorted(cases)
        cases.append((game.headers.get("Site"),0))
        return cases

def sort_games(games):
    games = sorted(games, key=lambda game: game[0])
    games = sorted(games,key=len, reverse=True)
    for game in range (len(games)):
        for reason in range (len(games[game])):
            reason_code = games[game][reason]
            if type(reason_code) == tuple:
                if reason_code[0] in reasons.values():
                    games[game][reason] = get_key(games[game][reason][0])
                else:
                    games[game][reason] = reason_code[0]
                if reason_code[1]!=0:
                    games[game][reason] +=". look for move number %d" %reason_code[1]
    return games

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