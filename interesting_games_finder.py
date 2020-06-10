import chess.pgn
import pyinputplus as pyip

def is_interesting(game):
    reasons = {
        "high rating players": 6,
        "high rated player lost": 5,
        "the players had a lot of time": 4,
        "black lost queen, but won": 3,
        "white crowned, but lost": 2,
        "draw": 1
    }
    cases = set()
    if game.headers.get("Termination")== "Abandoned":
        return None

    if int(game.headers.get("WhiteElo")) > 2100 and int(game.headers.get("BlackElo")) > 2100:
        cases.add(reasons["high rating players"])

    if game.headers.get("Result") == "1/2-1/2":
        cases.add(reasons["draw"])

    time, addition = game.headers.get("TimeControl").split("+")
    if int (time)>=600:
        cases.add(reasons["the players had a lot of time"])
    if int(time)>=300 and int(addition)>=5:
        cases.add(reasons["the players had a lot of time"])

    if game.headers.get("Result") =="0-1": #black won, white lost
        if int(game.headers.get("WhiteElo")) > 2100 and int(game.headers.get("BlackElo")) <= 2100:
            cases.add(reasons["high rated player lost"])
        queen_place = chess.D8
        for i,move in enumerate(game.mainline_moves(),1):
            if i%2==0:
                if move.from_square==queen_place:
                    queen_place=move.to_square
            else:
                if move.to_square==queen_place:
                    cases.add(reasons["black lost queen, but won"])
                if move.to_square>=56:
                    cases.add(reasons["white crowned, but lost"])
            i+=1

    else:
        if int(game.headers.get("BlackElo")) > 2100 and int(game.headers.get("WhiteElo")) <= 2100:
            cases.add(reasons["high rated player lost"])
    if len(cases)>0:
        cases = sorted(cases)
        cases.append(game.headers.get("Site"))
        return cases

def sort_games(games):
    games = sorted(games, key=lambda game: game[0])
    games =sorted(games,key=len, reverse=True)
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

filename = pyip.inputFilepath("enter file path", mustExist = True)
checking_all_games(filename)