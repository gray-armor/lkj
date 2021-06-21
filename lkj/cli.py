import os
from pathlib import Path
from lkj.calendar import Calendar

LKJ_HOME = Path(os.environ.get("LKJ_HOME") or os.path.expanduser("~/.lkj"))

def main():
    cal = Calendar(LKJ_HOME/"token.json", LKJ_HOME/"credentials.json")
    cal.print_items()

if __name__ == "__main__":
    main()
