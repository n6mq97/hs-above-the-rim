"""
Blueprint: game_route. Содержит роуты для /api/v1/games
"""

from flask import Blueprint, jsonify, current_app, request

from above_the_rim.errors.team_errors import TeamNotFoundError, InvalidTeamShortError
from above_the_rim.services.game_service import GameService
from above_the_rim.services.team_service import TeamService

game_route = Blueprint('game', __name__, url_prefix='/api/v1/games')

def _get_team_service() -> TeamService:
    """
    Дает TeamService из current_app. Служит для единообразия получения сервиса в контроллерах

    Returns:
        TeamService: сервис реализующий бизнес-логику работы с Team
    """
    return current_app.service_factory.get_team_service()

def _get_game_service() -> GameService:
    """
    Дает GameService из current_app. Служит для единообразия получения сервиса в контроллерах

    Returns:
        GameService: сервис реализующий бизнес-логику работы с Game
    """
    return current_app.service_factory.get_game_service()

@game_route.route('/', methods=['GET'])
def get_games():
    """
    Возвращает полный список игр (Game)

    Returns:
        200 OK: {"success": true, "data": {
            "1": "Chicago Wizards 123:89 Prague Gulls",
            "2": "Prague Gulls 76:67 Chicago Wizards"
        }}
    """
    game_service = _get_game_service()
    games = game_service.get_all_games()
    games_data = {
        game.ID: f"{game.home_team.NAME} {game.HOME_TEAM_SCORE}:{game.VISITING_TEAM_SCORE} {game.visiting_team.NAME}"
        for game in games
    }
    response = {"data": games_data, "success": True}
    return jsonify(response), 200

@game_route.route('/', methods=['POST'])
def add_game():
    """
    Добавляет игру (Game) в БД

    Args:
        JSON body:
            {
                "home_team": "XYZ", "visiting_team": "PRW",
                "home_team_score": 123, "visiting_team_score": 89
            }

    Validation:
        - формат short

    Returns:
        400 BAD REQUEST: {"success": false, "data": "Wrong team short"}
        201 CREATED: {"success": true, "data": "Game has been added"}
    """
    game_service = _get_game_service()
    team_service = _get_team_service()
    request_data = request.get_json()

    try:
        team_service.validate_team_short_or_rise(request_data["home_team"])
    except InvalidTeamShortError:
        return jsonify({"success": False, "data": "Wrong team short"}), 400

    try:
        team_service.validate_team_short_or_rise(request_data["visiting_team"])
    except InvalidTeamShortError:
        return jsonify({"success": False, "data": "Wrong team short"}), 400

    try:
        game_service.add_game_by_data(
            home_short=request_data["home_team"],
            visiting_short=request_data["visiting_team"],
            home_score=request_data["home_team_score"],
            visiting_score=request_data["visiting_team_score"],
        )
    except TeamNotFoundError:
        return jsonify({"success": False, "data": "Wrong team short"}), 400

    return jsonify({"success": True, "data": "Game has been added"}), 201
