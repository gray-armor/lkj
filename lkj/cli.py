from lkj.content import Content
from lkj.config import Config
import os
import argparse
from pathlib import Path
from lkj.calendar import CalendarService
from lkj.lkj import LKJ

LKJ_HOME = Path(os.environ.get("LKJ_HOME") or os.path.expanduser("~/.lkj"))
TOKEN_PATH = LKJ_HOME/"token.json"
CREDENTIALS_PATH = LKJ_HOME/"credentials.json"
CONFIG_PATH = LKJ_HOME/"config.json"
CONTENT_PATH = LKJ_HOME/"content.txt"

def cli(lkj: LKJ):
    def start_command(args):
        lkj.start_work(" ".join(args.contents))

    def init_command(args):
        lkj.init_config()

    def show_command(args):
        lkj.show()

    def delete_command(args):
        lkj.delete_work()

    def commit_command(args):
        lkj.commit()

    parser = argparse.ArgumentParser(description="CLI tool to report working time to Google Calendar")
    subparser = parser.add_subparsers()

    init_parser = subparser.add_parser('init')
    init_parser.set_defaults(handler=init_command)

    start_parser = subparser.add_parser('new', aliases=['n'], help="start working")
    start_parser.add_argument('contents', type=str, nargs="*")
    start_parser.set_defaults(handler=start_command)

    delete_parser = subparser.add_parser("delete", aliases=['d'])
    delete_parser.set_defaults(handler=delete_command)

    commit_parser = subparser.add_parser("commit", aliases=['c'])
    commit_parser.set_defaults(handler=commit_command)

    parser.set_defaults(handler=show_command)

    args = parser.parse_args()

    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()

def main():
    cal_service = CalendarService(TOKEN_PATH, CREDENTIALS_PATH)
    config = Config(CONFIG_PATH)
    content = Content(CONTENT_PATH)
    lkj = LKJ(cal_service, config, content)
    cli(lkj)

if __name__ == "__main__":
    main()
