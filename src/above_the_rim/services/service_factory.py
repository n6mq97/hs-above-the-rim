from sqlalchemy.orm import Session

from above_the_rim.services.game_service import GameService
from above_the_rim.services.repository_factory import RepositoryFactory
from above_the_rim.services.team_service import TeamService


class ServiceFactory:
    """
    Фабрика сервисов. Централизированно и правильно создает сервисы
    """

    def __init__(self, db: Session, repo_factory: RepositoryFactory):
        self.db = db
        self.repo_factory = repo_factory

    def get_game_service(self) -> GameService:
        """
        Инициализирует и возвращает GameService

        Returns:
            GameService: сервис реализующий бизнес-логику Game

        """
        return GameService(
            self.db,
            self.repo_factory.get_game_repository(),
            self.repo_factory.get_team_repository(),
            self.repo_factory.get_quarters_repository()
        )

    def get_team_service(self) -> TeamService:
        """
        Инициализирует и возвращает TeamService

        Returns:
            TeamService: сервис реализующий бизнес-логику Team

        """
        return TeamService(
            self.db,
            self.repo_factory.get_team_repository(),
            self.get_game_service()
        )