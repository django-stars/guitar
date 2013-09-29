from .base import CommandHandler

from guitar.inquirer import dialogs
from guitar.inquirer import messages
from guitar import fetcher

class SearchHandler(CommandHandler):
    def handle(self):
        assert len(self.options.packages) == 1, 'We can search only single package'
        package = self.options.packages[0]
        messages.message('Searching emulation for package `{}`'.format(package))
        config = fetcher.fetcher.get_config(package)
        if config:
            messages.success("Found.")
        else:
            messages.error("No Found.")
        a = "We ask this as you may not know, how to format proper values in kinds\nof any of magnifications.\nWe also appreciate you choice, so be free there."
        res = dialogs.YesNo("You want to continue?", help_text=None, default=False)
        res.do()
        print "RES: %s" % res.value
