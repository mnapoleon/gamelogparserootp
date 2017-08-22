import unittest
from classes.team import Team


class TestTeamEnum(unittest.TestCase):

    def test_get_team_name(self):
        self.assertEqual(Team.BEI.name, 'BEI')
        self.assertEqual(Team.BOG.name, 'BOG')
        self.assertEqual(Team.BA.name, 'BA')
        self.assertEqual(Team.CC.name, 'CC')
        self.assertEqual(Team.CHC.name, 'CHC')
        self.assertEqual(Team.CIN.name, 'CIN')
        self.assertEqual(Team.DEN.name, 'DEN')
        self.assertEqual(Team.DUB.name, 'DUB')
        self.assertEqual(Team.ELP.name, 'ELP')
        self.assertEqual(Team.GRE.name, 'GRE')
        self.assertEqual(Team.HON.name, 'HON')
        self.assertEqual(Team.HOU.name, 'HOU')
        self.assertEqual(Team.JAK.name, 'JAK')
        self.assertEqual(Team.KC.name, 'KC')
        self.assertEqual(Team.KRA.name, 'KRA')
        self.assertEqual(Team.LON.name, 'LON')
        self.assertEqual(Team.LA.name, 'LA')
        self.assertEqual(Team.MOS.name, 'MOS')
        self.assertEqual(Team.NSH.name, 'NSH')
        self.assertEqual(Team.PHI.name, 'PHI')
        self.assertEqual(Team.SA.name, 'SA')
        self.assertEqual(Team.SJ.name, 'SJ')
        self.assertEqual(Team.SD.name, 'SD')
        self.assertEqual(Team.SP.name, 'SP')
        self.assertEqual(Team.SEA.name, 'SEA')
        self.assertEqual(Team.SEO.name, 'SEO')
        self.assertEqual(Team.SYD.name, 'SYD')
        self.assertEqual(Team.TOR.name, 'TOR')

    def test_get_team_value(self):
        self.assertEqual(Team.BEI.value, 'Beijing Bison')
        self.assertEqual(Team.BOG.value, 'Bogota Toros')
        self.assertEqual(Team.BA.value, 'Buenos Aires Albicelestes')
        self.assertEqual(Team.CC.value, 'Cape Cod Hooks')
        self.assertEqual(Team.CHC.value, 'Christchurch Crusaders')
        self.assertEqual(Team.CIN.value, 'Cincinnati Showboats')
        self.assertEqual(Team.DEN.value, 'Denver Bears')
        self.assertEqual(Team.DUB.value, 'Dublin Shamrocks')
        self.assertEqual(Team.ELP.value, 'El Paso Prospectors')
        self.assertEqual(Team.GRE.value, 'Greenville Moonshiners')
        self.assertEqual(Team.HON.value, 'Honolulu Island Kings')
        self.assertEqual(Team.HOU.value, 'Houston Orbits')
        self.assertEqual(Team.JAK.value, 'Jakarta Tidal Wave')
        self.assertEqual(Team.KC.value, 'Kansas City Monarchs')
        self.assertEqual(Team.KRA.value, 'Krakow Dragons')
        self.assertEqual(Team.LON.value, 'London Spitfires')
        self.assertEqual(Team.LA.value, 'Los Angeles Express')
        self.assertEqual(Team.MOS.value, 'Moscow Enforcers')
        self.assertEqual(Team.NSH.value, 'Nashville Sounds')
        self.assertEqual(Team.PHI.value, 'Philadelphia Brewers')
        self.assertEqual(Team.SA.value, 'San Antonio Outlaws')
        self.assertEqual(Team.SJ.value, 'San Juan Tiburones')
        self.assertEqual(Team.SD.value, 'Santo Domingo Tortugas')
        self.assertEqual(Team.SP.value, 'Sao Paulo Oncas')
        self.assertEqual(Team.SEA.value, 'Seattle Admirals')
        self.assertEqual(Team.SEO.value, 'Seoul Crushers')
        self.assertEqual(Team.SYD.value, 'Sydney Marauders')
        self.assertEqual(Team.TOR.value, 'Toronto Beavers')

    def test_find_team_by_abbr(self):
        self.assertEqual(Team.CHC, Team.find_team_by_abbr('CHC'))
        self.assertEqual(Team.SD, Team.find_team_by_abbr('SD'))
        self.assertEqual(None, Team.find_team_by_abbr("ABC"))

    @unittest.expectedFailure
    def test_failed_find_team_by_abbr(self):
        self.assertEqual(Team.CHC, Team.find_team_by_abbr("AAA"))

    def test_find_team_by_name(self):
        self.assertEqual(Team.CHC.value, Team.find_team_by_name('christchurch crusaders'))
        self.assertEqual(Team.CC.value, Team.find_team_by_name('CAPE COD HOOKS'))
        self.assertEqual(Team.LA.value, Team.find_team_by_name('Los Angeles Express'))

if __name__ == '__main__':
    unittest.main()