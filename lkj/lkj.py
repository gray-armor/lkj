from datetime import datetime
from pathlib import Path
from lkj.calendar import CalendarService
from lkj.config import Config
from lkj.content import Content
from subprocess import call

class LKJ:
    def __init__(self, cal_service: CalendarService, config: Config, content: Content) -> None:
        self.cal_service = cal_service
        self.config = config
        self.content = content

    def start_work(self, content: str):
        if not self.config.valid():
            self.init_config()
        self.content.set_title(content)
        self.content.set_created_at()
        self.content.save()
        self.content.print()

    def delete_work(self):
        self.content.destroy()
        self.content.print()

    def show(self):
        self.content.print()

    def commit(self):
        if not self.content.created_at():
            self.content.print()
            return

        done_at = self.content.now()
        self.content.set_done_at(done_at)
        self.content.save()

        call(["vim", str(self.content.content_path.absolute())])

        print("Submitting this to Google Calendar.")
        self.content.print()
        while True:
            s = input("Are you sure? [y/n]: ")
            if s == "y" or s == "Y":
                self.cal_service.set_event(
                    self.config.calendarId,
                    self.content.created_at(),
                    self.content.done_at(),
                    self.content.title(),
                    self.content.message(),
                )
                self.content.destroy()
                print("Submitted.")
                return
            if s == "n" or s == "N":
                self.content.load()
                self.content.set_done_at(None)
                self.content.save()
                print("Commit aborted")
                return

    def init_config(self):
        cals = self.cal_service.get_calendars()

        if cals == None:
            print("Fail to fetch calendar data. sorry")
            exit(1)

        if len(cals) == 0:
            print("No calendar exists")
            exit(1)

        for i, cal in enumerate(cals):
            print(i+1, cal.summary)

        try:
            while True:
                try:
                    n = int(input("Select the calendar number to use: "))
                    if not (0 < n <= len(cals)):
                        raise ValueError
                    self.config.calendarId = cals[n-1].id
                    break
                except ValueError:
                    continue
        except KeyboardInterrupt:
            print("\nO.K. aborting...")
            exit(1)

        if not self.config.save():
            print("Fail to save configuration")
            exit(1)

        if not self.config.load():
            print("Fail to load configuration")
            exit(1)

        print(self.config)
