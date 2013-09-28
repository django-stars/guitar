"""
guitar django packages manager

Usage:
  guitar [-h | -V]
  guitar install <name>... [-vqNOD]
  guitar install <name>... [-U=<upath>] [-S=<spath>] [-L=<lspath>]
  guitar investigate [--save]
  guitar search <name>
  guitar create <name>

Options:
  -h --help                 Show this screen.
  -V --version              Show version.
  -v --verbose              Show more output.
  -q --quiet                Show no output
  -N --no-patch             Do not write any changes, only dump on screen.
  -O --overwrite            Allow to overwrite existing lines.
  -D --default              Do not ask any questions. Use defauts.
  -l --local-settings       Write changes to "local settings" file only.
  --save                    Save investigated into .guitar file
  -U --urls-file=<upath>
  -S --settings-file=<spath>
  -L --local-settings-file=<lspath>
"""
import os
from docopt import docopt

import handlers.install
import handlers.search
import handlers.create
import handlers.investigate


class Router(object):
    COMMANDS = ['install', 'search', 'investigate', 'create']
    def __init__(self, arguments):
        self.options = Options(arguments)
        self.command = self.get_command(arguments)

    def get_command(self, arguments):
        commands = [x for x in self.COMMANDS if arguments.get(x)]
        assert len(commands) == 1
        return commands[0]

    def route(self):
        # There is dict of available handlers, imported from handlers package.
        # We found right handler by key=command and provide 2 args:
        # command name and prettified options.
        {
            'install': handlers.install.InstallHandler,
            'search': handlers.search.SearchHandler,
            'investigate': handlers.investigate.InvestigateHandler,
            'create': handlers.create.CreateHandler
        }[self.command](self.command, self.options)


class Options(object):
    def __init__(self, arguments):
        self.cwd = os.getcwd()

        # Let's resolve absolute path's to files
        self.urls_file_path = self.get_full_path(arguments['--urls-file'])
        self.settings_file_path = self.get_full_path(arguments['--settings-file'])
        self.local_settings_file_path = self.get_full_path(arguments['--local-settings-file'])

        self.verbose = arguments['--verbose']
        self.quiet = arguments['--quiet']
        self.save = arguments['--save']
        self.use_defaults = arguments['--default']
        self.do_not_patch = arguments['--no-patch']
        self.overwrite = arguments['--overwrite']

        # We no need ability to list package twice or so -> set()
        self.packages = set(arguments['<name>'])

    def get_full_path(self, path):
        if path:
            full_path = os.path.abspath(os.path.join(self.cwd, path))
            if not os.path.exists(full_path):
                print("File {} does not exists.".format(full_path))  # better raise?
            return full_path


arguments = docopt(__doc__)
router = Router(arguments)
