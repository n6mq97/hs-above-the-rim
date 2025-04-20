from sqlite3 import IntegrityError
from typing import List, Type
from sqlalchemy.orm import Session

from above_the_rim.database.models import Team
from above_the_rim.database.repositories.team import TeamRepository
from above_the_rim.errors.team_errors import InvalidTeamShortError, TeamNotFoundError, TeamAlreadyExistsError
from above_the_rim.services.game_service import GameService


class TeamService:
    """
    Сервис содержащий методы для реализации бизнес-логики сущности Team
    """

    def __init__(
            self,
            db: Session,
            team_repo: TeamRepository,
            game_service: GameService):
        self.db = db
        self.team_repo = team_repo
        self.game_service = game_service

    def get_all_teams(self) -> List[Type[Team]]:
        """
        Получить все Team из БД

        Returns:
            List[Type[Team]]: список команд
        """
        return self.team_repo.get_all_teams()

    @staticmethod
    def validate_team_short(short: str) -> bool:
        """
        Проверяет валидность сокращенного имени команды

        Args:
            short (str): сокращенное имя для проверки

        Returns:
            bool: true, если имя валидно (3 латинские буквы в верхнем регистре)
        """
        return str(short).isupper() and len(short) == 3

    def validate_team_short_or_rise(self, short: str):
        """
        Проверяет валидность сокращенного имени команды, выбрасывает исключение, если имя невалидно

        Args:
            short (str): сокращенное имя для проверки

        Returns:
            None

        Raises:
            InvalidTeamShortError: если имя невалидно, не подходит под условие: 3 латинские буквы в верхнем регистре
        """
        if not self.validate_team_short(short):
            raise InvalidTeamShortError(f"Invalid team short: {short}")

    def add_team_by_data(self, short: str, name: str):
        """
        Добавляет Team в БД

        Args:
            short (str): Сокращенное имя команды (3 латинские буквы в верхнем регистре)
            name (str): Полное имя команды

        Returns:
            None

        Raises:
            TeamAlreadyExistsError: Team уже существует в БД

        Note:
            Для валидации сокращенного имени использовать TeamService.validate_team_short
        """
        new_team = Team(SHORT=short, NAME=name)
        try:
            self.team_repo.add_team(new_team)
            self.db.commit()
        except IntegrityError:
            raise TeamAlreadyExistsError(f"Team '{name}' already exists")
        except:
            self.db.rollback()
            raise

    def delete_team_by_short(self, short: str):
        """
        Удаляет Team из БД по ее сокращенному имени

        Args:
            short (str): сокращенное имя команды

        Returns:
            None

        Note:
            Для валидации short использовать TeamService.validate_team_short
        """
        try:
            self.team_repo.delete_team(short)
            self.db.commit()
        except:
            self.db.rollback()
            raise

    def get_team_stats(self, team_short: str) -> dict:
        """
        Возвращает статистику команды

        Args:
            team_short (str): Сокращенное имя команды

        Returns:
            dict: {
                "name": "Example Team",
                "short": "EXP",
                "win": 10,
                "lost": 3,
            }

        Raises:
            TeamNotFoundError: команда не найдена по short

        Note:
            Перед вызовом проверить валидность short с помощью TeamService.validate_team_short
        """
        team = self.team_repo.get_team_by_short(team_short)
        if team is None:
            raise TeamNotFoundError(f"Team {team_short} not found")

        return {
            "name": team.NAME,
            "short": team.SHORT,
            "win": self.game_service.get_total_wins(team_short),
            "lost": self.game_service.get_total_losses(team_short),
        }



