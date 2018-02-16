from __future__ import unicode_literals
import sys

from prompt_toolkit.eventloop.context import TaskLocal, TaskLocalNotSetError
from prompt_toolkit.utils import is_windows, is_conemu_ansi, get_term_environment_variable
from .base import Output

__all__ = [
    'create_output',
    'get_default_output',
    'set_default_output',
]


def create_output(stdout=None):
    """
    Return an :class:`~prompt_toolkit.output.Output` instance for the command
    line.

    :param color_depth: Any `ColorDepth` value, a callable that returns a
        `ColorDepth` or `None` for default.
    """
    stdout = stdout or sys.__stdout__

    if is_windows():
        from .conemu import ConEmuOutput
        from .win32 import Win32Output
        from .windows10 import is_win_vt100_enabled, Windows10_Output

        if is_win_vt100_enabled():
            return Windows10_Output(stdout)
        if is_conemu_ansi():
            return ConEmuOutput(stdout)
        else:
            return Win32Output(stdout)
    else:
        from .vt100 import Vt100_Output
        return Vt100_Output.from_pty(
            stdout, term=get_term_environment_variable())


_default_output = TaskLocal()


def get_default_output():
    """
    Get the output class to be used by default.

    Called when creating a new Application(), when no `Output` has been passed.
    """
    try:
        value = _default_output.get()
    except TaskLocalNotSetError:
        return create_output()
    else:
        return value


def set_default_output(output):
    """
    Set the default `Output` class.
    """
    assert isinstance(output, Output)
    _default_output.set(output)
