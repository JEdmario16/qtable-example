import pygame

from qtable_example.renders.camera_render import CameraGroup


class CameraCenter(pygame.sprite.Sprite):
    """
    Representa um sprite que centraliza a câmera em torno de um alvo.
    Esta classe é utilizada para servir como um ponto de referência para a câmera,
    permitindo que a câmera siga o movimento do sprite.

    """

    def __init__(self, camera_group: CameraGroup):
        super().__init__(camera_group)
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect(center=(0, 0))
        self.camera_group = camera_group
        self.direction = pygame.Vector2(0, 0)
        self.speed = 5

    def update(self):
        self.input()
        self.rect.center += self.direction * self.speed

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
