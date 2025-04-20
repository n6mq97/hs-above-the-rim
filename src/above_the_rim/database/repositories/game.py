from typing import Type, Optional
from sqlalchemy.orm import Session

from above_the_rim.database.models import Game


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_games(self) -> list[Type[Game]]:
        """
        Возвращает список всех игр

        Returns:
            list[Type[Game]]: полный список Game из БД
        """
        return self.db.query(Game).all()

    def get_game_by_id(self, game_id: int) -> Optional[Type[Game]]:
        """
        Возвращает Game по id

        Args:
            game_id (int): значение ID для поиска Game

        Returns:
            Game: игра найдена по ID
            None: игра не найдена по ID

        """
        return self.db.query(Game).filter(Game.ID == game_id).first()

    def add_game(self, game: Game):
        """
        Добавляет Game в БД

        Args:
            game (Game): экземпляр модели Game

        Returns:
            None: ничего не возвращает
        """
        self.db.add(game)

    def get_home_wins_by_team_id(self, team_id: int) -> int:
        """
        Возвращает количество игр, где команда победила и была дома:
        (Game.HOME_TEAM_ID == team_id, Game.HOME_TEAM_SCORE > Game.VISITING_TEAM_SCORE)

        Args:
            team_id: ID Team из БД

        Returns:
            int: количество побед
        """
        return self.db.query(Game).filter(
            Game.HOME_TEAM_ID == team_id,
            Game.HOME_TEAM_SCORE > Game.VISITING_TEAM_SCORE
        ).count()

    def get_visiting_wins_by_team_id(self, team_id: int) -> int:
        """
        Возвращает количество игр, где команда победила и была в гостях:
        (Game.VISITING_TEAM_ID == team_id, Game.VISITING_TEAM_SCORE > Game.HOME_TEAM_SCORE)

        Args:
            team_id: ID Team из БД

        Returns:
            int: количество игр с победой
        """
        return self.db.query(Game).filter(
            Game.VISITING_TEAM_ID == team_id,
            Game.VISITING_TEAM_SCORE > Game.HOME_TEAM_SCORE
        ).count()

    def get_home_loses_by_team_id(self, team_id: int) -> int:
        """
        Возвращает количество игр, где команда проиграла и была дома:
        (Game.HOME_TEAM_ID == team_id, Game.HOME_TEAM_SCORE < Game.VISITING_TEAM_SCORE)

        Args:
            team_id: ID Team из БД

        Returns:
            int: количество проигранных игр
        """
        return self.db.query(Game).filter(
            Game.HOME_TEAM_ID == team_id,
            Game.HOME_TEAM_SCORE < Game.VISITING_TEAM_SCORE
        ).count()

    def get_visiting_losses_by_team_id(self, team_id: int) -> int:
        """
        Возвращает количество игр, где команда проиграла и была в гостях:
        (Game.VISITING_TEAM_ID == team_id, Game.VISITING_TEAM_SCORE < Game.HOME_TEAM_SCORE)

        Args:
            team_id: ID Team из БД

        Returns:
            int: количество проигранных игр
        """
        return self.db.query(Game).filter(
            Game.VISITING_TEAM_ID == team_id,
            Game.VISITING_TEAM_SCORE < Game.HOME_TEAM_SCORE
        ).count()