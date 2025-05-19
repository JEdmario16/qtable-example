import pygame


class Container:

    def __init__(
        self,
        *,
        surface: pygame.Surface,
        width: int,
        height: int,
        size_mode: str = "pixel",
        position: tuple[int, int] = (0, 0),
        fill_color: tuple[int, int, int] = (0, 0, 0),
        border_color: tuple[int, int, int] = (255, 255, 255),
        alpha: float = 1.0,
        border_width: int = 1,
        border_radius: int = 0,
        border_style: str = "solid",
    ):
        """
        Initialize the container.

        Args:
            surface (pygame.Surface): The surface to draw the container on.
            width (int): The width of the container.
            height (int): The height of the container.
            position (tuple[int, int]): The position of the container relative to the surface.
            fill_color (tuple[int, int, int]): The fill color of the container.
            border_color (tuple[int, int, int]): The border color of the container.
            alpha (float): The alpha value for transparency (0.0 to 1.0).
            border_width (int): The width of the border.
            border_radius (int): The radius of the corners.
            border_style (str): The style of the border ("solid", "dashed", "dotted").
        """
        self.base_surface = surface
        self.width, self.height = self.get_size_from_mode(size_mode, width, height)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.fill_color = fill_color
        self.border_color = border_color
        self.alpha = alpha
        self.border_width = border_width
        self.border_radius = border_radius
        self.border_style = border_style

        self._childs = []

    def get_size_from_mode(
        self, size_mode: str, width: int, height: int
    ) -> tuple[int, int]:
        """
        Get the size of the container based on the size mode.
        Args:
            size_mode (str): The size mode ("pixel" or "percent").
            width (int): The width of the container.
            height (int): The height of the container.
        Returns:
            tuple[int, int]: The size of the container.
        """
        if size_mode == "pixel":
            return width, height
        elif size_mode == "percent":
            screen_width, screen_height = self.base_surface.get_size()
            return int(screen_width * (width / 100)), int(
                screen_height * (height / 100)
            )
        else:
            raise ValueError("Invalid size mode. Use 'pixel' or 'percent'.")

    def draw(self):
        """
        Draw the container on the surface.
        """
        # Set the alpha value for transparency
        self.image.set_alpha(int(self.alpha * 255))

        # Draw the fill color
        self.image.fill(self.fill_color)

        # Draw the border style
        # TODO - Implement border styles (solid, dashed, dotted)

        self.base_surface.blit(self.image, self.rect)

    def update(self):
        """
        Update the container (if needed).
        """
        # Update logic can be added here if needed
        self.image.set_alpha(int(self.alpha * 255))
        self.image.fill(self.fill_color)
        self.base_surface.blit(self.image, self.rect)

        for child in self._childs:
            child.update()
            self.base_surface.blit(child.image, child.rect)

    def set_position(self, position: tuple[int, int]):
        """
        Set the position of the container.

        Args:
            position (tuple[int, int]): The new position of the container.
        """
        self.rect.topleft = position

    def add_child(self, child: pygame.sprite.Sprite):
        """
        Add a child sprite to the container.

        Args:
            child (pygame.sprite.Sprite): The child sprite to add.
        """
        self._childs.append(child)
