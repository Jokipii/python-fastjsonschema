"""Indentation module."""

def indent(func):
    """
    Indentation decorator.

    Decorator for allowing to use method as normal method or with
    context manager for auto-indenting code blocks.
    """
    def wrapper(self, *args, **kwds):
        func(self, *args, **kwds)
        return Indent(self)
    return wrapper


class Indent:
    """Indent class to keep correct imdemtation."""

    def __init__(self, instance):
        """Init."""
        self.instance = instance

    def __enter__(self):
        """Indent."""
        self.instance._indent += 1

    def __exit__(self, type_, value, traceback):
        """Dedent."""
        self.instance._indent -= 1
