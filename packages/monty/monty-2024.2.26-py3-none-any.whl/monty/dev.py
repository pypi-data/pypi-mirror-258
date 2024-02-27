"""
This module implements several useful functions and decorators that can be
particularly useful for developers. E.g., deprecating methods / classes, etc.
"""

import functools
import logging
import sys
import warnings

logger = logging.getLogger(__name__)


def deprecated(replacement=None, message=None, category=FutureWarning):
    """
    Decorator to mark classes or functions as deprecated, with a possible replacement.

    Args:
        replacement (callable): A replacement class or method.
        message (str): A warning message to be displayed.
        category (Warning): Choose the category of the warning to issue. Defaults
            to FutureWarning. Another choice can be DeprecationWarning. NOte that
            FutureWarning is meant for end users and is always shown unless silenced.
            DeprecationWarning is meant for developers and is never shown unless
            python is run in developmental mode or the filter is changed. Make
            the choice accordingly.

    Returns:
        Original function, but with a warning to use the updated class.
    """

    def craft_message(old, replacement, message):
        msg = f"{old.__name__} is deprecated"
        if replacement is not None:
            if isinstance(replacement, property):
                r = replacement.fget
            elif isinstance(replacement, (classmethod, staticmethod)):
                r = replacement.__func__
            else:
                r = replacement
            msg += f"; use {r.__name__} in {r.__module__} instead."
        if message is not None:
            msg += "\n" + message
        return msg

    def deprecated_decorator(old):
        def wrapped(*args, **kwargs):
            msg = craft_message(old, replacement, message)
            warnings.warn(msg, category=category, stacklevel=2)
            return old(*args, **kwargs)

        return wrapped

    return deprecated_decorator


class requires:
    """
    Decorator to mark classes or functions as requiring a specified condition
    to be true. This can be used to present useful error messages for
    optional dependencies. For example, decorating the following code will
    check if scipy is present and if not, a runtime error will be raised if
    someone attempts to call the use_scipy function::

        try:
            import scipy
        except ImportError:
            scipy = None

        @requires(scipy is not None, "scipy is not present.")
        def use_scipy():
            print(scipy.majver)

    Args:
        condition: Condition necessary to use the class or function.
        message: A message to be displayed if the condition is not True.
    """

    def __init__(
        self, condition: bool, message: str, err_cls: type[Exception] = RuntimeError
    ) -> None:
        """
        :param condition: A expression returning a bool.
        :param message: Message to display if condition is False.
        """
        self.condition = condition
        self.message = message
        self.err_cls = err_cls

    def __call__(self, _callable):
        """
        :param _callable: Callable function.
        """

        @functools.wraps(_callable)
        def decorated(*args, **kwargs):
            if not self.condition:
                raise self.err_cls(self.message)
            return _callable(*args, **kwargs)

        return decorated


def install_excepthook(hook_type="color", **kwargs):
    """
    This function replaces the original python traceback with an improved
    version from Ipython. Use `color` for colourful traceback formatting,
    `verbose` for Ka-Ping Yee's "cgitb.py" version kwargs are the keyword
    arguments passed to the constructor. See IPython.core.ultratb.py for more
    info.

    Return:
        0 if hook is installed successfully.
    """
    try:
        from IPython.core import ultratb  # pylint: disable=import-outside-toplevel
    except ImportError:
        warnings.warn("Cannot install excepthook, IPyhon.core.ultratb not available")
        return 1

    # Select the hook.
    hook = dict(
        color=ultratb.ColorTB,
        verbose=ultratb.VerboseTB,
    ).get(hook_type.lower(), None)

    if hook is None:
        return 2

    sys.excepthook = hook(**kwargs)
    return 0
