from animation import *
from config import *
from point import *


class Sprite(object):
    def __init__(self,
                 game,
                 x, y,
                 key,
                 scale=Point(1, 1),
                 crop=pygame.Rect(0, 0, 0, 0)):
        self.game = game
        if key != '':
            self.image = game.load.images[key]
        else:
            self.image = None

        new_scale = Point(scale.x, scale.y)
        new_scale.multiply(game.scale.scale)
        self.children = []
        self.crop = crop
        self.crop.width = int(self.crop.width * new_scale.x)
        self.crop.height = int(self.crop.height * new_scale.y)
        if (crop.width == 0 or crop.height == 0) and key != '':
            self.crop = pygame.Rect(0, 0,
                                    int(game.load.images[key].get_width() * new_scale.x),
                                    int(game.load.images[key].get_height() * new_scale.y))
        self.width = self.crop.width
        self.height = self.crop.height
        if self.image is not None:
            self.image = pygame.transform.scale(
                self.image,
                (
                    int(game.load.images[key].get_width() * new_scale.x),
                    int(game.load.images[key].get_height() * new_scale.y)))

        self.animations = AnimationManager()

        self.body = pygame.Rect(0, 0, self.width, self.height)

        self.dx = 0
        self.dy = 0
        self.x = x
        self.y = y
        self.allow_rotations = False
        # Rotation in degrees
        self.rotation = 0
        self.angular_velocity = 0

        self.alpha = 1.0
        self.flip_x = False
        self.flip_y = False

        self.health = 10
        self.out_of_bounds_kill = True
        self.gravity = 0.0

        self.anchor = Point(0.5, 0.5)

    def exists(self):
        return self.health > 0

    def update(self, time):
        if self.gravity != 0.0:
            self.dy += self.gravity * time
        self.x += self.dx * time
        self.y += self.dy * time
        if self.gravity != 0.0:
            if self.y > self.game.config.FLOOR_Y:
                self.land()
        if self.allow_rotations:
            self.rotation += self.angular_velocity * time
        self.animations.update()

        if (self.out_of_bounds_kill and (
                self.x + self.width < 0 or
                self.x - self.width > self.game.width or
                self.y + self.height < 0 or
                self.y - self.height > self.game.height)):
            self.health = 0

        self.children[:] = [
            child for child in self.children if child.exists()]
        for child in self.children:
            child.update(time)

    def land(self):
        pass

    def draw(self, surface):
        if self.game.config.DEBUG_DRAW_SPRITE_BOUNDS:
            s = pygame.Surface((self.width, self.height))
            s.set_alpha(128)
            s.fill((0, 255, 0))
            surface.blit(s, (
                self.x - self.width * self.anchor.x,
                self.y - self.height * self.anchor.y))
        if self.game.config.DEBUG_DRAW_SPRITE_BODY:
            s = pygame.Surface((self.body.width, self.body.height))
            s.set_alpha(128)
            s.fill((255, 0, 255))
            point = Point(self.x, self.y)
            point.multiply(self.game.scale.scale)
            point.add(Point(self.body.x - self.body.width / 2,
                            self.body.y - self.body.height / 2))
            surface.blit(s, (int(point.x), int(point.y)))
        if self.image is not None:
            cropped = pygame.Surface(self.crop.size)
            cropped.fill((255, 0, 255, 0))
            cropped.set_colorkey((255, 0, 255, 0))
            if self.alpha < 1.0:
                cropped.set_alpha(int(self.alpha * 255))
            crop = self.animations.get_crop(self.crop.size,
                                            self.image.get_width())
            cropped.blit(self.image, (0, 0), crop)
            cropped = pygame.transform.flip(cropped, self.flip_x, self.flip_y)

            # Check if we need to offset a bit due to rotation
            # This is because rotations can cause the surface to enlarge
            draw_size = [self.width, self.height]
            if self.allow_rotations and not self.game.config.DEBUG_NO_ROTATIONS:
                cropped = pygame.transform.rotate(cropped, self.rotation)
                draw_size = [cropped.get_width(), cropped.get_height()]
            point = Point(self.x, self.y)
            point.multiply(self.game.scale.scale)
            point.subtract(Point(draw_size[0] * self.anchor.x,
                                 draw_size[1] * self.anchor.y))
            surface.blit(cropped, (int(point.x), int(point.y)))
        if self.game.config.DEBUG_DRAW_SPRITE_ANCHOR:
            point = Point(self.x, self.y)
            point.multiply(self.game.scale.scale)
            pygame.draw.circle(surface,
                               (0, 0, 255),
                               (int(point.x), int(point.y)),
                               3,
                               0)

        for child in self.children:
            child.draw(surface)

    def get_body_center(self):
        return Point(self.x + self.body.x, self.y + self.body.y)