#!/usr/bin/env python
import itertools
import physics
from bubble import *
from enemy_generator import *
from game import *
from high_score import *
from joystick import *
from keyboard import *
from player import *
from sprite import *
from state import *


class SlappaGame(Game):
    def __init__(self):
        super(SlappaGame, self).__init__("Slappa!", GAME_SIZE[0], GAME_SIZE[1])
        self.scale.setup_scale(SCREEN_SIZE[0], SCREEN_SIZE[1])
        self.players_joined = [False, False]

        # Input devices
        self.keys = Keyboard()
        self.joys = Joystick()


# Title screen
class TitleState(State):
    def __init__(self):
        super(TitleState, self).__init__()
        assets.images['background'] = pygame.image.load("data/images/bg.png")
        assets.images['ground'] = pygame.image.load("data/images/ground.png")
        assets.images['logo'] = pygame.image.load("data/images/logo.png")
        assets.images['gong'] = pygame.image.load("data/images/gong.png")
        assets.images['keyboard'] = pygame.image.load("data/images/keyboard.png")
        assets.images['xbox360'] = pygame.image.load("data/images/xbox360.png")
        assets.images['gcw-zero'] = pygame.image.load("data/images/gcw-zero.png")
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

            bg = self.game.add.image(0, 0, 'background')
            bg.anchor = Point(0, 0)
            bg.smoothed = False
            bg.width = self.game.width
            bg.height = self.game.height
            ground = self.game.add.image(0, FLOOR_Y, 'ground')
            ground.width = self.game.width
            ground.height = self.game.height - FLOOR_Y
            ground.anchor = Point(0, 0)
            logo = self.game.add.image(self.game.width / 2, self.game.height / 2,
                                       'logo')

            padding = 24
            if GCW_ZERO:
                gcw_zero = self.game.add.image(padding,
                                               self.game.height - padding,
                                               'gcw-zero')
                gcw_zero.anchor = Point(0, 1)
            else:
                kb = self.game.add.image(padding, self.game.height - padding,
                                         'keyboard')
                kb.anchor = Point(0, 1)
            joy = self.game.add.image(self.game.width - padding,
                                      self.game.height - padding,
                                      'xbox360')
            joy.anchor = Point(1, 1)

            self.gong = self.game.add.sprite(self.game.width / 2,
                                             FLOOR_Y,
                                             'gong',
                                             Point(2, 2))
            self.gong.anchor.y = 1
            self.gong.body.y = -46

            self.hurt_boxes = self.game.add.group()
            self.players = self.game.add.group()
            offset = self.game.width * 0.06
            self.add_player(self.game.width / 2 - offset, 'cat')
            self.game.players_joined = [False, False]
        self.create = create

        def update(time):
            self.grace_timer -= ANIM_FRAME_RATE / FRAME_RATE
            if self.grace_timer <= 0:
                self.game.keys.update()
                if self.game.keys.is_escape():
                    self.is_quit = True
                self.game.joys.update()

            # Detect second player
            if (len(self.players) == 1 and
                    self.game.joys.joystick is not None):
                offset = self.game.width * 0.06
                self.add_player(self.game.width / 2 + offset, 'dog')

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

            # Hit gong
            def gong_hit(g, h):
                assets.sounds['gong'].play()
                self.state.start('game')
            physics.overlap(self.gong, self.hurt_boxes, gong_hit)
        self.update = update

        def draw(surface):
            font = assets.fonts['big']
            text = "Slappa!"
            size = font.size(text)
            surface.blit(font.render(text,
                                     True,
                                     (255, 140, 160)),
                         ((self.game.width - size[0]) / 2,
                          (self.game.height - size[1]) / 2))
        self.draw = draw

    def add_player(self, x, key):
        player = self.players.add(Player(self.game,
                                         x, FLOOR_Y,
                                         key,
                                         self.hurt_boxes))
        player.health = 0
        player.is_dying = True
        player.animations.play('die')


class HighScoreHelper(object):
    def __init__(self, state):
        self.high_scores = None
        self.top_scores = []
        self.score_index = -1
        self.state = state
        self.is_entering = False
        self.last_key = None
        state.game.keys.on_down = self.enter_key

    def __exit__(self, type, value, traceback):
        self.game.keys.on_down = None

    def enter_key(self, key, unicode):
        if self.score_index >= 0 and self.is_entering:
            score = self.top_scores[self.score_index]
            if pygame.K_a <= key <= pygame.K_z:
                score[1] += unicode
            elif key == pygame.K_BACKSPACE and len(score[1]) > 0:
                score[1] = score[1][:-1]
            elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
                self.is_entering = False
                self.high_scores.add(score[0], score[1])

    def update(self):
        # Check for game end and high score
        if (all(player.health <= 0 for player in self.state.players) and
                self.high_scores is None):
            self.high_scores = HighScore()
            # Check to see if our score is good enough
            i = 0
            for score in self.high_scores.get_scores():
                if score[0] <= self.state.score and self.score_index == -1:
                    self.score_index = i
                    self.top_scores.append([self.state.score,
                                            '',
                                            self.high_scores.get_date()])
                i += 1
                self.top_scores.append(score)
                if i == 10:
                    break
            if i != 10 and self.score_index < 0:
                self.score_index = i
                self.top_scores.append([self.state.score,
                                        '',
                                        self.high_scores.get_date()])
            if self.score_index >= 0:
                self.is_entering = True

    def draw(self, surface):
        font = assets.fonts['font']
        # Headings
        line_height = 36
        y = 24
        name_x = 25
        score_x = int(self.state.game.width * 0.4)
        date_x = int(self.state.game.width * 0.7)
        surface.blit(font.render("Name", True, (255, 255, 0)),
                     (name_x, y))
        surface.blit(font.render("Score", True, (255, 255, 0)),
                     (score_x, y))
        surface.blit(font.render("Date", True, (255, 255, 0)),
                     (date_x, y))
        y += line_height
        i = 0
        for score in self.top_scores:
            # Name
            name = score[1][:]
            color = (255, 255, 255)
            if self.is_entering and i == self.score_index:
                name += '_'
            if i == self.score_index:
                color = (0, 255, 0)
            surface.blit(font.render(name, True, color), (name_x, y))
            # Score
            surface.blit(font.render(str(score[0]), True, color), (score_x, y))
            # Date
            surface.blit(font.render(score[2], True, color), (date_x, y))
            i += 1
            y += line_height

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
        self.high_score_helper = None
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
            self.high_score_helper = HighScoreHelper(self)

            bg = self.game.add.image(0, 0, 'background')
            bg.anchor = Point(0, 0)
            bg.smoothed = False
            bg.width = self.game.width
            bg.height = self.game.height

            ground = self.game.add.image(0, FLOOR_Y, 'ground')
            ground.width = self.game.width
            ground.height = self.game.height - FLOOR_Y
            ground.anchor = Point(0, 0)

            self.bubbles = self.game.add.group()
            self.enemies = self.game.add.group()
            self.thing_group = self.game.add.group()
            self.hurt_boxes = self.game.add.group()
            self.players = self.game.add.group()
            self.enemy_generator = EnemyGenerator(
                self.game, self.enemies, self.players, self.thing_group)

            offset = self.game.width * 0.06
            self.add_player(self.game.width / 2 - offset, 'cat', 0)
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

            # Detect second player
            if (len(self.players) == 1 and
                    self.game.joys.joystick is not None):
                offset = self.game.width * 0.06
                self.add_player(self.game.width / 2 + offset, 'dog', 1)

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

            # remove dead enemies
            self.enemy_generator.update(time)

            # Collisions
            def hit(x, y):
                random.choice(assets.sounds['hits']).play()
                self.bubbles.add(Bubble(self.game, x, y))

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

            self.high_score_helper.update()
        self.update = update

        def draw(surface):
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
            if players_alive == 0:
                self.high_score_helper.draw(surface)
            else:
                surface.blit(font.render("Score: " + str(self.score),
                                         True,
                                         (255, 255, 0)),
                             (self.game.width / 2 - 100, 50))
        self.draw = draw

    def add_player(self, x, key, index):
        player = self.players.add(Player(self.game,
                                         x, FLOOR_Y,
                                         key,
                                         self.hurt_boxes))
        if not self.game.players_joined[index]:
            player.health = 0
            player.is_dying = True
            player.animations.play('die')


def main():
    game = SlappaGame()
    game.state.add('game', GameState())
    game.state.add('title', TitleState())
    game.state.start('title')


if __name__ == '__main__':
    main()