from .base import CommandHandler
from guitar import fetcher
from guitar import inquirer

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
                print inquirer.confirm('Do you want to simply install apckage using `pip`?')
                a = """Remove any common leading whitespace from every line in text.

                This can be used to make triple-quoted strings line up with the left edge of the display, while still presenting them in the source code in indented form.
                Note that tabs and spaces are both treated as whitespace, but they are not equal: the lines "  hello" and "\thello" are considered to have no common leading whitespace. (This behaviour is new in Python 2.5; older versions of this module incorrectly expanded tabs before searching for common leading whitespace.)
                """
                inquirer.warning(a)

                b = inquirer.ask("What is your name bro?")
                inquirer.success(b)

                choices = (
                    ('SOME_VALUE', 'This is some value\nAnd there is more big description'),
                    ('BHT', 'This is unclear info')
                    )

                inquirer.select(choices, title='Simple Title')

