from .base import CommandHandler


class InvestigateHandler(CommandHandler):
    def handle(self):
        assert len(self.options.packages) == 0, 'Investigate do not require any package'
        print('Investigation emulation...')
