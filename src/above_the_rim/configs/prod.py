import os

from dotenv import load_dotenv

from above_the_rim.configs.base import BaseConfig

load_dotenv()

class ProdConfig(BaseConfig):
    DB_URL = os.environ.get("DB_URL")