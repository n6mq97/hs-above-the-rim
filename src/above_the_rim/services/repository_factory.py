from sqlalchemy.orm import Session

from above_the_rim.database.repositories.game import GameRepository
from above_the_rim.database.repositories.quarters import QuartersRepository
from above_the_rim.database.repositories.team import TeamRepository


class RepositoryFactory:
    """
    Фабрика для создания репозиториев. Централизованное место для правильного создания всех репозиториев в программе
    """
    def __init__(self, db: Session):
        self.db = db

    def get_team_repository(self) -> TeamRepository:
        """
        Инициализирует и возвращает TeamRepository

        Returns:
            TeamRepository: репозиторий, через который идет взаимодействие с БД по сущности Team
        """
        return TeamRepository(self.db)

    def get_game_repository(self) -> GameRepository:
        """
        Инициализирует и возвращает GameRepository

        Returns:
            GameRepository: репозиторий, через который идет взаимодействие с БД по сущности Game
        """
        return GameRepository(self.db)

    def get_quarters_repository(self) -> QuartersRepository:
        """
        Инициализирует и возвращает QuartersRepository

        Returns:
            QuartersRepository: репозиторий, через который идет взаимодействие с БД по сущности Quarters
        """
        return QuartersRepository(self.db)