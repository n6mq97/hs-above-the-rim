import os

from dotenv import load_dotenv

from above_the_rim.configs.base import BaseConfig

load_dotenv()

class TestConfig(BaseConfig):
    DB_URL = "sqlite://"