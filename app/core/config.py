from pydantic import BaseSettings, AnyUrl
from typing import List, Any
import logging


class AppSettings(BaseSettings):
    DEBUG: bool = True
    LOG_LEVEL: str = ""
    API_PREFIX: str = "/api"
    APPLICATION_NAME: str = "Snake & Ladder REST API"
    APPLICATION_VERSION: str = "1.0"
    ALLOWED_HOSTS_STR: str = ""
    DB_USER: str = "root"
    DB_HOST: str = "localhost"
    DB_PORT: str = 27017
    DB_NAME: str = "snake_ladder"
    DB_PASSWORD: str = "root"
    DATABASE_URL: str = ""
    MAX_CONNECTIONS_COUNT: int = 10
    MIN_CONNECTIONS_COUNT: int = 1
    LOG_LEVEL_ACTUAL: Any = logging.INFO

    @property
    def DATABASE_URL(self) -> str:
        return f"mongodb://{self.DB_USER}:{self.DB_PASSWORD}@" \
               f"{self.DB_HOST}:{self.DB_PORT}/"

    @property
    def ALLOWED_HOSTS(self) -> List[str]:
        return [host.strip() for host in self.ALLOWED_HOSTS_STR.split(",") if host]

    @property
    def LOG_LEVEL_ACTUAL(self):
        if self.LOG_LEVEL == 'DEBUG':
            return logging.DEBUG

    class Config:
        env_prefix = ""
        case_sensitive = True


settings = AppSettings()

database_name = settings.DB_NAME
player_collection = "players"
game_collection = "games"

all_db_collections = [
    player_collection,
    game_collection
]

# Logging setup
logging.basicConfig(level=settings.LOG_LEVEL_ACTUAL,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
