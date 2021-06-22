from datetime import datetime
from pathlib import Path
import os
import re
from prettytable import PrettyTable

class Content:
    TITLE = "Work"
    __valid: bool = None
    __message:str = None
    __title: str = None
    __created_at: datetime = None
    __done_at: datetime = None

    def __init__(self, content_path: Path) -> None:
        self.content_path = content_path

    def load(self):
        if self.__valid is not None:
            return self.__valid

        if not self.content_path.is_file():
            self.__valid = False
            return False

        try:
            with open(self.content_path, "r") as f:
                self.__created_at = datetime.fromisoformat(re.sub("^Created At:", "", f.readline()).strip())
                done_at = re.sub("^Done At:", "", f.readline()).strip()
                try:
                    self.__done_at = datetime.fromisoformat(done_at)
                except:
                    self.__done_at = None
                self.__title = re.sub("^Title:", "", f.readline()).strip()
                self.__message = f.read()
        except Exception:
            self.__valid = False
            return False

        self.__valid = True
        return True

    def message(self):
        if not self.load():
            return None

        return self.__message

    def set_message(self, message: str):
        self.__message = message

    def created_at(self):
        if not self.load():
            return None

        return self.__created_at

    def set_created_at(self, created_at: datetime = None):
        if created_at is None:
            self.__created_at = self.now()
        else:
            self.__created_at = created_at

    def done_at(self):
        if not self.load():
            return None

        return self.__done_at

    def set_done_at(self, done_at: datetime):
        self.__done_at = done_at

    def title(self):
        if not self.load():
            return None

        return self.__title

    def set_title(self, title: str):
        self.__title = title

    def save(self):
        created_at = self.__created_at or self.now()
        done_at = "" if self.__done_at is None else self.__done_at.isoformat()
        title = self.get_default_title() if self.__title is None or self.__title.strip() == "" else self.__title.strip()
        with open(self.content_path, "w") as f:
            f.write("\n".join([
                "Created At: " + created_at.isoformat(),
                "Done At: " + done_at,
                "Title: " + title,
                "<description>"
            ]))
        self.__valid = None

    def destroy(self):
        if self.content_path.is_file():
            os.remove(self.content_path)
        self.__valid = None

    def get_default_title(self):
        return self.TITLE

    def print(self):
        if not self.content_path.is_file():
            print("No current work exists")
            return
        x = PrettyTable()
        x.title = "Current Work"
        x.field_names = ["Key", "Value"]
        x.add_row(["Created At", self.created_at()])
        x.add_row(["Done At", self.done_at()])
        x.add_row(["Title", self.title()])
        x.add_row(["Message", self.message()])
        print(x)

    def now(self) -> datetime:
        return datetime.now().astimezone().replace(second=0, microsecond=0)
