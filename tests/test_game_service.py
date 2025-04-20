import unittest

from above_the_rim.database.db import init_db
from above_the_rim.configs.test import TestConfig
from above_the_rim.services.repository_factory import RepositoryFactory
from above_the_rim.services.service_factory import ServiceFactory
from above_the_rim.services.game_service import GameService
from utils import TestUtils

class TestGameService(unittest.TestCase):

    def setUp(self):
        self.db = init_db(TestConfig.DB_URL)
        self.repo_factory = RepositoryFactory(self.db)
        self.service_factory = ServiceFactory(self.db, self.repo_factory)

    def test_get_game_with_quarters(self):
        setup_data = {
            "teams": [
                {"ID": 1, "SHORT": "CHW", "NAME": "Chicago Wizards"},
                {"ID": 2, "SHORT": "PRG", "NAME": "Prague Gulls"}
            ],
            "games": [
                {"ID": 1, "HOME_TEAM_ID": 2, "VISITING_TEAM_ID": 1, "HOME_TEAM_SCORE": 76, "VISITING_TEAM_SCORE": 67},
                {"ID": 2, "HOME_TEAM_ID": 2, "VISITING_TEAM_ID": 1, "HOME_TEAM_SCORE": 33, "VISITING_TEAM_SCORE": 32}
            ],
            "quarters": [
                {"ID": 1,"GAME_ID": 2, "QUARTERS": "12:20"},
                {"ID": 2, "GAME_ID": 2, "QUARTERS": "21:12"},
            ]
        }
        TestUtils.populate_db(self.db, setup_data)

        game_service: GameService = self.service_factory.get_game_service()
        all_games = game_service.get_all_games_with_quarters()
        game_1_data, game_2_data = all_games
        quarters_2_1, quarters_2_2 = game_2_data["quarters"]
        self.assertEqual(len(game_1_data["quarters"]), 0)
        self.assertEqual(len(game_2_data["quarters"]), 2)
        self.assertEqual(quarters_2_1.QUARTERS, "12:20")
        self.assertEqual(quarters_2_2.QUARTERS, "21:12")
