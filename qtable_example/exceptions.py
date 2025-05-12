class OutOfBoundsError(Exception):
    """Exception raised when a position is out of grid bounds."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AlreadyOccupiedError(Exception):
    """Exception raised when a position is already occupied."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
