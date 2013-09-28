from .base import CommandHandler
from guitar import fetcher


class InstallHandler(CommandHandler):
    def handle(self):
        for package in self.options.packages:
            print('Installation emulation for package `{}`'.format(package))
            print('Fetchinf configuration file...')
            config = fetcher.fetcher.get_config(package)
            if config:
                print('Fetching OK. Continue...')
            else:
                print('Fetching NOT FOUND...')
                # Check https://pypi.python.org/pypi/{} if package really exist.
                print('We do not have configuration for package you trying to install.')
                print('You can help, by contributing such configuration,')
                print('to do so, type: `guitar create {}` to create barebone configuration.'.format(package))
                print('Do you want to simply install apckage using `pip`?')

