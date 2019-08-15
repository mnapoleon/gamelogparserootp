from enum import Enum


class Team(Enum):

    BEI = 'Beijing Bison'
    BOG = 'Bogota Toros'
    BA = 'Buenos Aires Albicelestes'
    CC = 'Cape Cod Hooks'
    CHC = 'Christchurch Crusaders'
    CIN = 'Cincinnati Showboats'
    DEN = 'Denver Bears'
    DUB = 'Dublin Shamrocks'
    ELP = 'El Paso Prospectors'
    GRE = 'Greenville Moonshiners'
    HON = 'Honolulu Island Kings'
    HOU = 'Houston Orbits'
    JAK = 'Jakarta Tidal Wave'
    KC = 'Kansas City Monarchs'
    KRA = 'Krakow Dragons'
    LON = 'London Spitfires'
    LA = 'Los Angeles Express'
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
