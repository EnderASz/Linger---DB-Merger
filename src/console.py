import os
import sys

from rich.console import Console as RichConsole


class Console(RichConsole):
    def debug(self, *args, **kwargs):
        if os.environ.get('DEBUG', "false").lower() in {"t", "true"}:
            self.log(":bug:", *args, emoji=True, _stack_offset=2, **kwargs)

    def warn(self, *args, **kwargs):
        self.print(":exclamation:", *args, emoji=True, **kwargs)

    def error(self, *args, **kwargs):
        self.print(":x:", *args, emoji=True, **kwargs)

    def hint(self, *args, **kwargs):
        self.print(":grey_question:", *args, emoji=True, **kwargs)

    def exit(self, *args, code=0, **kwargs):
        self.print(":door:", *args, "Exiting...", emoji=True, **kwargs)
        sys.exit(code)


def init_console():
    global console
    console = Console()
