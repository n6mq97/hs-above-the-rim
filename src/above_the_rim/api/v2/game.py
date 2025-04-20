"""
Blueprint: game_route_v2. Содержит роуты для /api/v2/games
"""

from flask import Blueprint, jsonify, current_app, request

from above_the_rim.errors.game_errors import GameNotFoundError
from above_the_rim.errors.team_errors import InvalidTeamShortError, TeamNotFoundError
from above_the_rim.services.game_service import GameService
from above_the_rim.services.team_service import TeamService
from above_the_rim.database.models import Game

game_route_v2 = Blueprint("game_v2", __name__, url_prefix="/api/v2/games")

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

@game_route_v2.route("/", methods=["POST"])
def create_game():
    """
    Добавляет Game без счета в БД

    Args:
        JSON body:
            {
              "home_team": "PRW",
              "visiting_team": "CHG"
            }

    Returns:
        400 BAD REQUEST: {"success": false, "data": "Wrong team short"}
        200 OK: {"success": True, "data": <GAME_ID>}
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
        added_game: Game = game_service.add_game_by_data(
            home_short=request_data["home_team"],
            visiting_short=request_data["visiting_team"]
        )
    except TeamNotFoundError:
        return jsonify({"success": False, "data": "Wrong team short"}), 400

    return jsonify({"success": True, "data": added_game.ID}), 201

@game_route_v2.route("/<game_id>", methods=["POST"])
def add_quarters(game_id: int):
    """
    Добавляет счет одной четвертой игры в БД

    Args:
        PATH variables:
            game_id (int): id команды

        JSON body:
            {
                "quarters": "21:12"
            }

    Returns:
        400 BAD REQUEST: {'success': False, 'data': 'There is no game with id <GAME_ID>'}
        200 OK: {"success": True, "data": "Score updated"}
    """
    game_service = _get_game_service()
    request_data = request.get_json()
    try:
        game_service.add_game_quarter(game_id, request_data['quarters'])
    except GameNotFoundError:
        return jsonify({f'success': False, 'data': f'There is no game with id {game_id}'}), 400

    return jsonify({"success": True, "data": "Score updated"}), 201

@game_route_v2.route("/", methods=["GET"])
def get_games():
    """
    Возвращает список Games с дополнительными данными по Quarters

    Returns:
        200 OK: {
            "success": True,
             "data": {
               "1": "Chicago Gulls 123:89 Prague Wizards",
               "2": "Prague Wizards 76:67 Chicago Gulls",
               "3": "Prague Wizards 33:32 Chicago Gulls (12:20,21:12)"
            }
        }
    """
    game_service = _get_game_service()
    games_with_quarters = game_service.get_all_games_with_quarters()
    games_data = {}
    for gm in games_with_quarters:
        game = gm["game"]
        quarters = gm["quarters"]
        quarters_str = f" ({','.join([q.QUARTERS for q in quarters])})" if len(quarters) else ""
        games_data[game.ID] = f"{game.home_team.NAME} {game.HOME_TEAM_SCORE}:{game.VISITING_TEAM_SCORE} {game.visiting_team.NAME}{quarters_str}"
    response = {"data": games_data, "success": True}
    return jsonify(response), 200