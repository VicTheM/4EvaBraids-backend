from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    def __init__(self):
        self._config = {
            "db": {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "27017"),
            },
        }
        self._config["db"][
            "uri"
        ] = f"mongodb://{self.db['host']}:{self.db['port']}/"
        self._config["db"]["name"] = os.getenv("DB_NAME", "4eva")
        self.secret_key = os.getenv("SECRET_KEY", "secret")

    @property
    def db(self):
        return self._config["db"]

    @property
    def secret_key(self):
        return self._config["secret_key"]

    @secret_key.setter
    def secret_key(self, value):
        self._config["secret_key"] = value


settings = Config()
