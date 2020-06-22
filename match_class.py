import chess.pgn


class GameInterestingAttributes ():
    reasons = {
        "high rating players": 6,
        "high rated player lost": 5,
        "the players had a lot of time": 4,
        "black lost queen, but won": 3,
        "white crowned, but lost": 2,
        "draw": 1
    }

    def __init__(self, game):
        self.game = game
        self.rejected = False
        self.high_rated_players = False
        self.high_rated_player_lost = False
        self.lots_of_time = False
        self.draw = False
        self.b_lost_queen_but_won = []
        self.w_crowned_but_lost = []

        if self.game.headers.get("Termination") != "Normal":
            self.rejected = True
        if int(self.game.headers.get("WhiteElo"))<1400 and int(self.game.headers.get("BlackElo")) < 1400:
            self.rejected = True

        if int(self.game.headers.get("WhiteElo")) > 2100 and int(self.game.headers.get("BlackElo")) > 2100:
            self.high_rated_players = True

        if self.game.headers.get("Result") == "1/2-1/2":
            self.draw = True

        time, addition = self.game.headers.get("TimeControl").split("+")
        if int (time)>=600:
            self.lots_of_time = True
        if int(time)>=300 and int(addition)>=5:
            self.lots_of_time = True

        if self.game.headers.get("Result") == "0-1":  # black won, white lost
            if int(self.game.headers.get("WhiteElo")) > 2100 and int(self.game.headers.get("BlackElo")) <= 2100:
                self.high_rated_player_lost = True

            queen_place = chess.D8
            theres_a_queen = 0

            for i, move in enumerate(self.game.mainline_moves(), 1):
                if theres_a_queen != 0:
                    if move.to_square != theres_a_queen:
                        self.w_crowned_but_lost.append (int((i - 1) / 2 + 0.5))
                    theres_a_queen = 0
                if i % 2 == 0:
                    if move.from_square == queen_place:
                        queen_place = move.to_square
                else:
                    if move.to_square == queen_place:
                        self.b_lost_queen_but_won.append(int(i/2+0.5))
                        queen_place = -5
                    if move.promotion == 5:
                        theres_a_queen = move.to_square
        if self.game.headers.get("Result") == "1-0":
            if int(self.game.headers.get("BlackElo")) > 2100 and int(self.game.headers.get("WhiteElo")) <= 2100:
                self.high_rated_player_lost = True

    def analize_game(self):
        reasons = ["rejected","high_rated_players","high_rated_player_lost","lots_of_time","draw","b_lost_queen_but_won","w_crowned_but_lost"]
        results = [self.rejected, self.high_rated_players, self.high_rated_player_lost, self.lots_of_time, self.draw, self.b_lost_queen_but_won,self.w_crowned_but_lost]
        analitics = {"site": self.game.headers.get("Site")}
        for i in range (len(reasons)):
            analitics[reasons[i]]=results[i]
        return (analitics)

    def interesting_parts(self):
        reasons = ["rejected", "high_rated_players", "high_rated_player_lost", "lots_of_time", "draw",
                   "b_lost_queen_but_won", "w_crowned_but_lost"]
        results = [self.rejected, self.high_rated_players, self.high_rated_player_lost, self.lots_of_time, self.draw,
                   self.b_lost_queen_but_won, self.w_crowned_but_lost]
        analitics = {"site": self.game.headers.get("Site")}
        for i in range (len(results)):
            if results[i]!= False and results[i]!=[]:
                analitics[reasons[i]] = results[i]
        return (analitics)

    def score(self):
        interesting = self.interesting_parts()
        if "rejected" in interesting.keys():
            return 0

        score = 0
        if len(interesting)>1:
            score+=(len(interesting)-1)*10
        reasons = ["high_rated_players", "high_rated_player_lost", "lots_of_time", "draw", "b_lost_queen_but_won", "w_crowned_but_lost"]
        for i,reason in enumerate(reasons,1):
            if reason in interesting.keys():
                score+=i
        return score

