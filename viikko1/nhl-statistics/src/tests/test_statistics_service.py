import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(PlayerReaderStub())
    
    def test_search_finds_player(self):
        player = self.stats.search("Semenko")
        self.assertEqual(player.name, "Semenko")
        self.assertEqual(player.team, "EDM")
        self.assertEqual(player.goals, 4)
        self.assertEqual(player.assists, 12)
    
    def test_search_returns_none_if_player_not_found(self):
        player = self.stats.search("NonExistent")
        self.assertIsNone(player)
    
    def test_team_returns_players_of_team(self):
        edm_players = self.stats.team("EDM")
        self.assertEqual(len(edm_players), 3)
        self.assertEqual(edm_players[0].name, "Semenko")
        self.assertEqual(edm_players[1].name, "Kurri")
        self.assertEqual(edm_players[2].name, "Gretzky")
    
    def test_team_returns_empty_list_if_team_not_found(self):
        team = self.stats.team("NON")
        self.assertEqual(len(team), 0)
    
    def test_top_returns_correct_number_of_players(self):
        top_players = self.stats.top(3)
        self.assertEqual(len(top_players), 3)
    
    def test_top_sorts_by_points_by_default(self):
        top_players = self.stats.top(5)
        self.assertEqual(top_players[0].name, "Gretzky")  # 35 + 89 = 124 points
        self.assertEqual(top_players[1].name, "Lemieux")  # 45 + 54 = 99 points
        self.assertEqual(top_players[2].name, "Yzerman")  # 42 + 56 = 98 points
        self.assertEqual(top_players[3].name, "Kurri")    # 37 + 53 = 90 points
        self.assertEqual(top_players[4].name, "Semenko")  # 4 + 12 = 16 points

    def test_top_sorts_by_points_when_explicitly_specified(self):
        top_players = self.stats.top(5, SortBy.POINTS)
        self.assertEqual(top_players[0].name, "Gretzky")  # 124 points
        self.assertEqual(top_players[1].name, "Lemieux")  # 99 points
        self.assertEqual(top_players[2].name, "Yzerman")  # 98 points

    def test_top_sorts_by_goals(self):
        top_players = self.stats.top(5, SortBy.GOALS)
        self.assertEqual(top_players[0].name, "Lemieux")  # 45 goals
        self.assertEqual(top_players[1].name, "Yzerman")  # 42 goals
        self.assertEqual(top_players[2].name, "Kurri")    # 37 goals

    def test_top_sorts_by_assists(self):
        top_players = self.stats.top(5, SortBy.ASSISTS)
        self.assertEqual(top_players[0].name, "Gretzky")  # 89 assists
        self.assertEqual(top_players[1].name, "Yzerman")  # 56 assists
        self.assertEqual(top_players[2].name, "Lemieux")  # 54 assists