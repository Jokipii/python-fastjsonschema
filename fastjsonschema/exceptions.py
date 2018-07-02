"""Module for exceptions."""

class JsonSchemaException(ValueError):
    """
    Base exception.

    Exception raised by validation function. Contains ``message`` with
    information what is wrong.

    :argument str message: Error message

    """

    def __init__(self, message):
        """Init."""
        super().__init__()
        self.message = message
