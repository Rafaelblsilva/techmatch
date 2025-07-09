# Will store 'env' configurations, like logging verbosity, external urls
# and other non sensitive information related to the API
import logging
import os
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = ""
    DB_URL: str = Field(..., env="MONGO_URL")
    DB_NAME: str = Field(..., env="DB_NAME")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_ID: str = ""
    TOKEN_URL: str = '/token'
    DEFAULT_MODEL: str= 'TheBloke/Mistral-7B-Instruct-v0.2-GPTQ'


def get_settings():
    # ENV must be set as environment variable in the respective container app
    ENV = os.environ.get("ENV", "LOCAL")  # Assume local is the default one

    # get secrets from key
    return Settings(
        ENV=ENV,
        DB_URL="",
        DB_NAME="",
        SECRET_KEY="",
    )


settings = get_settings()


def setup_logger(
    name: str,
    fmt: str = "%(asctime)s.%(msecs)04d [%(name)s] %(levelname)8s: %(message)s",
    datefmt: str = "%Y-%m-%d %H:%M:%S",
    level: int = logging.INFO,
):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fmt = logging.Formatter(fmt=fmt, datefmt=datefmt)

    hdlr = logging.StreamHandler()
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    return logger
