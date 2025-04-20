"""
Blueprint: team_route. Содержит роуты для /api/v1/team (/api/v1/teams)
"""

from flask import Blueprint, jsonify, current_app, request
from sqlalchemy.exc import IntegrityError

from above_the_rim.errors.team_errors import InvalidTeamShortError, TeamNotFoundError, TeamAlreadyExistsError
from above_the_rim.services.team_service import TeamService

team_route = Blueprint('team', __name__, url_prefix='/api/v1')

def get_team_service() -> TeamService:
    """
    Дает TeamService из current_app. Служит для единообразия получения сервиса в контроллерах

    Returns:
        TeamService: сервис реализующий бизнес-логику работы с Team
    """
    return current_app.service_factory.get_team_service()

@team_route.route('/teams', methods=['GET'])
def get_teams():
    """
    Возвращает полный список команд

    Returns:
        200 OK: {"success": true, "data": {"EXP": "Example Team"}}

    """
    team_service = get_team_service()
    teams = team_service.get_all_teams()
    teams_for_response = dict()
    for team in teams:
        teams_for_response[team.SHORT] = team.NAME
    return jsonify({"data": teams_for_response, "success": True}), 200

@team_route.route("/teams", methods=['POST'])
def add_team():
    """
    Добавляет команду в БД

    Args:
        JSON body:
            {
                "short": str, 3 буквы, латиница, верхний регистр,
                "name": str, произвольное имя команды
            }

    Validation:
        - формат short

    Returns:
        400 BAD REQUEST: {"success": false, "data": "Wrong short format"}
        409 CONFLICT: {"success": false, "data": "Team already exists"}
        201 CREATED: {"success": true, "data": "Team has been added"}

    """
    team_service = get_team_service()
    request_data = request.get_json()
    try:
        team_service.validate_team_short_or_rise(request_data['short'])
        team_service.add_team_by_data(short=request_data['short'], name=request_data['name'])
    except InvalidTeamShortError:
        return jsonify({"success": False, "data": "Wrong short format"}), 400
    except IntegrityError:
        return jsonify({"success": False, "data": "Team already exists"}), 409

    return jsonify({"data": "Team has been added", "success": True}), 201

@team_route.route("/team/<short>", methods=['DELETE'])
def delete_team(short: str):
    """
    Удаляет Team из БД

    Args:
        short (str): сокращенное имя команды

    Returns:
        400 BAD REQUEST: {"success": false, "data": "Wrong short format"}
        200 OK: {"success": false, "data": "Team has been deleted"}
    """
    team_service = get_team_service()
    try:
        team_service.validate_team_short_or_rise(short)
        team_service.delete_team_by_short(short)
    except InvalidTeamShortError:
        return jsonify({"success": False, "data": "Wrong short format"}), 400

    return jsonify({"data": "Team has been deleted", "success": True}), 200

@team_route.route('team/<short>', methods=['GET'])
def get_team_stats(short):
    """
    Возвращает статистику побед и поражений для команды

    Args:
        short (str): 3 буквы, латиница, верхний регистр

    Validation:
    - формат short

    Returns:
        400 BAD REQUEST: {"success": false, "data": f"There is no team <short>"}
        200 OK: {"success": true, "data": {
            "name": "Example Team",
            "short": "EXP",
            "win": 10,
            "lost": 3,
        }}

    """
    team_service: TeamService = get_team_service()
    try:
        team_service.validate_team_short_or_rise(short)
        team_stats = team_service.get_team_stats(short)
        return jsonify({
            "success": True,
            "data": team_stats
        }), 200
    except (InvalidTeamShortError, TeamNotFoundError) as e:
        return jsonify({"success": False, "data": f"There is no team {short}"}), 400