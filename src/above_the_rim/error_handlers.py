from flask import jsonify, Flask

def register_error_handlers(app: Flask):
    """
    Регистрирует обработчики ошибок

    Args:
        app (Flask): приложение, для которого необходимо зарегистрировать обработчики

    Returns:
        None: ничего не возвращает
    """
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"success": False, "data": "Wrong address"}), 404