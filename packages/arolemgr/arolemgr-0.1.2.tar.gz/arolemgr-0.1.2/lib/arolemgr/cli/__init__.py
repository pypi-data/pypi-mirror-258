# Copyright: (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
# Copyright: (c) 2016, Toshio Kuratomi <tkuratomi@ansible.com>
# Copyright: (c) 2018, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import locale
import os
import sys

# Used for determining if the system is running a new enough python version
# and should only restrict on our documented minimum versions
if sys.version_info < (3, 10):
    raise SystemExit(
        'ERROR: Ansible requires Python 3.10 or newer on the controller. '
        'Current version: %s' % ''.join(sys.version.splitlines())
    )


def check_blocking_io():
    """Check stdin/stdout/stderr to make sure they are using blocking IO."""
    handles = []

    for handle in (sys.stdin, sys.stdout, sys.stderr):
        # noinspection PyBroadException
        try:
            fd = handle.fileno()
        except Exception:
            continue  # not a real file handle, such as during the import sanity test

        if not os.get_blocking(fd):
            handles.append(getattr(handle, 'name', None) or '#%s' % fd)

    if handles:
        raise SystemExit('ERROR: Ansible requires blocking IO on stdin/stdout/stderr. '
                         'Non-blocking file handles detected: %s' % ', '.join(_io for _io in handles))


check_blocking_io()


def initialize_locale():
    """Set the locale to the users default setting and ensure
    the locale and filesystem encoding are UTF-8.
    """
    try:
        locale.setlocale(locale.LC_ALL, '')
        dummy, encoding = locale.getlocale()
    except (locale.Error, ValueError) as e:
        raise SystemExit(
            'ERROR: Ansible could not initialize the preferred locale: %s' % e
        )

    if not encoding or encoding.lower() not in ('utf-8', 'utf8'):
        raise SystemExit('ERROR: Ansible requires the locale encoding to be UTF-8; Detected %s.' % encoding)

    fs_enc = sys.getfilesystemencoding()
    if fs_enc.lower() != 'utf-8':
        raise SystemExit('ERROR: Ansible requires the filesystem encoding to be UTF-8; Detected %s.' % fs_enc)


initialize_locale()


from importlib.metadata import version
from arolemgr.module_utils.compat.version import LooseVersion

# Used for determining if the system is running a new enough Jinja2 version
# and should only restrict on our documented minimum versions
jinja2_version = version('jinja2')
if jinja2_version < LooseVersion('3.0'):
    raise SystemExit(
        'ERROR: Ansible requires Jinja2 3.0 or newer on the controller. '
        'Current version: %s' % jinja2_version
    )

import errno
import getpass
import subprocess
import traceback
from abc import ABC, abstractmethod
from pathlib import Path

try:
    from arolemgr import  constants as C
    from arolemgr.utils.display import Display
    display = Display()
except Exception as e:
    print('ERROR: %s' % e, file=sys.stderr)
    sys.exit(5)

from arolemgr import  context
from arolemgr.cli.arguments import option_helpers as opt_help
from arolemgr.errors import AnsibleError, AnsibleOptionsError, AnsibleParserError
from arolemgr.module_utils.six import string_types
from arolemgr.module_utils.common.text.converters import to_bytes, to_text
from arolemgr.module_utils.common.collections import is_sequence
from arolemgr.module_utils.common.file import is_executable
from arolemgr.plugins.loader import add_all_plugin_dirs, init_plugin_loader
from arolemgr.release import __version__
from arolemgr.utils.path import unfrackpath
from arolemgr.utils.unsafe_proxy import to_unsafe_text

try:
    import argcomplete
    HAS_ARGCOMPLETE = True
except ImportError:
    HAS_ARGCOMPLETE = False


class CLI(ABC):
    ''' code behind bin/ansible* programs '''

    PAGER = C.config.get_config_value('PAGER')

    # -F (quit-if-one-screen) -R (allow raw ansi control chars)
    # -S (chop long lines) -X (disable termcap init and de-init)
    LESS_OPTS = 'FRSX'
    SKIP_INVENTORY_DEFAULTS = False

    def __init__(self, args, callback=None):
        """
        Base init method for all command line programs
        """

        if not args:
            raise ValueError('A non-empty list for args is required')

        self.args = args
        self.parser = None
        self.callback = callback

        if C.DEVEL_WARNING and __version__.endswith('dev0'):
            display.warning(
                'You are running the development version of Ansible. You should only run Ansible from "devel" if '
                'you are modifying the Ansible engine, or trying out features under development. This is a rapidly '
                'changing source of code and can become unstable at any point.'
            )

    @abstractmethod
    def run(self):
        """Run the ansible command

        Subclasses must implement this method.  It does the actual work of
        running an Ansible command.
        """
        self.parse()

        # Initialize plugin loader after parse, so that the init code can utilize parsed arguments
        cli_collections_path = context.CLIARGS.get('collections_path') or []
        if not is_sequence(cli_collections_path):
            # In some contexts ``collections_path`` is singular
            cli_collections_path = [cli_collections_path]
        init_plugin_loader(cli_collections_path)

        display.vv(to_text(opt_help.version(self.parser.prog)))

        if C.CONFIG_FILE:
            display.v(u"Using %s as config file" % to_text(C.CONFIG_FILE))
        else:
            display.v(u"No config file found; using defaults")

        # warn about deprecated config options
        for deprecated in C.config.DEPRECATED:
            name = deprecated[0]
            why = deprecated[1]['why']
            if 'alternatives' in deprecated[1]:
                alt = ', use %s instead' % deprecated[1]['alternatives']
            else:
                alt = ''
            ver = deprecated[1].get('version')
            date = deprecated[1].get('date')
            collection_name = deprecated[1].get('collection_name')
            display.deprecated("%s option, %s%s" % (name, why, alt),
                               version=ver, date=date, collection_name=collection_name)


    def validate_conflicts(self, op, runas_opts=False, fork_opts=False):
        ''' check for conflicting options '''

        if fork_opts:
            if op.forks < 1:
                self.parser.error("The number of processes (--forks) must be >= 1")

        return op

    @abstractmethod
    def init_parser(self, usage="", desc=None, epilog=None):
        """
        Create an options parser for most ansible scripts

        Subclasses need to implement this method.  They will usually call the base class's
        init_parser to create a basic version and then add their own options on top of that.

        An implementation will look something like this::

            def init_parser(self):
                super(MyCLI, self).init_parser(usage="My Ansible CLI", inventory_opts=True)
                ansible.arguments.option_helpers.add_runas_options(self.parser)
                self.parser.add_option('--my-option', dest='my_option', action='store')
        """
        self.parser = opt_help.create_base_parser(self.name, usage=usage, desc=desc, epilog=epilog)

    @abstractmethod
    def post_process_args(self, options):
        """Process the command line args

        Subclasses need to implement this method.  This method validates and transforms the command
        line arguments.  It can be used to check whether conflicting values were given, whether filenames
        exist, etc.

        An implementation will look something like this::

            def post_process_args(self, options):
                options = super(MyCLI, self).post_process_args(options)
                if options.addition and options.subtraction:
                    raise AnsibleOptionsError('Only one of --addition and --subtraction can be specified')
                if isinstance(options.listofhosts, string_types):
                    options.listofhosts = string_types.split(',')
                return options
        """

        # process tags
        if hasattr(options, 'tags') and not options.tags:
            # optparse defaults does not do what's expected
            # More specifically, we want `--tags` to be additive. So we cannot
            # simply change C.TAGS_RUN's default to ["all"] because then passing
            # --tags foo would cause us to have ['all', 'foo']
            options.tags = ['all']
        if hasattr(options, 'tags') and options.tags:
            tags = set()
            for tag_set in options.tags:
                for tag in tag_set.split(u','):
                    tags.add(tag.strip())
            options.tags = list(tags)

        # process skip_tags
        if hasattr(options, 'skip_tags') and options.skip_tags:
            skip_tags = set()
            for tag_set in options.skip_tags:
                for tag in tag_set.split(u','):
                    skip_tags.add(tag.strip())
            options.skip_tags = list(skip_tags)

        # Make sure path argument doesn't have a backslash
        if hasattr(options, 'action') and options.action in ['install', 'download'] and hasattr(options, 'args'):
            options.args = [path.rstrip("/") for path in options.args]

        # process inventory options except for CLIs that require their own processing
        if hasattr(options, 'inventory') and not self.SKIP_INVENTORY_DEFAULTS:

            if options.inventory:

                # should always be list
                if isinstance(options.inventory, string_types):
                    options.inventory = [options.inventory]

                # Ensure full paths when needed
                options.inventory = [unfrackpath(opt, follow=False) if ',' not in opt else opt for opt in options.inventory]
            else:
                options.inventory = C.DEFAULT_HOST_LIST

        return options

    def parse(self):
        """Parse the command line args

        This method parses the command line arguments.  It uses the parser
        stored in the self.parser attribute and saves the args and options in
        context.CLIARGS.

        Subclasses need to implement two helper methods, init_parser() and post_process_args() which
        are called from this function before and after parsing the arguments.
        """
        self.init_parser()

        if HAS_ARGCOMPLETE:
            argcomplete.autocomplete(self.parser)

        try:
            options = self.parser.parse_args(self.args[1:])
        except SystemExit as ex:
            if ex.code != 0:
                self.parser.exit(status=2, message=" \n%s" % self.parser.format_help())
            raise
        options = self.post_process_args(options)
        context._init_global_context(options)

    @staticmethod
    def version_info(gitinfo=False):
        ''' return full ansible version info '''
        if gitinfo:
            # expensive call, user with care
            ansible_version_string = opt_help.version()
        else:
            ansible_version_string = __version__
        ansible_version = ansible_version_string.split()[0]
        ansible_versions = ansible_version.split('.')
        for counter in range(len(ansible_versions)):
            if ansible_versions[counter] == "":
                ansible_versions[counter] = 0
            try:
                ansible_versions[counter] = int(ansible_versions[counter])
            except Exception:
                pass
        if len(ansible_versions) < 3:
            for counter in range(len(ansible_versions), 3):
                ansible_versions.append(0)
        return {'string': ansible_version_string.strip(),
                'full': ansible_version,
                'major': ansible_versions[0],
                'minor': ansible_versions[1],
                'revision': ansible_versions[2]}

    @staticmethod
    def pager(text):
        ''' find reasonable way to display text '''
        # this is a much simpler form of what is in pydoc.py
        if not sys.stdout.isatty():
            display.display(text, screen_only=True)
        elif CLI.PAGER:
            if sys.platform == 'win32':
                display.display(text, screen_only=True)
            else:
                CLI.pager_pipe(text)
        else:
            p = subprocess.Popen('less --version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.communicate()
            if p.returncode == 0:
                CLI.pager_pipe(text, 'less')
            else:
                display.display(text, screen_only=True)

    @staticmethod
    def pager_pipe(text):
        ''' pipe text through a pager '''
        if 'less' in CLI.PAGER:
            os.environ['LESS'] = CLI.LESS_OPTS
        try:
            cmd = subprocess.Popen(CLI.PAGER, shell=True, stdin=subprocess.PIPE, stdout=sys.stdout)
            cmd.communicate(input=to_bytes(text))
        except IOError:
            pass
        except KeyboardInterrupt:
            pass

    @classmethod
    def cli_executor(cls, args=None):
        if args is None:
            args = sys.argv

        try:
            display.debug("starting run")

            ansible_dir = Path(C.ANSIBLE_HOME).expanduser()
            try:
                ansible_dir.mkdir(mode=0o700)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    display.warning(
                        "Failed to create the directory '%s': %s" % (ansible_dir, to_text(exc, errors='surrogate_or_replace'))
                    )
            else:
                display.debug("Created the '%s' directory" % ansible_dir)

            try:
                args = [to_text(a, errors='surrogate_or_strict') for a in args]
            except UnicodeError:
                display.error('Command line args are not in utf-8, unable to continue.  Ansible currently only understands utf-8')
                display.display(u"The full traceback was:\n\n%s" % to_text(traceback.format_exc()))
                exit_code = 6
            else:
                cli = cls(args)
                exit_code = cli.run()

        except AnsibleOptionsError as e:
            cli.parser.print_help()
            display.error(to_text(e), wrap_text=False)
            exit_code = 5
        except AnsibleParserError as e:
            display.error(to_text(e), wrap_text=False)
            exit_code = 4
    # TQM takes care of these, but leaving comment to reserve the exit codes
    #    except AnsibleHostUnreachable as e:
    #        display.error(str(e))
    #        exit_code = 3
    #    except AnsibleHostFailed as e:
    #        display.error(str(e))
    #        exit_code = 2
        except AnsibleError as e:
            display.error(to_text(e), wrap_text=False)
            exit_code = 1
        except KeyboardInterrupt:
            display.error("User interrupted execution")
            exit_code = 99
        except Exception as e:
            if C.DEFAULT_DEBUG:
                # Show raw stacktraces in debug mode, It also allow pdb to
                # enter post mortem mode.
                raise
            have_cli_options = bool(context.CLIARGS)
            display.error("Unexpected Exception, this is probably a bug: %s" % to_text(e), wrap_text=False)
            if not have_cli_options or have_cli_options and context.CLIARGS['verbosity'] > 2:
                log_only = False
                if hasattr(e, 'orig_exc'):
                    display.vvv('\nexception type: %s' % to_text(type(e.orig_exc)))
                    why = to_text(e.orig_exc)
                    if to_text(e) != why:
                        display.vvv('\noriginal msg: %s' % why)
            else:
                display.display("to see the full traceback, use -vvv")
                log_only = True
            display.display(u"the full traceback was:\n\n%s" % to_text(traceback.format_exc()), log_only=log_only)
            exit_code = 250

        sys.exit(exit_code)
