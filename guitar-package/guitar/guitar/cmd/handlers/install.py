from .base import CommandHandler
from guitar import fetcher
from guitar import inquirer

class InstallHandler(CommandHandler):
    def handle(self):
        for package in self.options.packages:
            print('Installation emulation for package `{}`'.format(package))
            print('Fetching configuration file...')
            config = fetcher.fetcher.get_config(package)
            if config:
                print('Fetching OK. Continue...')
                # TODO: Check if package already installed by pip
                # TODO: Investigate project structure to find required files.
                # TODO: Ask questions
                # TODO: Write changes to settings, urls, requirements.
            else:
                print('Fetching NOT FOUND...')
                # Check https://pypi.python.org/pypi/{} if package really exist.
                # XXX: We can have configurations, not related to packages, like:
                # - simplify CACHE, DATABASE, DEFAULT_CONTEXT_PROCESSORS configuration.
                # - scaffolding?
                # So that is is not necessary, that pypi should return 200
                print('We do not have configuration for package you trying to install.')
                print('You can help, by contributing such configuration,')
                print('To do so, type: `guitar create {}` to create barebone configuration.'.format(package))
                #print inquirer.dialogs.YesNo('Do you want to simply install apckage using `pip`?').do()


