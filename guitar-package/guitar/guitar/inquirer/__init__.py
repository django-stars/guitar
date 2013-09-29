from textwrap import fill
from clint.textui import colored, cols
# from clint.textui import puts

ANSWERS_YES = "y yes true sure ok 1 tada".split()
ANSWERS_NO = "n no not false 0 nah".split()

MAX_LENGTH = 79

QUESTION_PREFIX = colored.blue("> ")

def confirm(question, default=False, prompt=None):
    prompt_addon = prompt or "[Y/n]" if default else "[N/y]"
    prompt = "{}{} {}: ".format(QUESTION_PREFIX, question.strip(), colored.green(prompt_addon))
    while True:
        val = raw_input(prompt)
        if val.strip() == "":
            return default
        if val in ANSWERS_YES:
            return True
        if val in ANSWERS_NO:
            return False

def ask(question, default=None):
    # TODO: check if question + prompt < MAX_LENGTH
    if default:
        prompt = "{}{} [{}]: ".format(QUESTION_PREFIX, question, colored.green(default))
    else:
        prompt = "{}{}: ".format(QUESTION_PREFIX, question)
    while True:
        val = raw_input(prompt)
        if val.strip():
            return val
        if val.strip() and default:
            return default

def __prepare_choices(choices):
    choices_list = []
    for i, choice in enumerate(choices):
        choices_list.append({
            'title': choice[1],
            'value': choice[0],
            'selected': False,
            'id': i + 1
            })
    return choices_list

def __choice_line(choice):
    # TODO: multiline title
    mark = (" ", "*")[int(choice['selected'])]
    print("{}{}{})\t{}".format(QUESTION_PREFIX, mark, choice['id'], choice['title']))

def select(choices, title=None, default=None, multiple=None):
    if title:
        print(title)

    choices = __prepare_choices(choices)

    while True:
        for choice in choices:
            __choice_line(choice)
        val = raw_input("[?]: ").strip()
        print val
        if val == "?":
            print "Help message. Clear?"
            raw_input()
        # TODO: 1,2,3 1 2 3, 12-14,15
        if val == "":
            # TODO: return valueS!
            return True




def success(message):
    message = fill(message, MAX_LENGTH)
    message = colored.green(message)
    print(message)

def warning(message):
    message = fill(message, MAX_LENGTH)
    message = colored.yellow(message)
    print(message)

def error(message):
    message = fill(message, MAX_LENGTH)
    message = colored.red(message)
    print(message)
