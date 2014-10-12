import physics
from bubble import *
from enemy_generator import *
from game import *
from group import *
from joystick import *
from keyboard import *
from player import *
from sprite import *
from state import *


class SlappaGame(Game):
    def __init__(self):
        super(SlappaGame, self).__init__("Slappa!", SCREEN_SIZE[0], SCREEN_SIZE[1])
        self.players_joined = [False, False]

        # Input devices
        self.keys = Keyboard()
        self.joys = Joystick()


# Title screen
class TitleState(State):
    def __init__(self):
        super(TitleState, self).__init__()
        assets.images['background'] = pygame.image.load("data/images/bg.png")
        assets.images['logo'] = pygame.image.load("data/images/logo.png")
        assets.images['gong'] = pygame.image.load("data/images/gong.png")
        assets.images['keyboard'] = pygame.image.load("data/images/keyboard.png")
        assets.images['xbox360'] = pygame.image.load("data/images/xbox360.png")
        assets.sounds['gong'] = pygame.mixer.Sound("data/sounds/gong.ogg")
        assets.fonts['font'] = pygame.font.Font("data/MedievalSharp.ttf", 32)
        assets.fonts['big'] = pygame.font.Font("data/MedievalSharp.ttf", 72)
        # Don't detect input for a bit
        # To prevent capturing escape from game screen
        self.grace_timer = 30

        self.hurt_boxes = None
        self.players = None
        self.gong = None

        def preload():
            pygame.mixer.music.load("data/sounds/asian strings.ogg")
            self.grace_timer = 30
        self.preload = preload

        def create():
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.7)
            self.hurt_boxes = Group()
            self.players = Group()

            self.players.add(Player(self.game.width / 2 - 48, FLOOR_Y,
                                    'cat',
                                    self.hurt_boxes))
            self.players.add(Player(self.game.width / 2 + 48, FLOOR_Y,
                                    'dog',
                                    self.hurt_boxes))
            for player in self.players:
                player.health = 0
                player.is_dying = True
                player.animations.play('die')
            self.game.players_joined = [False, False]
            self.gong = Sprite(self.game.width / 2, FLOOR_Y, 'gong', Point(2, 2))
            self.gong.anchor.y = 1
        self.create = create

        def update(time):
            self.grace_timer -= 1
            if self.grace_timer <= 0:
                self.game.keys.update()
                if self.game.keys.is_escape():
                    self.is_quit = True
                self.game.joys.update()

            # Detect input and add player
            if self.game.keys.dir() != 0 or self.game.keys.is_jump() or self.game.keys.hit() != "":
                self.players[0].health = 5
                self.game.players_joined[0] = True
            if self.game.joys.dir() != 0 or self.game.joys.is_jump() or self.game.joys.hit() != "":
                self.players[1].health = 5
                self.game.players_joined[1] = True

            for i in range(len(self.players)):
                player = self.players[i]
                if i == 0:
                    player.hit(self.game.keys.hit())
                    player.move(self.game.keys.dir())
                    if self.game.keys.is_jump():
                        player.jump()
                elif i == 1:
                    player.hit(self.game.joys.hit())
                    player.move(self.game.joys.dir())
                    if self.game.joys.is_jump():
                        player.jump()
                player.update(time)
            self.hurt_boxes.update(time)

            # Hit gong
            def gong_hit(g, h):
                assets.sounds['gong'].play()
                self.state.start('game')
            gongs = Group()
            gongs.add(self.gong)
            physics.overlap(gongs, self.hurt_boxes, gong_hit)

            self.gong.update(time)
        self.update = update

        def draw(surface):
            surface.blit(assets.images['background'], (0, 0))
            s = assets.images['logo']
            surface.blit(s, ((self.game.width - s.get_width()) / 2,
                             (self.game.height - s.get_height()) / 2))
            font = assets.fonts['big']
            surface.blit(font.render("Slappa!",
                                     True,
                                     (255, 140, 160)),
                         (280, self.game.height / 2))
            font = assets.fonts['font']
            s = assets.images['keyboard']
            padding = 25
            surface.blit(s, ((padding,
                             (self.game.height - s.get_height() - padding))))
            s = assets.images['xbox360']
            surface.blit(s, (self.game.width - s.get_width() - padding,
                             self.game.height - s.get_height() - padding))
            self.gong.draw(surface)
            for player in self.players:
                player.draw(surface)
        self.draw = draw


# Game state
class GameState(State):
    def __init__(self):
        super(GameState, self).__init__()
        self.score = 0
        self.bubbles = None
        self.enemies = None
        self.thing_group = None
        self.hurt_boxes = None
        self.players = None
        self.enemy_generator = None
        # Sounds
        assets.sounds['hits'] = load_sounds_from_folder("hits")
        assets.sounds['jump'] = pygame.mixer.Sound("data/sounds/jump.ogg")
        assets.sounds['land'] = pygame.mixer.Sound("data/sounds/land.ogg")
        assets.sounds['swings'] = load_sounds_from_folder("swings")
        assets.sounds['meow'] = pygame.mixer.Sound("data/sounds/meow.ogg")
        assets.sounds['yelp'] = pygame.mixer.Sound("data/sounds/yelp.ogg")
        assets.sounds['growls'] = load_sounds_from_folder("growls")
        assets.sounds['deaths'] = load_sounds_from_folder("deaths")

        # Images/templates
        assets.images['explosion'] = pygame.image.load("data/images/explosion.png")
        assets.images['cat'] = pygame.image.load("data/images/players/cat.png")
        assets.images['dog'] = pygame.image.load("data/images/players/dog.png")
        assets.images['zombie'] = pygame.image.load("data/images/enemies/zombie.png")
        assets.images['monster'] = pygame.image.load(
            "data/images/enemies/monster.png")
        assets.images['flying'] = pygame.image.load("data/images/enemies/flying.png")

        def create():
            pygame.mixer.music.load("data/sounds/Blackmoor Ninjas.ogg")
            self.score = 0
            self.bubbles = Group()
            self.enemies = Group()
            self.thing_group = Group()
            self.hurt_boxes = Group()
            self.players = Group()
            self.enemy_generator = EnemyGenerator(
                self.enemies, self.players, self.thing_group)

            self.players.add(Player(SCREEN_SIZE[0] / 2 - 48, FLOOR_Y,
                                    'cat',
                                    self.hurt_boxes))
            self.players.add(Player(SCREEN_SIZE[0] / 2 + 48, FLOOR_Y,
                                    'dog',
                                    self.hurt_boxes))
            if not self.game.players_joined[0]:
                self.players[0].health = 0
                self.players[0].is_dying = True
                self.players[0].animations.play('die')
            if not self.game.players_joined[1]:
                self.players[1].health = 0
                self.players[1].is_dying = True
                self.players[1].animations.play('die')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.7)
        self.create = create

        def update(time):
            # Keys
            self.game.keys.update()
            if self.game.keys.is_escape():
                self.state.start('title')
                return
            self.game.joys.update()

            # Detect input and add player
            if (not self.game.players_joined[0] and
                    (self.game.keys.dir() != 0 or self.game.keys.is_jump() or self.game.keys.hit() != "")):
                self.players[0].health = 5
                self.game.players_joined[0] = True
            if (not self.game.players_joined[1] and
                    (self.game.joys.dir() != 0 or self.game.joys.is_jump() or self.game.joys.hit() != "")):
                self.players[1].health = 5
                self.game.players_joined[1] = True

            #Update
            for i in range(len(self.players)):
                player = self.players[i]
                if i == 0:
                    player.hit(self.game.keys.hit())
                    player.move(self.game.keys.dir())
                    if self.game.keys.is_jump():
                        player.jump()
                elif i == 1:
                    player.hit(self.game.joys.hit())
                    player.move(self.game.joys.dir())
                    if self.game.joys.is_jump():
                        player.jump()
                player.update(time)

            # remove dead enemies
            self.enemy_generator.update(time)
            self.enemies.update(time)
            # remove out of bounds things
            self.thing_group.update(time)
            self.hurt_boxes.update(time)
            self.bubbles.update(time)

            # Collisions
            def hit(x, y):
                random.choice(assets.sounds['hits']).play()
                self.bubbles.add(Bubble(x, y))

            def enemy_hurt(e, h):
                if not h.has_hit_monster:
                    if e.hurt():
                        hit((e.x + h.x) / 2, (e.y + h.y) / 2)
                        h.has_hit_monster = True
                        self.score += 1
            physics.overlap(self.enemies, self.hurt_boxes, enemy_hurt)

            # things get hit and become players'
            def things_hit(t, h):
                if t.is_enemy:
                    t.hit(h.player, self.enemies)
                    hit((t.x + h.x) / 2, (t.y + h.y) / 2)
                    self.score += 1
            physics.overlap(self.thing_group,
                            self.hurt_boxes,
                            things_hit)

            def enemy_get_hit(e, t):
                if not t.is_enemy and t.health > 0:
                    if e.hurt():
                        t.health = 0
                        hit((e.x + t.x) / 2, (e.y + t.y) / 2)
                        self.score += 2
            physics.overlap(self.enemies,
                            self.thing_group,
                            enemy_get_hit)

            def player_get_hit(p, t):
                if t.is_enemy:
                    if p.hurt():
                        t.health = 0
                        hit((p.x + t.x) / 2, (p.y + t.y) / 2)
            physics.overlap(self.players,
                            self.thing_group,
                            player_get_hit)
        self.update = update

        def draw(surface):
            #Render
            surface.blit(assets.images['background'], (0, 0))
            for enemy in self.enemies:
                enemy.draw(surface)
            for player in self.players:
                player.draw(surface)
            for thing in self.thing_group:
                thing.draw(surface)
            for box in self.hurt_boxes:
                box.draw(surface)
            for bubble in self.bubbles:
                bubble.draw(surface)
            font = assets.fonts['font']
            padding = 25
            players_alive = 0
            for i in range(len(self.players)):
                player = self.players[i]
                x = padding
                if i == 1:
                    x = self.game.width - 100 - padding
                surface.blit(font.render("HP: " + str(player.health),
                                         True,
                                         (0, 255, 0)),
                             (x, self.game.height - 25 - padding))
                if player.health > 0:
                    players_alive += 1
            surface.blit(font.render("Score: " + str(self.score),
                                     True,
                                     (255, 255, 0)),
                         (self.game.width / 2 - 100, 50))
            if players_alive == 0:
                font = assets.fonts['big']
                surface.blit(font.render("YOU LOSE", True, (255, 255, 255)),
                             (self.game.width / 2 - 150, self.game.height / 2 - 50))
        self.draw = draw


def main():
    game = SlappaGame()
    game.state.add('game', GameState())
    game.state.add('title', TitleState())
    game.state.start('title')


if __name__ == '__main__':
    main()