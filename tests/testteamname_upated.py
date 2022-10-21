import unittest
from classes.team_old import Team


class TestTeamEnum(unittest.TestCase):

    def test_get_team_name(self):
        self.assertEqual(Team.NB.name, 'NB')
        self.assertEqual(Team.SIL.name, 'SIL')
        self.assertEqual(Team.HP.name, 'HP')

    def test_get_team_value(self):
        self.assertEqual(Team.NB.value, 'New Bludvist Ravens')
        self.assertEqual(Team.SIL.value, 'Siltston Neptunes')
        self.assertEqual(Team.HP.value, 'High Point Miners')

    def test_find_team_by_abbr(self):
        self.assertEqual(Team.NB, Team.find_team_by_abbr('NB'))
        self.assertEqual(Team.SRF, Team.find_team_by_abbr('SRF'))
        self.assertEqual(None, Team.find_team_by_abbr("XYZ"))

    @unittest.expectedFailure
    def test_failed_find_team_by_abbr(self):
        self.assertEqual(Team.NB, Team.find_team_by_abbr("AAA"))

    def test_find_team_by_name(self):
        self.assertEqual(Team.NB, Team.find_team_by_name('New Bludvist Ravens'))
        self.assertEqual(Team.HP, Team.find_team_by_name('HIGH POINT MINERS'))
        self.assertEqual(Team.SIL, Team.find_team_by_name('siltston neptunes'))

if __name__ == '__main__':
    unittest.main()