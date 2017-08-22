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
        self.player = ""
        self.player_team = ""
        self.inning = 0
        self.game_date = ""
        self.pitcher = ""
        self.pitcher_team = ""
        self.balls = 0
        self.swinging_strikes = 0
        self.called_strikes = 0
        self.foul_balls = 0
        self.ball_in_play = False
        self.home_run = False
        self.first_pitch_strike = False
        self.result = ""

    def __str__(self):
        return self.player + " - " + self.pitcher + " Inning : " + self.inning + \
                " - Balls: " + str(self.balls) + \
                " Called Strikes: " + str(self.called_strikes) + " Swinging Stikes: " + str(self.swinging_strikes) + \
                " First Pitch Strike: " + str(self.first_pitch_strike) + " Foul Balls: " + str(self.foul_balls) + \
                " Ball In Play : " + str(self.ball_in_play) + "Home Run : " + str(self.home_run) + \
                " Result: " + self.result