import json
import unittest
from sqlalchemy.orm import Session

from utils import TestUtils
from above_the_rim.app_factory import create_app
from above_the_rim.configs.test import TestConfig

class TestApi(unittest.TestCase):
    """
    Класс для проверки API
    """

    def setUp(self):
        """
        Готовит окружение для проведения кейсов. Запускается перед каждым тексткейсом
        """
        self.app = create_app(TestConfig())
        self.db: Session = self.app.db

    def test_api_v1(self):
        """
        Универсальный метод для прогона тестов. Берет данные из data/test_api_v1.json
        """
        with open("data/test_api_v1.json", "r") as f:
            test_cases: list[dict] = json.load(f)
        self._run_test_cases(test_cases)

    def test_api_v2(self):
        """
        Универсальный метод для прогона тестов. Берет данные из data/test_api_v2.json
        """
        with open("data/test_api_v2.json", "r") as f:
            test_cases: list[dict] = json.load(f)
        self._run_test_cases(test_cases)

    def test_api_compatibility(self):
        """
        Универсальный метод для прогона тестов. Берет данные из data/test_api_compatibility.json
        """
        with open("data/test_api_compatibility.json", "r") as f:
            test_cases: list[dict] = json.load(f)
        self._run_test_cases(test_cases)

    def _run_test_cases(self, test_cases):
        """
        Запускает тест кейсы из файла конфигурации data/test_api_*.json

        Args:
            test_cases (list[dict]): словарь конфига

        Returns:
            None: ничего не возвращает
        """
        for test_case in test_cases:
            with self.subTest(msg=test_case["description"]):
                if test_case.get('clearDb', True):
                    TestUtils.recreate_db(self.db)
                TestUtils.populate_db(self.db, test_case['setup'])
                request_params = TestUtils.get_request_params(test_case['request'])
                response = self.app.test_client().open(**request_params)
                self.assertEqual(
                    first=response.status_code,
                    second=test_case['expected']['status'],
                    msg='Неверный код ответа'
                )
                if 'json' in test_case['expected']:
                    self.assertEqual(
                        first=response.get_json(),
                        second=test_case['expected']['json'],
                        msg='Неверное тело ответа'
                    )
