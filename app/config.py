import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
# we need addHandler to combine handler with logger
logger.addHandler(console_handler)

#### formatter ####
formatter = logging.Formatter("%(levelname)s: %(asctime)s %(message)s")
# we need setFormatter to combine handler with handler
console_handler.setFormatter(formatter)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SERVER_", env_file=".env", extra="ignore"
    )
    host: str
    port: int
