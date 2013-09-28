from .base import CommandHandler

class SearchHandler(CommandHandler):
    def handle(self):
        assert len(self.options.packages) == 1, 'We can search only single package'
        package = self.options.packages[0]
        print('Searching emulation for package `{}`'.format(package))
