class ScreenCoordinates:
    """
    Class to represent screen coordinates.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"ScreenCoordinates(x={self.x}, y={self.y})"


class GridCoordinates:
    """
    Class to represent grid coordinates.
    """

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"GridCoordinates(row={self.row}, col={self.col})"
