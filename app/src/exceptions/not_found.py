"""
Custom exception for not found resources
"""


class NotFound(Exception):
    """
    Exception raised when a resource is not found in the database.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
