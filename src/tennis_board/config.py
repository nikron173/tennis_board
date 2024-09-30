from os.path import exists
from typing import Dict
from pathlib import Path
from yaml import load, FullLoader
from jinja2 import Environment, PackageLoader


class Settings:

    def __init__(self):
        self._parse_config()

    @property
    def database_url(self) -> str:
        db: Dict = self._cfg["database"]
        return f"postgresql+psycopg2://{db['user']}:{db['passwd']}@{db['host']}:{db['port']}/{db['name']}"

    def _parse_config(self):
        path = Path(__file__).parent.parent.parent.joinpath("config.yaml").resolve()
        if not exists(path):
            raise FileNotFoundError("Configuration file config.yaml not found.")
        with open(path, encoding="utf8") as f:
            cfg = load(f, Loader=FullLoader)
            self._cfg = cfg

    @property
    def logger_level(self) -> str:
        return self._cfg["app"]["logger"]["level"]

    @property
    def pool_size(self) -> int:
        return self._cfg["app"]["sqlalchemy"]["pool_size"]

    @property
    def is_sqlalchemy_echo(self) -> bool:
        return self._cfg["app"]["sqlalchemy"]["echo"]


settings = Settings()
templates = Environment(loader=PackageLoader(__name__, "templates"))
