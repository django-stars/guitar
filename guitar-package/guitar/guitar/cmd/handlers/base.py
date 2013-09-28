class CommandHandler(object):
    def __init__(self, command, options):
        self.options = options
        self.command = command
        self.handle()

    def handle(self):
        raise NotImplementedError('You should overwrite `handle` method of `{}`'.format(self.__class__.__name__))
