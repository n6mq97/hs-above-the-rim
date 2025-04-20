import unittest
from sqlalchemy.exc import IntegrityError

from above_the_rim.database.db import init_db
from above_the_rim.configs.test import TestConfig
from above_the_rim.services.repository_factory import RepositoryFactory
from above_the_rim.database.models import Team
from utils import TestUtils

class TestTeamRepository(unittest.TestCase):

    def setUp(self):
        self.db = init_db(TestConfig.DB_URL)
        repo_factory = RepositoryFactory(self.db)
        self.team_repository = repo_factory.get_team_repository()

    def test_get_team_by_short_found(self):
        setup_data = {
            "teams": [
                {"ID": 1, "SHORT": "CHW", "NAME": "Chicago Wizards"}
            ]
        }
        TestUtils.populate_db(self.db, setup_data)
        team = self.team_repository.get_team_by_short("CHW")
        self.assertEqual("Chicago Wizards", team.NAME)

    def test_get_team_by_short_not_found(self):
        team = self.team_repository.get_team_by_short("CHW")
        self.assertIsNone(team)

    def test_get_all_teams_not_empty(self):
        setup_data = {
            "teams": [
                {"ID": 1, "SHORT": "CHW", "NAME": "Chicago Wizards"},
                {"ID": 2, "SHORT": "PRG", "NAME": "Prague Gulls"}
            ]
        }
        TestUtils.populate_db(self.db, setup_data)
        teams = self.team_repository.get_all_teams()
        self.assertEqual(2, len(teams))

    def test_get_all_teams_empty(self):
        teams = self.team_repository.get_all_teams()
        self.assertEqual(0, len(teams))

    def test_add_team_success(self):
        tesm = Team(SHORT="CHW", NAME="Chicago Wizards")
        self.team_repository.add_team(tesm)
        self.db.commit()
        teams = self.db.query(Team).all()
        self.assertEqual(1, len(teams))

    def test_add_team_duplicate_short(self):
        setup_data = {
            "teams": [
                {"ID": 1, "SHORT": "CHW", "NAME": "Chicago Wizards"}
            ]
        }
        TestUtils.populate_db(self.db, setup_data)
        team = Team(SHORT="CHW", NAME="Chicago Wzz")
        with self.assertRaises(IntegrityError):
            self.team_repository.add_team(team)
            self.db.commit()

    def test_add_team_duplicate_name(self):
        setup_data = {
            "teams": [
                {"ID": 1, "SHORT": "CHW", "NAME": "Chicago Wizards"}
            ]
        }
        TestUtils.populate_db(self.db, setup_data)
        team = Team(SHORT="CHZ", NAME="Chicago Wizards")
        with self.assertRaises(IntegrityError):
            self.team_repository.add_team(team)
            self.db.commit()

    def test_delete_team_success(self):
        setup_data = {
            "teams": [
                {"ID": 1, "SHORT": "CHW", "NAME": "Chicago Wizards"}
            ]
        }
        TestUtils.populate_db(self.db, setup_data)
        rows_deleted_count = self.team_repository.delete_team("CHW")
        self.db.commit()
        teams = self.db.query(Team).all()
        self.assertEqual(1, rows_deleted_count)
        self.assertEqual(0, len(teams))

    def test_delete_team_not_found(self):
        rows_deleted_count = self.team_repository.delete_team("CHW")
        self.db.commit()
        self.assertEqual(0, rows_deleted_count)
