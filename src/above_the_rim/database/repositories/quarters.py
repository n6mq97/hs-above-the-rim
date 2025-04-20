from typing import List, Type

from sqlalchemy.orm import Session

from above_the_rim.database.models import Quarters


class QuartersRepository:
    """
    Репозиторий для обмена данными по сущности Quarters
    """
    def __init__(self, db: Session):
        self.db = db

    def add_quarter(self, quarter: Quarters):
        """
        Добавляет quarter в БД

        Args:
            quarter (Quarters): объект Quarters

        Returns:
            None: ничего не возвращает
        """
        self.db.add(quarter)

    def get_quarters_by_game_id(self, game_id: int) -> List[Type[Quarters]]:
        """
        Возвращает Quarters по Game.ID
        Args:
            game_id (int): ID сущности Game

        Returns:
            list[Type[Quarters]]: список найденных Quarters
        """
        return self.db.query(Quarters).filter(Quarters.GAME_ID == game_id).all()