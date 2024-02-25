import sys

from .user import *

if DIR_UWS:
    sys.path.insert(0, f'{DIR_UWS}/.uniws')
    from hardware import hardware
    from software import software
else:
    def hardware() -> 'list[Hardware]':
        return []

    def software() -> 'list[Software]':
        return []


class AppWorkspace(App):
    '''
    An application to initialize a uniform workspace: `uws`.
    '''

    def __init__(self) -> 'None':
        super().__init__(
            help='Initialize an empty workspace.',
        )
        self.arg_remote = Arg(
            name='URI',
            sopt='r',
            lopt='remote',
            help='A Git remote to set as the origin.',
        )
        self.args.append(self.arg_remote)
        self.arg_branch = Arg(
            name='NAME',
            sopt='b',
            lopt='branch',
            help='A Git branch to set as the default.',
        )
        self.args.append(self.arg_branch)
        self.arg_dir = Arg(
            name='DIR',
            count='?',
            default=DIR_PWD,
            help='A non-existing or empty directory.',
        )
        self.args.append(self.arg_dir)

    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        dir = os.path.abspath(args[self.arg_dir])
        if os.path.exists(dir):
            if os.path.isdir(dir):
                if len(os.listdir(dir)) != 0:
                    raise CallError(f'The directory is not empty: {dir}')
            else:
                raise CallError(f'Not a directory: {dir}')
        else:
            os.makedirs(dir, 0o755)
        branch = args[self.arg_branch]
        branch = f'-b {branch}' if branch else ''
        remote = args[self.arg_remote]
        remote = f'git remote add origin {remote}' if remote else 'true'
        sh(f'true'
           f' && cp -RaT {os.path.dirname(__file__)}/template {dir}'
           f' && cd {dir}'
           f' && git init {branch}'
           f' && {remote}'
           f' && git add -A'
           f' && git commit -m "Initial commit"'
           f';')


class AppWare(App):
    '''
    A hardware or software action application (`uh*` or `us*`).
    '''

    def __init__(
        self,
        ware: 'list[Hardware | Software]',
        name: 'str',
        help: 'str',
    ) -> 'None':
        '''
        Create an instance.
        Introduces two internal fields:
         * `app`   - a substitute `App`. This is for cases when only one
           instance of `Hardware` or `Software` is defined. The corresponding
           `App` fields (`action`, `download`, `test`) can be "merged" into
           the action application (`uha`, `usd`, `ust`).
         * `error` - an error message. If not empty, a `CallError` will be
           raised before any other action.

        Parameters:
         * `ware` - a list obtained by running `hardware()` or `software()`.
         * `name` - the action name, must correspond to one of the fields
           in `Hardware` or `Software`, e.g. "action", "download", "test".
           It is not used as the application name.
         * `help` - corresponds to `App.help`.
        '''
        super().__init__(help=help)
        # Pick only apps that support the given command.
        for x in ware:
            app: 'App' = getattr(x, f'app_{name}')
            if app:
                app.name = x.name
                self.apps.append(app)
        # Return immediately if nothing supports the given command.
        self.error = ''
        if not self.apps:
            self.error = f'Nothing supports {name}.'
            return
        # Special case when there is only one item in ware.
        # Merge it into the main one for convenience.
        self.app = None
        if len(ware) == 1:
            self.app = self.apps.pop()
            self.help = self.app.help or self.help
            self.prolog = self.app.prolog or self.prolog
            self.epilog = self.app.epilog or self.epilog
            self.args.extend(self.app.args)
            self.apps.extend(self.app.apps)

    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        '''
        Execute `self.app`, if not `None`. Otherwise no-op.

        Exceptions:
         * `CallError`, if `DIR_UWS` is not defined.
         * `CallError`, if `self.error` is not empty.
        '''
        if not DIR_UWS:
            self.error = 'This command must be run in a workspace.'
        if self.error:
            raise CallError(self.error)
        if self.app:
            self.app(args, apps)
