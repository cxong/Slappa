import physics
from bubble import *
from enemy_generator import *
from group import *
from keyboard import *
from player import *
from sprite import *
from state import *

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.display.set_caption("Slappa!")
screen = pygame.display.set_mode(SCREEN_SIZE)

# Input devices
keys = Keyboard()


# Game state
score = 0
bubbles = Group()
enemies = Group()
thing_group = Group()
hurt_boxes = Group()
players = Group()
enemy_generator = EnemyGenerator(enemies, players, thing_group)
imageBackground = pygame.image.load("images/bg.png")
font = pygame.font.Font("MedievalSharp.ttf", 32)
state = State()


def preload():
    # Sounds
    pygame.mixer.music.load("sounds/Blackmoor Ninjas.mp3")
    assets.sounds['hits'] = load_sounds_from_folder("hits")
    assets.sounds['jump'] = pygame.mixer.Sound("sounds/jump.ogg")
    assets.sounds['land'] = pygame.mixer.Sound("sounds/land.ogg")
    assets.sounds['swings'] = load_sounds_from_folder("swings")
    assets.sounds['meow'] = pygame.mixer.Sound("sounds/meow.ogg")
    assets.sounds['yelp'] = pygame.mixer.Sound("sounds/yelp.ogg")
    assets.sounds['growls'] = load_sounds_from_folder("growls")
    assets.sounds['deaths'] = load_sounds_from_folder("deaths")

    # Images/templates
    assets.images['explosion'] = pygame.image.load("images/explosion.png")
    assets.images['cat'] = pygame.image.load("images/players/cat.png")
    assets.images['dog'] = pygame.image.load("images/players/dog.png")
    assets.images['zombie'] = pygame.image.load("images/enemies/zombie.png")
    assets.images['monster'] = pygame.image.load("images/enemies/monster.png")
    assets.images['flying'] = pygame.image.load("images/enemies/flying.png")
state.preload = preload


def create():
    players.add(Player(SCREEN_SIZE[0] / 2, FLOOR_Y, 'dog', hurt_boxes))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.7)
state.create = create


def update(state, time):
    # Keys
    keys.update()
    if keys.is_escape():
        state.is_quit = True

    #Update
    for player in players:
        player.hit(keys.hit())
        player.move(keys.dir())
        if keys.is_jump():
            player.jump()
        player.update(time)

    # remove dead enemies
    enemy_generator.update(time)
    enemies.update(time)
    # remove out of bounds things
    thing_group.update(time)
    hurt_boxes.update(time)
    bubbles.update(time)

    # Collisions
    def hit(x, y):
        random.choice(assets.sounds['hits']).play()
        bubbles.add(Bubble(x, y))

    def enemy_hurt(e, h):
        if not h.has_hit_monster:
            if e.hurt():
                hit((e.x + h.x) / 2, (e.y + h.y) / 2)
                h.has_hit_monster = True
                global score
                score += 1
    physics.overlap(enemies, hurt_boxes, enemy_hurt)

    # things get hit and become players'
    def things_hit(t, h):
        if t.is_enemy:
            t.hit(h.player, enemies)
            hit((t.x + h.x) / 2, (t.y + h.y) / 2)
            global score
            score += 1
    physics.overlap(thing_group, hurt_boxes, things_hit)

    def enemy_get_hit(e, t):
        if not t.is_enemy and t.health > 0:
            if e.hurt():
                t.health = 0
                hit((e.x + t.x) / 2, (e.y + t.y) / 2)
                global score
                score += 2
    physics.overlap(enemies, thing_group, enemy_get_hit)

    def player_get_hit(p, t):
        if t.is_enemy:
            if p.hurt():
                t.health = 0
                hit((p.x + t.x) / 2, (p.y + t.y) / 2)
    physics.overlap(players, thing_group, player_get_hit)
state.update = update


def draw(surface):
    #Render
    surface.fill((255, 255, 255))
    surface.blit(imageBackground, (0, 0))
    for enemy in enemies:
        enemy.draw(surface)
    for player in players:
        player.draw(surface)
    for thing in thing_group:
        thing.draw(surface)
    for box in hurt_boxes:
        box.draw(surface)
    for bubble in bubbles:
        bubble.draw(surface)
    surface.blit(font.render("HP: " + str(player.health), True, (255, 128, 64)), (50, 50))
    surface.blit(font.render("Score: " + str(score), True, (0, 255, 0)), (500, 50))
    surface.blit(font.render("WAD: punch", True, (0, 0, 0)), (50, SCREEN_SIZE[1] - 50))
    surface.blit(font.render("Arrows: move", True, (0, 0, 0)), (SCREEN_SIZE[0] - 300, SCREEN_SIZE[1] - 50))
    if player.health <= 0:
        surface.blit(font.render("YOU LOSE", True, (255, 255, 255)), (300, 200))
    screen.blit(surface, (0, 0))
state.draw = draw

state.start()

pygame.mixer.quit()
pygame.quit()