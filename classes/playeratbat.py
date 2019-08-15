class HitResult:
    SINGLE = '1B'
    DOUBLE = '2B'
    TRIPLE = '3B'
    HOMERUN = 'HR'
    WALK = 'BB'
    INTENTIONAL_WALK = 'IBB'
    HIT_BY_PITCH = 'HB'
    STRIKEOUT = 'SO'
    GROUNDOUT = 'GO'
    GROUND_INTO_DOUBLE_PLAY = 'GO-DP'
    POPOUT = 'PO'
    FLYOUT = 'FO'
    SACRIFICE = 'SAC'
    REACHED_ON_ERROR = 'ROE'

class PlayerAtBat:

    def __init__(self):
        self.game_id = 0
        self.player_id = 0
        self.player = ""
        self.player_team = ""
        self.league = ""
        self.inning = 0
        self.game_date = ""
        self.pitcher_id = 0
        self.pitcher = ""
        self.pitcher_team = ""
        self.balls = 0
        self.swinging_strikes = 0
        self.called_strikes = 0
        self.foul_balls = 0
        self.ball_in_play = 0
        self.home_run = 0
        self.first_pitch_strike = 0
        self.called_strike_out = 0
        self.swinging_strike_out = 0
        self.result = ""
        self.hittype = ""
        self.hitlocation = ""
        self.exitvelo = ""

    def __str__(self):
        return "GameId: "+self.game_id + ":" + self.player + "(" + self.player_id + ")" + " - " + self.pitcher + "(" + self.pitcher_id + ")" + " Inning : " + self.inning + \
                " - Balls: " + str(self.balls) + \
                " Called Strikes: " + str(self.called_strikes) + " Swinging Stikes: " + str(self.swinging_strikes) + \
                " First Pitch Strike: " + str(self.first_pitch_strike) + " Foul Balls: " + str(self.foul_balls) + \
                " Ball In Play : " + str(self.ball_in_play) + "Home Run : " + str(self.home_run) + \
                " Result: " + self.result + " Hit Type: " + self.hittype + " Hit Location: " + self.hitlocation + \
                " Exit Velo: " + self.exitvelo + " League: " + self.league
