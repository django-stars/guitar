from .base import CommandHandler

class CreateHandler(CommandHandler):
    def handle(self):
        assert len(self.options.packages) == 1, 'We can create only single package'
        package = self.options.packages[0]
        print('Creation emulation for package `{}`'.format(package))
