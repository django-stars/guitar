from guitar.inquirer import messages
from guitar import fetcher
from .base import CommandHandler


class SearchHandler(CommandHandler):
    def handle(self):
        assert len(self.options.packages) == 1, 'We can search only single package'
        package = self.options.packages[0]
        messages.message('Searching emulation for package `{}`'.format(package))
        res = fetcher.fetcher.search(package)
        if res and res['status'] == "OK":
            messages.success("Found by `{}`".format(package))
            for p in res['chords']:
                messages.message("> {}".format(p))
        else:
            messages.error("No Found.")
