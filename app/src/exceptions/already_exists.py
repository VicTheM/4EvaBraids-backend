"""
Exception raised when a resource already exists in the database.
"""


class AlreadyExists(Exception):
    """
    Exception raised when an attempt is made to create an entity that already exists.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
