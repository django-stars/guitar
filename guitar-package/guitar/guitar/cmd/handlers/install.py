from .base import CommandHandler

class InstallHandler(CommandHandler):
    def handle(self):
        for package in self.options.packages:
            print('Installation emulation for package `{}`'.format(package))
