from enum import Enum


class Team(Enum):

    NR = 'New Ruksburgh Red Squirrels'
    TRA = 'Traston Robins'
    POR = 'Port Berth Armada'
    RAU = 'Raupo Kings'
    NB = 'New Bludvist Ravens'
    CSB = 'Crescent Bay Sharks'
    StG = 'St. Grouix Islanders'
    TID = 'Tidepool Gulls'
    EDG = 'Eden Garden Appleseeds'
    SIL = 'Siltston Neptunes'
    PLU = 'Plumbua Warriors'
    SRF = 'Surf City Beacons'
    KIT = 'Kitter Tigers'
    TRO = 'Trome Knights'
    KOL = 'Koldonia Wizards'
    SC = 'Star City Emeralds'
    BIL = 'Biltanore Stone Crabs'
    LRF = 'Lockrun Forest Bears'
    RR = 'Rustic River Barons'
    HAI = 'Hainesville Hooligans'
    DEP = 'Deepwood Lumberjacks'
    DEA = 'Deadwood Wranglers'
    HP = 'High Point Miners'
    TRE = 'Trelly Springs Bells'

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
