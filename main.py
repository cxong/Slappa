#!/usr/bin/env python
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
        self.joys = Joysticks()

        # Player devices
        self.devices = [self.keys, self.joys[0]]
        if DEMO_MODE:
            self.devices = [self.joys[0], self.joys[1]]

        # Sounds
        # TODO: lists of sounds
        self.audio = {}


# Title screen
class TitleState(State):
    def __init__(self):
        super(TitleState, self).__init__()
        # Don't detect input for a bit
        # To prevent capturing escape from game screen
        self.grace_timer = 30

        self.hurt_boxes = None
        self.players = None
        self.gong = None

        def preload():
            self.game.load.image('background', "data/images/bg.png")
            self.game.load.image('ground', "data/images/ground.png")
            self.game.load.image('logo', "data/images/logo.png")
            self.game.load.image('gong', "data/images/gong.png")
            self.game.load.image('keyboard', "data/images/keyboard.png")
            self.game.load.image('xbox360', "data/images/xbox360.png")
            self.game.load.image('gcw-zero', "data/images/gcw-zero.png")
            self.game.load.audio('gong', "data/sounds/gong.ogg")
            self.game.load.image('cat', "data/images/players/cat.png")
            self.game.load.image('dog', "data/images/players/dog.png")
            self.game.load.font('font', "data/MedievalSharp.ttf",
                                self.game.scale.scale.x * 32)
            self.game.load.font('big', "data/MedievalSharp.ttf",
                                self.game.scale.scale.x * 72)

            self.game.audio['hits'] = load_sounds_from_folder("hits")
            self.game.load.audio('jump', "data/sounds/jump.ogg")
            self.game.load.audio('land', "data/sounds/land.ogg")
            self.game.audio['swings'] = load_sounds_from_folder("swings")
            self.game.load.audio('meow', "data/sounds/meow.ogg")
            self.game.load.audio('yelp', "data/sounds/yelp.ogg")

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
            ground = self.game.add.image(0, self.game.config.FLOOR_Y, 'ground')
            ground.width = self.game.width
            ground.height = self.game.height - self.game.config.FLOOR_Y
            ground.anchor = Point(0, 0)
            logo = self.game.add.image(self.game.width / 2,
                                       self.game.height / 2,
                                       'logo')
            self.game.add.text(self.game.width / 2, self.game.height / 2,
                               'Slappa!',
                               {'font': self.game.load.fonts['big'],
                                'fill': (255, 140, 160)})

            padding = 24
            if GCW_ZERO:
                gcw_zero = self.game.add.image(padding,
                                               self.game.height - padding,
                                               'gcw-zero')
                gcw_zero.anchor = Point(0, 1)
            elif DEMO_MODE:
                joy1 = self.game.add.image(padding, self.game.height - padding,
                                           'xbox360')
                joy1.anchor = Point(0, 1)
            else:
                kb = self.game.add.image(padding, self.game.height - padding,
                                         'keyboard')
                kb.anchor = Point(0, 1)
            if self.game.devices[1] is not None:
                joy = self.game.add.image(self.game.width - padding,
                                          self.game.height - padding,
                                          'xbox360')
                joy.anchor = Point(1, 1)

            self.gong = self.game.add.sprite(self.game.width / 2,
                                             self.game.config.FLOOR_Y,
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
            self.grace_timer -= self.game.config.ANIM_FRAME_RATE / self.game.config.FRAME_RATE
            if self.grace_timer <= 0:
                self.game.keys.update()
                if self.game.keys.is_escape():
                    self.is_quit = True
                self.game.joys.update()

            # Detect second player
            if len(self.players) == 1 and self.game.devices[1] is not None:
                offset = self.game.width * 0.06
                self.add_player(self.game.width / 2 + offset, 'dog')

            # Detect input and add player
            if self.game.devices[0].pressed():
                self.players[0].health = 5
                self.game.players_joined[0] = True
            if self.game.devices[1] is not None and self.game.devices[1].pressed():
                self.players[1].health = 5
                self.game.players_joined[1] = True

            for i in range(len(self.players)):
                player = self.players[i]
                player.hit(self.game.devices[i].hit())
                player.move(self.game.devices[i].dir())
                if self.game.devices[i].is_jump():
                    player.jump()

            # Hit gong
            def gong_hit(g, h):
                self.game.add.audio('gong').play()
                self.state.start('game')
            physics.overlap(self.gong, self.hurt_boxes, gong_hit)
        self.update = update

    def add_player(self, x, key):
        player = self.players.add(Player(self.game,
                                         x, self.game.config.FLOOR_Y,
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
        self.headings = Group()
        # Headings
        y = 24
        name_x = 25
        score_x = int(self.state.game.width * 0.4)
        date_x = int(self.state.game.width * 0.7)
        style = {'font': state.game.load.fonts['font'], 'fill': (255, 255, 0)}
        text = Text(state.game, name_x, y, 'Name', style)
        text.anchor = Point(0, 0)
        self.headings.add(text)
        text = Text(state.game, score_x, y, 'Score', style)
        text.anchor = Point(0, 0)
        self.headings.add(text)
        text = Text(state.game, date_x, y, 'Date', style)
        text.anchor = Point(0, 0)
        self.headings.add(text)
        self.cursor_blink = 300

    def __exit__(self, type, value, traceback):
        self.state.game.keys.on_down = None

    def enter_key(self, key, unicode):
        if self.score_index >= 0 and self.is_entering:
            score = self.top_scores[self.score_index]
            if GCW_ZERO:
                # Accept up/down, backspace, or enter
                if key == pygame.K_UP:
                    self.cycle_letter(1)
                elif key == pygame.K_DOWN:
                    self.cycle_letter(-1)
                elif key == pygame.K_LALT:
                    self.backspace()
                elif key == pygame.K_LCTRL:
                    # If we're full, end
                    if len(score[1]) >= 3:
                        self.end()
                    else:
                        # Else, add a letter
                        score[1] += 'A'
                # Add the first letter
                if len(score[1]) == 0:
                    score[1] = 'A'
            else:
                if pygame.K_a <= key <= pygame.K_z:
                    score[1] += unicode
                elif key == pygame.K_BACKSPACE:
                    self.backspace()
                elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
                    self.end()

    def end(self):
        if self.score_index >= 0 and self.is_entering:
            score = self.top_scores[self.score_index]
            self.is_entering = False
            self.high_scores.add(score[0], score[1])

    def backspace(self):
        if self.score_index >= 0 and self.is_entering:
            score = self.top_scores[self.score_index]
            if len(score[1]) > 0:
                score[1] = score[1][:-1]

    def cycle_letter(self, direction):
        if self.score_index >= 0 and self.is_entering:
            score = self.top_scores[self.score_index]
            score[1] = score[1][:-1] + chr(ord(score[1][-1]) + direction)
            if score[1][-1] > 'Z':
                score[1] = score[1][:-1] + 'A'
            if score[1][-1] < 'A':
                score[1] = score[1][:-1] + 'Z'

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
                if GCW_ZERO:
                    score = self.top_scores[self.score_index]
                    # Add the first letter
                    if len(score[1]) == 0:
                        score[1] = 'A'

    def draw(self, surface):
        self.headings.draw(surface)
        font = self.state.game.load.fonts['font']
        # Headings
        line_height = 36
        y = 24
        name_x = 25
        score_x = int(self.state.game.width * 0.4)
        date_x = int(self.state.game.width * 0.7)
        y += line_height
        style_others = {'font': self.state.game.load.fonts['font'],
                        'fill': (255, 255, 255)}
        style_self = {'font': self.state.game.load.fonts['font'],
                      'fill': (0, 255, 0)}
        i = 0
        for score in self.top_scores:
            if i == 10:
                break
            # Name
            name = score[1][:]
            style = style_others
            if self.is_entering and i == self.score_index and self.cursor_blink > 0:
                name += '_'
            self.cursor_blink -= 1
            if self.cursor_blink < -300:
                self.cursor_blink = 300
            if i == self.score_index:
                style = style_self
            text = Text(self.state.game, name_x, y, name, style)
            text.anchor = Point(0, 0)
            text.draw(surface)
            # Score
            text = Text(self.state.game, score_x, y, str(score[0]), style)
            text.anchor = Point(0, 0)
            text.draw(surface)
            # Date
            text = Text(self.state.game, date_x, y, score[2], style)
            text.anchor = Point(0, 0)
            text.draw(surface)
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
        self.pause_text = None
        self.pause_sound = None

        def preload():
            # Sounds
            self.game.audio['growls'] = load_sounds_from_folder("growls")
            self.game.audio['deaths'] = load_sounds_from_folder("deaths")
            self.game.load.audio('pause', 'data/sounds/pause.ogg')

            # Images/templates
            self.game.load.image('explosion', "data/images/explosion.png")
            self.game.load.image('zombie', "data/images/enemies/zombie.png")
            self.game.load.image('monster', "data/images/enemies/monster.png")
            self.game.load.image('flying', "data/images/enemies/flying.png")
        self.preload = preload

        def create():
            pygame.mixer.music.load("data/sounds/Blackmoor Ninjas.ogg")
            self.score = 0
            self.high_score_helper = HighScoreHelper(self)

            bg = self.game.add.image(0, 0, 'background')
            bg.anchor = Point(0, 0)
            bg.smoothed = False
            bg.width = self.game.width
            bg.height = self.game.height

            ground = self.game.add.image(0, self.game.config.FLOOR_Y, 'ground')
            ground.width = self.game.width
            ground.height = self.game.height - self.game.config.FLOOR_Y
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
            # Detect second player
            if self.game.devices[1] is not None:
                offset = self.game.width * 0.06
                self.add_player(self.game.width / 2 + offset, 'dog', 1)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.7)
            self.pause_text = self.game.add.text(
                self.game.width / 2, self.game.height / 2,
                "Paused",
                {'font': self.game.load.fonts['big'], 'fill': (255, 255, 0)})
            self.pause_text.visible = False
            self.game.on_paused = self.on_pause
            self.game.on_resume = self.on_resume
            self.game.keys.on_down = self.enter_key
            self.pause_sound = self.game.add.audio('pause')
        self.create = create

        def update(time):
            # Keys
            self.game.keys.update()
            if self.game.keys.is_escape():
                self.state.start('title')
                return
            self.game.joys.update()

            # Detect input and add player
            if not self.high_score_helper.is_entering:
                if (not self.game.players_joined[0] and
                        (self.game.devices[0].hit())):
                    self.players[0].health = 5
                    self.game.players_joined[0] = True
                if (not self.game.players_joined[1] and
                        self.game.devices[1] is not None and
                        self.game.devices[1].hit()):
                    self.players[1].health = 5
                    self.game.players_joined[1] = True
            else:
                self.game.players_joined = [True, True]

            #Update
            for i in range(len(self.players)):
                player = self.players[i]
                player.hit(self.game.devices[i].hit())
                player.move(self.game.devices[i].dir())
                if self.game.devices[i].is_jump():
                    player.jump()

            # remove dead enemies
            self.enemy_generator.update(time)

            # Collisions
            def hit(x, y):
                random.choice(self.game.audio['hits']).play()
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
            font = self.game.load.fonts['font']
            padding = 25
            players_alive = 0

            for i in range(len(self.players)):
                player = self.players[i]
                text = Text(self.state.game,
                            padding, self.game.height - padding,
                            "HP: " + str(player.health),
                            {'font': font, 'fill': (0, 255, 0)})
                text.anchor = Point(0, 1)
                if i == 1:
                    text.x = self.game.width - padding
                    text.anchor.x = 1
                text.draw(surface)
                if player.health > 0:
                    players_alive += 1
            if players_alive == 0:
                self.high_score_helper.draw(surface)
            else:
                text = Text(self.state.game,
                            self.game.width / 2, 50,
                            "Score: " + str(self.score),
                            {'font': font, 'fill': (255, 255, 0)})
                text.draw(surface)
            if self.game.config.DEBUG_SHOW_FPS:
                text = Text(self.state.game,
                            self.game.width - padding, padding,
                            "FPS: %.1f" % self.game.time.fps,
                            {'font': font, 'fill': (0, 0, 0)})
                text.anchor = Point(1, 0)
                text.draw(surface)
        self.draw = draw

    def on_pause(self):
        self.pause_text.visible = True
        pygame.mixer.music.pause()
        self.pause_sound.play()

    def on_resume(self):
        self.pause_text.visible = False
        pygame.mixer.music.unpause()

    def enter_key(self, key, unicode):
        if key == pygame.K_p or (GCW_ZERO and key == pygame.K_RETURN):
            self.game.paused = not self.game.paused
        else:
            self.high_score_helper.enter_key(key, unicode)

    def add_player(self, x, key, index):
        player = self.players.add(Player(self.game,
                                         x, self.game.config.FLOOR_Y,
                                         key,
                                         self.hurt_boxes))
        if not self.game.players_joined[index]:
            player.health = 0
            player.is_dying = True
            player.animations.play('die')


def main():
    game = SlappaGame()
    if game.config.DEBUG_SHOW_FPS:
        game.time.advanced_timing = True
    game.state.add('game', GameState())
    game.state.add('title', TitleState())
    game.state.start('title')


if __name__ == '__main__':
    main()