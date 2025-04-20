from typing import Optional, List, Type
from sqlalchemy.orm import Session

from above_the_rim.database.models import Team


class TeamRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_team_by_short(self, short: str) -> Optional[Team]:
        """
        Возвращает Team по ее сокращенному имени

        Args:
            short (str): сокращенное имя команды

        Returns:
            Team: модель команды
        """
        return self.db.query(Team).filter_by(SHORT=short).first()

    def get_all_teams(self) -> List[Type[Team]]:
        """
        Возвращает все Team из БД

        Returns:
            List[Type[Team]]: списко всех команд
        """
        return self.db.query(Team).all()

    def add_team(self, team: Team):
        """
        Добавляет Team в БД

        Args:
            team (Team): модель Team

        Returns:
            None

        Raises:
            IntegrityError:
                - Нарушение UNIQUE constraint
        """
        self.db.add(team)

    def delete_team(self, short: str) -> int:
        """
        Удаляет Team из БД по ее сокращенному имени

        Args:
            short (str): сокращенное имя команды

        Returns:
            int: количество удаленных строк
        """
        return self.db.query(Team).filter_by(SHORT=short).delete()