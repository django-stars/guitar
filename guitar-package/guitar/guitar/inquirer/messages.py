from clint.textui import colored
from textwrap import fill
from . import MAX_WIDTH


class Message(object):
    KINDS = {
        "message": colored.white,
        "success": colored.green,
        "warning": colored.yellow,
        "error": colored.red
    }

    def __init__(self, message, max_width=None, kind=None, delay=False):
        self.message = message
        self.max_width = max_width or MAX_WIDTH
        self.kind = kind or "message"
        assert self.kind in self.KINDS.keys(), "Unsupported type of message"
        if not delay:
            self.render()

    def prepare_message(self, message):
        return fill(message, self.max_width)

    def colorize(self, message):
        return self.KINDS[self.kind](message)

    def render(self):
        print(self.colorize(self.prepare_message(self.message)))


def success(msg):
    Message(msg, kind="success")

def warning(msg):
    Message(msg, kind="warning")

def error(msg):
    Message(msg, kind="error")

def message(msg):
    Message(msg, kind="message")