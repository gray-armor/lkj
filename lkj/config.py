from json.decoder import JSONDecodeError
from pathlib import Path
from prettytable import PrettyTable
import json

class Config:
    calendarId: str

    def __init__(self, config_path: Path) -> None:
        self.config_path = config_path
        self.__valid = self.load()

    def valid(self) -> bool:
        return self.__valid

    def load(self) -> bool:
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                self.calendarId = config["calendarId"]
                return True
        except (IOError, JSONDecodeError, KeyError):
            return False

    def save(self) -> bool:
        try:
            data = {
                "calendarId": self.calendarId
            }
            with open(self.config_path, "w") as f:
                json.dump(data, f)
            return True
        except IOError:
            return False

    def __str__(self) -> str:
        x = PrettyTable()
        x.title = "Configuration"
        x.field_names = ["Key", "Value"]
        x.add_row(["Calendar Id", self.calendarId])
        return x.get_string()
