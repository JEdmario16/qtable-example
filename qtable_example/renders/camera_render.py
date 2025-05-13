import pygame


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2

        # zoom
        self.zoom_scale = 1.0
        self.internal_surface_size = (4000, 4000)
        self.internal_surface = pygame.Surface(
            self.internal_surface_size, pygame.SRCALPHA
        )
        self.internal_rect = self.internal_surface.get_rect(
            center=(self.half_w, self.half_h)
        )
        self.internal_surface_size_vector = pygame.math.Vector2(
            self.internal_surface_size[0], self.internal_surface_size[1]
        )
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surface_size_vector.x // 2 - self.half_w
        self.internal_offset.y = self.internal_surface_size_vector.y // 2 - self.half_h

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.1
        elif keys[pygame.K_e]:
            self.zoom_scale -= 0.1

    def custom_draw(self, target):
        self.center_target_camera(target)

        # zoom
        self.internal_surface.fill((0, 0, 0))

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.internal_surface.blit(sprite.image, offset_pos)

        scaled_surface = pygame.transform.scale(
            self.internal_surface,
            self.internal_surface_size_vector * self.zoom_scale,
        )
        scaled_rect = scaled_surface.get_rect(
            center=(self.half_w, self.half_h)
        )

        self.display_surface.blit(
            scaled_surface,
            scaled_rect,
        )
