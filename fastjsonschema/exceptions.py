class JsonSchemaException(ValueError):
    """
    Exception raised by validation function. Contains ``message`` with
    information what is wrong.

    :argument str message: Error message

    """

    def __init__(self, message):
        super().__init__()
        self.message = message
