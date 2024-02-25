import os
import subprocess
from argapp import *


def __pwd() -> 'str':
    return os.path.abspath(os.getenv('PWD'))


def __root() -> 'str':
    result = __pwd()
    while result != '/':
        if os.path.exists(f'{result}/.uniws'):
            return result
        result = os.path.dirname(result)
    return ''


DIR_PWD = __pwd()
'''
The current working directory.
'''

DIR_UWS = __root()
'''
The workspace root.
The first directory that contains a `.uniws` subdirectory.
'''

DIR_UNI = f'{DIR_UWS}/.uniws'
'''
`DIR_UWS/.uniws`
'''

DIR_BIN = f'{DIR_UWS}/bin'
'''
`DIR_UWS/bin`
'''

DIR_ETC = f'{DIR_UWS}/etc'
'''
`DIR_UWS/etc`
'''

DIR_LIB = f'{DIR_UWS}/lib'
'''
`DIR_UWS/lib`
'''

DIR_TMP = f'{DIR_UWS}/tmp'
'''
`DIR_UWS/tmp`
'''


class Hardware(App):
    '''
    A hardware representation, `name` serves as a unique identifier
    and as a value for a command line argument, if multiple hardwares
    are available.

    The `app_*` application fields correspond to the `uh*` commands,
    and can be identified by the first letter.
    Implement them as any other `App` - uniws takes care of the rest.
    Note that the `App.name` will be set to `Hardware.name`, though.

    It is not necessary to implement everything. Not applicable fields
    may be left as is (`None`).

    The fields are only suggestions and hints what to do. There are no
    UI/UX expectations, so the actual implementation can do whatever.
    '''

    def __init__(self, name: 'str') -> 'None':
        super().__init__(name=name)
        self.app_connect: 'App' = None
        self.app_power: 'App' = None
        self.app_upload: 'App' = None
        self.app_download: 'App' = None
        self.app_shell: 'App' = None
        self.app_action: 'App' = None


class Software(App):
    '''
    A software representation, `name` serves as a unique identifier
    and as a value for a command line argument, if multiple softwares
    are available.

    The `app_*` application fields correspond to the `us*` commands,
    and can be identified by the first letter.
    Implement them as any other `App` - uniws takes care of the rest.
    Note that the `App.name` will be set to `Software.name`, though.

    It is not necessary to implement everything. Not applicable fields
    may be left as is (`None`).

    The fields are only suggestions and hints what to do. There are no
    UI/UX expectations, so the actual implementation can do whatever.
    '''

    def __init__(self, name: 'str') -> 'None':
        super().__init__(name=name)
        self.app_download: 'App' = None
        self.app_build: 'App' = None
        self.app_install: 'App' = None
        self.app_test: 'App' = None
        self.app_clean: 'App' = None
        self.app_action: 'App' = None


class ShellResult:
    '''
    The result of a shell command execution.
    '''

    def __init__(
        self,
        command: 'str',
        output: 'str',
        code: 'int',
    ) -> 'None':
        '''
        The constructor.

        Parameters:
         * `command` - corresponds to `self.command`.
         * `output`  - corresponds to `self.output`.
         * `code`    - corresponds to `self.code`.
        '''
        if code < 0 or code > 255:
            code = 1
        self.__command = command
        self.__output = output
        self.__code = code

    @property
    def command(self) -> 'str':
        '''
        The command that was run.
        '''
        return self.__command

    @property
    def output(self) -> 'str':
        '''
        The command's stdout and stderr, if captured.
        '''
        return self.__output

    @property
    def code(self) -> 'int':
        '''
        The command's return code.
        Note that it will be set to 1 if the range is not between 0 and 255.
        '''
        return self.__code


class ShellError(CallError):
    '''
    The error raised for a shell command execution.
    '''

    def __init__(self, result: 'ShellResult') -> 'None':
        '''
        The constructor.

        Parameters:
         * `result` - `ShellResult` to initialize the corresponding fields.
        '''
        super().__init__(
            text=str(
                f'The command failed with the exit code {result.code}:\n'
                f'{result.command}'
            ),
            code=result.code,
        )
        self.__result = result

    @property
    def command(self) -> 'str':
        '''
        Corresponds to `ShellResult.command`.
        '''
        return self.__result.command

    @property
    def output(self) -> 'str':
        '''
        Corresponds to `ShellResult.output`.
        '''
        return self.__result.output


def sh(
    command: 'str',
    capture: 'bool' = False,
    check: 'bool' = True,
) -> 'ShellResult':
    '''
    Execute a shell command, note that:
     * `/bin/bash` is used as the shell.
     * `expand_aliases` is enabled prior to execution.
     * `DIR_UNI/.bashrc` is sourced prior to execution, if present.
     * `PATH` is extended with `DIR_BIN` if there is no `DIR_UNI/.bashrc`.

    Parameters:
     * `command` - a shell command to execute. The original value is never
       modified, but extra commands are prepended (see above).
     * `capture` - whether to capture the output (both stdout and stderr).
     * `check`   - whether to raise a `ShellError` if the return code is not zero.

    Exceptions:
     * `ShellError`, if `check` is `True` and `command` returns a non-zero code.

    Returns:
     * `ShellResult`, with the fields properly set.
    '''

    bashrc = f'{DIR_UNI}/.bashrc'
    if os.path.isfile(bashrc):
        command = f'source {bashrc};\n{command}'
    elif DIR_UWS:
        PATH = f'export PATH={DIR_BIN}:$PATH'
        command = f'{PATH};\n{command}'
    command = f'shopt -s expand_aliases;\n{command}'
    args = [command]
    kwargs = {
        'shell': True,
        'universal_newlines': True,
        'executable': '/bin/bash',
    }
    if capture:
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.STDOUT
    proc = subprocess.Popen(*args, **kwargs)
    proc.wait()
    result = ShellResult(
        command=command,
        output=('' if not capture else proc.stdout.read()),
        code=proc.returncode,
    )
    if check and result.code != 0:
        raise ShellError(result)
    return result
