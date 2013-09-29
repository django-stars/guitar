from textwrap import fill
from clint.textui import colored

from . import MAX_WIDTH


class DialogBase(object):
    question_prefix = "> "  # Prefix will be showed for first line of question
    question_prefix_len = len(question_prefix)  # Help text (if given), will be indented for len of prefix
    prompt = ":"

    def __init__(self, title, help_text=None, default=None, input_function=None):
        self.title = title
        self.help_text = help_text
        self.default = default
        if self.default is not None:
            assert self.validate(self.default), "Default value is not valid!"
        self.input_function = input_function or raw_input  # For test, should be replaced by `lambda: "input text"`
        self.value = None
        self.setup()

    def setup(self):
        pass

    def get_title_line(self):
        # First line of question. The only line if not help text provided.
        return "{}{}".format(self.question_prefix, self.title)

    def get_help_text(self):
        # We need reformat help text to fit into MAX_WIDTH and to be indented in the same time.
        help_lines = self.help_text.split("\n")
        # Reformat each line, by fit it into adapted MAX_WIDTH, with respect to indent and then prefixed by indent.
        return "\n".join(
            [
                "{}{}".format(
                    " " * self.question_prefix_len,
                    fill(x, MAX_WIDTH - self.question_prefix_len)
                ) for x in help_lines
            ]
        )

    def get_prompt(self):
        if self.default:
            return "[{}]{}".format(self.default, self.prompt)
        return self.prompt

    def validate(self, value):
        if value.strip():
            return value.strip()

    def check_default(self, value):
        if value.strip() == "" and self.default is not None:
            return True
        else:
            return False

    def cleanup(self, value):
        return value

    def render(self):
        # In case help_text is provided, message will be multi line. Otherwise - not.
        # Because of this we should handle prompt differently.
        if self.help_text:
            print(colored.blue(self.get_title_line()))
            print(self.get_help_text())
            print("{}{}".format(" " * self.question_prefix_len, self.get_prompt())),
        else:
            if self.default is not None:
                print("{} {}".format(colored.blue(self.get_title_line()), self.get_prompt())),
            else:
                print("{}{}".format(colored.blue(self.get_title_line()), self.get_prompt())),

    def do(self):
        while True:
            self.render()
            value = self.input_function()
            if self.check_default(value):
                value = self.default
            if self.validate(value):
                self.value = value
                return self.cleanup(value)


class Ask(DialogBase):
    pass


class YesNo(DialogBase):
    ANSWERS_YES = "y yes true sure ok 1 tada".split()
    ANSWERS_NO = "n no not false 0 nah".split()

    def setup(self):
        if self.default is None:
            self.default = False

    def get_prompt(self):
        if self.default:
            return "[Y/n]{}".format(self.prompt)
        else:
            return "[N/y]{}".format(self.prompt)

    def validate(self, value):
        # As typing "RETURN" will return True or False from `check_default`, we add those values there.
        return value in self.ANSWERS_NO or value in self.ANSWERS_YES or value in (True, False)

    def cleanup(self, value):
        if value in self.ANSWERS_YES:
            return True
        else:
            return False
