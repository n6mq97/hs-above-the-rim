import os
from flask import Flask

from above_the_rim.configs.base import BaseConfig
from above_the_rim.database.db import init_db
from above_the_rim.services.repository_factory import RepositoryFactory
from above_the_rim.services.service_factory import ServiceFactory
from above_the_rim.utils import register_blueprints
from above_the_rim.error_handlers import register_error_handlers

def create_app(config: BaseConfig):
    """
    Точка входа в приложение. Инициализирует и подключает все необходимое

    Args:
        config (BaseConfig): конфиг приложения, лежат в above_the_rim.configs

    Returns:
        Flask: инициализированное и полностью настроенное приложение Flask,
        которое нужно только запустить с нужными параметрами
    """
    app = Flask(__name__, root_path=os.getcwd())

    register_error_handlers(app)

    db = init_db(config.DB_URL)
    app.db = db

    repo_factory = RepositoryFactory(db)
    service_factory = ServiceFactory(db, repo_factory)
    app.service_factory = service_factory

    # Автоматическая регистрация всех блюпринтов из пакета v1
    from above_the_rim.api.v1 import __path__ as api_v1_path
    register_blueprints(app, "above_the_rim.api.v1", api_v1_path[0])

    # Автоматическая регистрация всех блюпринтов из пакета v1
    from above_the_rim.api.v2 import __path__ as api_v2_path
    register_blueprints(app, "above_the_rim.api.v2", api_v2_path[0])

    from above_the_rim.pages import __path__ as pages_path
    register_blueprints(app, "above_the_rim.pages", pages_path[0])

    return app