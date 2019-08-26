from enum import Enum


class Team(Enum):

    BEI = 'Beijing Bison'
    BOG = 'Bogota Toros'
    BDX = 'Bordeaux Vignerons'
    CC = 'Cape Cod Hooks'
    CHC = 'Christchurch Crusaders'
    CIN = 'Cincinnati Showboats'
    DUB = 'Dublin Shamrocks'
    GRE = 'Greenville Moonshiners'
    HON = 'Honolulu Island Kings'
    HOU = 'Houston Orbits'
    KC = 'Kansas City Monarchs'
    LON = 'London Spitfires'
    MOS = 'Moscow Enforcers'
    NSH = 'Nashville Sounds'
    PHI = 'Philadelphia Brewers'
    SA = 'San Antonio Outlaws'
    SJ = 'San Juan Tiburones'
    SD = 'Santo Domingo Tortugas'
    SP = 'Sao Paulo Oncas'
    SEA = 'Seattle Admirals'
    SEO = 'Seoul Crushers'
    SYD = 'Sydney Marauders'
    TOR = 'Toronto Beavers'

    SHA = 'Shanghai Snakes'
    GUA = 'Guangzhou Tigers'
    ZHE = 'Zhengzhou Elephants'
    MAN = 'Manchuria Moon Bears'
    TIB = 'Tibet Wolves'

    @staticmethod
    def find_team_by_abbr(abbr):
        for team in Team:
            if team.name == abbr:
                return team

    @staticmethod
    def find_team_by_name(name):
        for team in Team:
            if str(team.value).strip().lower().__eq__(name.strip().lower()):
                return team
