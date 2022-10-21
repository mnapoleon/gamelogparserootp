from enum import Enum


class Team(Enum):
    # PL
    BOS = 'Boston Shoremen'
    CAR = 'Carolina Reapers'
    DC = 'DC Eagles'
    HOU = 'Houston Moondogs'
    KTY = 'Kentucky Bootleggers'
    MEX = 'Mexico City Chupacabras'
    NO = 'New Orleans Krewe'
    PHI = 'Philadelphia Liberty'
    PHO = 'Phoenix Sun Dogs'
    TOR = 'Toronto Mythics'

    # SL
    ATL = 'Atlanta Swarm'
    CHI = 'Chicago Gale'
    CLE = 'Cleveland Paladins'
    DEN = 'Denver Wolves'
    GAL = 'Galveston Gremlins'
    IND = 'Indianapolis Hawks'
    MIA = 'Miami Warriors'
    MIN = 'Minnesota Freeze'
    SLC = 'Salt Lake City Stormbirds'
    TB = 'Tampa Bay Palms'

    # BL
    CIN = 'Cincinnati Kings'
    DET = 'Detroit Motors'
    LA = 'Los Angeles Chilis'
    LV = 'Las Vegas Lightning'
    NY = 'New York Empire'
    ORL = 'Orlando Orcas'
    SD = 'San Diego Fleet'
    SEA = 'Seattle Steelheads'
    VAN = 'Vancouver Titans'
    WIN = 'Winnipeg Goldeyes'

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
