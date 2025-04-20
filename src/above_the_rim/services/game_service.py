from typing import Type
from sqlalchemy.orm import Session

from above_the_rim.database.models import Game, Team, Quarters
from above_the_rim.database.repositories.game import GameRepository
from above_the_rim.database.repositories.team import TeamRepository
from above_the_rim.database.repositories.quarters import QuartersRepository
from above_the_rim.errors.game_errors import GameNotFoundError
from above_the_rim.errors.team_errors import TeamNotFoundError


class GameService:
    """
    Содержит методы, реализующие бизнес-логику связанную с сущностью Game
    """
    def __init__(
            self,
            db: Session,
            game_repository: GameRepository,
            team_repository: TeamRepository,
            quarters_repository: QuartersRepository):
        self.db = db
        self.game_repository = game_repository
        self.team_repository = team_repository
        self.quarters_repository = quarters_repository

    def get_all_games(self) -> list[Type[Game]]:
        """
        Возвращает список всех Game из базы данных

        Returns:
            list[Game]: список объектов типа Game

        """
        return self.game_repository.get_all_games()

    def add_game_by_data(self, home_short:str, visiting_short:str, home_score:int=0, visiting_score:int=0) -> Game:
        """
        Добавляет новую запись Game в базу данных, принимая примитивные параметры, состовляющие Game

        Args:
            home_short (str): сокращенное имя команды, например: 'ATL';
            visiting_short (str): сокращенное имя команды, например: 'ATL';
            home_score (int): счет домашней команды, например: 31;
            visiting_score: (int): счет команды-гостя, например: 31;

        Returns:
            game (Game): обновленный экземпляр модели, после добавления в БД

        Raises:
            TeamNotFoundError: домашнюю или гостевую команду не удалось найти по сокращенному имени.

        Note:
            Для валидации team_short используй TeamService.validate_team_short
        """
        home_team = self.team_repository.get_team_by_short(home_short)
        visiting_team = self.team_repository.get_team_by_short(visiting_short)

        if home_team is None:
            raise TeamNotFoundError(f"Home team short {home_short} does not exist")

        if visiting_team is None:
            raise TeamNotFoundError(f"Visiting team short {visiting_short} does not exist")

        new_game = Game(
            HOME_TEAM_ID=home_team.ID,
            VISITING_TEAM_ID=visiting_team.ID,
            HOME_TEAM_SCORE=home_score,
            VISITING_TEAM_SCORE=visiting_score
        )

        try:
            self.db.add(new_game)
            self.db.commit()
            self.db.refresh(new_game)
            return new_game
        except:
            self.db.rollback()
            raise

    def _get_team_or_raise(self, team_short:str) -> Team:
        """
        Поиск Team по team_short в БД, в случае ненахождения - исключение

        Args:
            team_short: Короткое имя команды. Например: 'ATL'.

        Returns:
            Team: объект команды из базы

        Raises:
            TeamNotFoundError: не найдена по короткому имени
        """
        team = self.team_repository.get_team_by_short(team_short)
        if team is None:
            raise TeamNotFoundError(f"Team short {team_short} does not exist")
        return team

    def get_home_wins(self, team_short:str) -> int:
        """
        Подсчитывает количество игр, в которых команда победила дома

        Args:
            team_short (str): 3 символа, uppercase. Короткое имя команды. Например: 'ATL'.

        Returns:
            int: количество игр

        Raises:
            TeamNotFoundError: не найдена по короткому имени

        Note:
            Для валидации team_short используй TeamService.validate_team_short
        """
        team = self._get_team_or_raise(team_short)
        return self.game_repository.get_home_wins_by_team_id(team.ID)

    def get_visiting_wins(self, team_short:str) -> int:
        """
        Подсчитывает количество игр, в которых команда победила в гостях

        Args:
            team_short (str): 3 символа, uppercase. Короткое имя команды. Например: 'ATL'.

        Returns:
            int: количество игр

        Raises:
            TeamNotFoundError: не найдена по короткому имени

        Note:
            Для валидации team_short используй TeamService.validate_team_short
        """
        team = self._get_team_or_raise(team_short)
        return self.game_repository.get_visiting_wins_by_team_id(team.ID)

    def get_home_loses(self, team_short:str) -> int:
        """
        Подсчитывает количество игр, в которых команда проиграла дома

        Args:
            team_short (str): 3 символа, uppercase. Короткое имя команды. Например: 'ATL'.

        Returns:
            int: количество игр

        Raises:
            TeamNotFoundError: не найдена по короткому имени

        Note:
            Для валидации team_short используй TeamService.validate_team_short
        """
        team = self._get_team_or_raise(team_short)
        return self.game_repository.get_home_loses_by_team_id(team.ID)

    def get_visiting_losses(self, team_short:str) -> int:
        """
        Подсчитывает количество игр, в которых команда проиграла в гостях

        Args:
            team_short (str): 3 символа, uppercase. Короткое имя команды. Например: 'ATL'.

        Returns:
            int: количество игр

        Raises:
            TeamNotFoundError: не найдена по короткому имени

        Note:
            Для валидации team_short используй TeamService.validate_team_short
        """
        team = self._get_team_or_raise(team_short)
        return self.game_repository.get_visiting_losses_by_team_id(team.ID)

    def get_total_wins(self, team_short:str) -> int:
        """
        Подсчитывает общее количество игр, в которых команда победила

        Args:
            team_short (str): 3 символа, uppercase. Короткое имя команды. Например: 'ATL'.

        Returns:
            int: количество игр

        Raises:
            TeamNotFoundError: не найдена по короткому имени

        Note:
            Для валидации team_short используй TeamService.validate_team_short
        """
        return self.get_home_wins(team_short) + self.get_visiting_wins(team_short)

    def get_total_losses(self, team_short:str) -> int:
        """
        Подсчитывает общее количество игр, в которых команда проиграла

        Args:
            team_short (str): 3 символа, uppercase. Короткое имя команды. Например: 'ATL'.

        Returns:
            int: количество игр

        Raises:
            TeamNotFoundError: не найдена по короткому имени

        Note:
            Для валидации team_short используй TeamService.validate_team_short
        """
        return self.get_home_loses(team_short) + self.get_visiting_losses(team_short)

    def add_game_quarter(self, game_id: int, quarter_data: str):
        """
        Добавляет запись Quarters и обновляет счет соответствующей Game

        Args:
            game_id (int): ID сущности Game
            quarter_data (str): Счет в одной четвертой игры в формате "<home_score>:<visiting_score>. Например - "21:12""

        Returns:
            None: ничего не возвращает
            
        Raises:
            GameNotFoundError: если Game не найдена по ID
        """
        game = self.game_repository.get_game_by_id(game_id)

        if game is None:
            raise GameNotFoundError(f"Game with ID '{game_id}' not found")

        home_score, visiting_score = [int(score) for score in quarter_data.split(":")]
        try:
            self.quarters_repository.add_quarter(Quarters(GAME_ID=game_id, QUARTERS=quarter_data))
            game.HOME_TEAM_SCORE += home_score
            game.VISITING_TEAM_SCORE += visiting_score
            self.db.commit()
        except:
            self.db.rollback()
            raise

    def get_all_games_with_quarters(self) -> list[dict[str, object]]:
        """
        Возвращает список всех Games, с дополнительной информацией о Quarters

        Returns:
            list[dict[str, object]]: кастомная структура сырых данных для использования в контроллере. Пример:
                [
                    {
                        "game": <Game object>,
                        "quarters": [<Quarters objects list>]
                    }
                ]
        """
        games = self.game_repository.get_all_games()
        games_with_quarters = []
        for game in games:
            quarters = self.quarters_repository.get_quarters_by_game_id(game.ID)
            games_with_quarters.append({
                "game": game,
                "quarters": quarters
            })

        return games_with_quarters