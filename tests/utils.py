from sqlalchemy.orm import Session
from functools import wraps
from typing import Callable

from above_the_rim.database.db import Base

class TestUtils:
    @staticmethod
    def get_request_params(params_data: dict) -> dict:
        request_params = dict()
        request_params['method'] = params_data['method']
        request_params['path'] = params_data['url']
        request_params['follow_redirects'] = True
        if 'json' in params_data:
            request_params['json'] = params_data['json']

        return request_params

    @staticmethod
    def get_model_by_table_name(table_name: str):
        for mapper in Base.registry.mappers:
            cls = mapper.class_
            if cls.__tablename__ == table_name:
                return cls
        raise ValueError(f"No model found for table name: {table_name}")

    @staticmethod
    def populate_db(db: Session, setup_data: dict):
        """
        Универсальный метод для наполнения БД

        Args:
            db (sqlalchemy.orm.Session): Объект сессии БД, через который будет происходить заполнение
            setup_data (dict):
                структура данных, которую нужно добавить в БД.
                В качестве ключей первого уровня должны быть названия таблиц,
                которые привязаны к моделям. Пример:
                      "teams": [
                        {"ID": 1, "SHORT": "CHG", "NAME": "Chicago Gulls"},
                        {"ID": 2, "SHORT": "PRW", "NAME": "Prague Wizards"}
                      ]

        Returns:
            None
        """
        for table_name, items in setup_data.items():
            ModelClass = TestUtils.get_model_by_table_name(table_name)
            for item in items:
                db.add(ModelClass(**item))
        db.commit()

    @staticmethod
    def recreate_db(db: Session):
        """
        Пересоздает БД

        Args:
            db (sqlalchemy.orm.Session): Объект сессии БД, через который будет происходить очистка

        Returns:
            None
        """
        engine = db.get_bind()
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)