"""
A context manager that can be used to determine if we're executing inside of
a Typer command. This is analogous to click's get_current_context but for
command execution.
"""

import typing as t
from contextlib import contextmanager
from threading import local

from django.conf import settings

# DO NOT IMPORT ANYTHING FROM TYPER HERE - SEE patch.py


def traceback_config() -> t.Union[bool, t.Dict[str, t.Any]]:
    """
    Fetch the rich traceback installation parameters from our settings. By default
    rich tracebacks are on with show_locals = True. If the config is set to False
    or None rich tracebacks will not be installed even if the library is present.

    This allows us to have a common traceback configuration for all commands. If rich
    tracebacks are managed separately this setting can also be switched off.
    """
    cfg = getattr(settings, "DT_RICH_TRACEBACK_CONFIG", {"show_locals": True})
    if cfg:
        return {"show_locals": True, **cfg}
    return bool(cfg)


_local = local()


@contextmanager
def push_command(command: "TyperCommand"):  # type: ignore
    """
    Pushes a new command to the current stack.
    """
    _local.__dict__.setdefault("stack", []).append(command)
    try:
        yield
    finally:
        _local.stack.pop()


def get_current_command() -> t.Optional["TyperCommand"]:  # type: ignore
    """
    Returns the current typer command. This can be used as a way to
    access the current command object from anywhere if we are executing
    inside of one from higher on the stack. We primarily need this because certain
    monkey patches are required in typer code - namely for enabling/disabling
    color based on configured parameters.

    :return: The current typer command or None if there is no active command.
    """
    try:
        return t.cast("TyperCommand", _local.stack[-1])  # type: ignore
    except (AttributeError, IndexError):
        pass
    return None


T = t.TypeVar("T")  # pylint: disable=C0103


def with_typehint(baseclass: t.Type[T]) -> t.Type[T]:
    """
    Type hinting mixin inheritance is really annoying. The current
    canonical way is to use Protocols but this is prohibitive when
    the super classes already exist and are extensive. All we're
    trying to do is let our type checker know about super() methods
    etc - this is a simple way to do that.
    """
    if t.TYPE_CHECKING:
        return baseclass  # pragma: no cover
    return object  # type: ignore
