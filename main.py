import physics
from enemy import *
from group import *
from keyboard import *
from player import *
from sprite import *

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.display.set_caption("Slappa!")
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Input devices
keys = Keyboard()


# Sounds
pygame.mixer.music.load("sounds/Blackmoor Ninjas.mp3")
assets.sounds['hits'] = load_sounds_from_folder("hits")
assets.sounds['jump'] = pygame.mixer.Sound("sounds/jump.ogg")
assets.sounds['land'] = pygame.mixer.Sound("sounds/land.ogg")
assets.sounds['swings'] = load_sounds_from_folder("swings")
assets.sounds['meow'] = pygame.mixer.Sound("sounds/meow.ogg")
assets.sounds['growls'] = load_sounds_from_folder("growls")
assets.sounds['deaths'] = load_sounds_from_folder("deaths")

# Game state
FRAME_RATE = 60
screenBuf = pygame.Surface(SCREEN_SIZE)
score = 0
enemies = Group()
thing_group = Group()
hurt_boxes = Group()

# Images/templates
imageBackground = pygame.image.load("images/bg.png")
assets.images['cat'] = pygame.image.load("images/players/cat.png")
players = Group()
players.add(Player(SCREEN_SIZE[0] / 2, FLOOR_Y, 'cat', (64, 64), hurt_boxes))
thing_keys = load_things_from_folder("things")
assets.images['monster'] = pygame.image.load("images/enemies/monster.png")

# Other
font = pygame.font.Font("MedievalSharp.ttf", 32)


def add_enemy(x, y):
    enemies.add(Enemy(x, y,
                      'monster',
                      (64, 64),
                      players,
                      thing_keys,
                      thing_group))
add_enemy(100, FLOOR_Y)
add_enemy(170, FLOOR_Y)
add_enemy(250, FLOOR_Y)

# Game loop
clock.tick()
pygame.mixer.music.play(-1)
while True:
    is_quit = False
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_quit = True

    # Keys
    keys.update()
    if keys.is_escape():
        is_quit = True

    if is_quit:
        break

    #Update
    for player in players:
        player.hit(keys.hit())
        player.move(keys.dir())
        if keys.is_jump():
            player.jump()
        player.update(clock.get_time())

    # remove dead enemies
    enemies.update(clock.get_time())
    # TODO: add enemies periodically
    # remove out of bounds things
    thing_group.update(clock.get_time())
    hurt_boxes.update(clock.get_time())

    # Collisions
    def enemy_hurt(e, h):
        if not h.has_hit_monster:
            e.hurt()
            random.choice(assets.sounds['hits']).play()
            h.has_hit_monster = True
    physics.overlap(enemies, hurt_boxes, enemy_hurt)

    # things get hit and become players'
    def things_hit(t, _):
        if t.is_enemy:
            t.hit()
            random.choice(assets.sounds['hits']).play()
    physics.overlap(thing_group, hurt_boxes, things_hit)

    def enemy_get_hit(e, t):
        if not t.is_enemy:
            e.hurt()
            t.health = 0
            random.choice(assets.sounds['hits']).play()
    physics.overlap(enemies, thing_group, enemy_get_hit)

    def player_get_hit(p, t):
        if t.is_enemy:
            p.hurt()
            t.health = 0
            random.choice(assets.sounds['hits']).play()
    physics.overlap(players, thing_group, player_get_hit)

    #Render
    screenBuf.fill((255, 255, 255))
    screenBuf.blit(imageBackground, (0, 0))
    for enemy in enemies:
        enemy.draw(screenBuf)
    for player in players:
        player.draw(screenBuf)
    for thing in thing_group:
        thing.draw(screenBuf)
    for box in hurt_boxes:
        box.draw(screenBuf)
    screenBuf.blit(font.render("HP: " + str(player.health), False, (255, 0, 0)), (50, 50))
    screenBuf.blit(font.render("Score: " + str(score), False, (0, 255, 0)), (500, 50))
    screenBuf.blit(font.render("WAD: punch", False, (0, 0, 0)), (50, SCREEN_SIZE[1] - 50))
    screenBuf.blit(font.render("Arrows: move", False, (0, 0, 0)), (SCREEN_SIZE[0] - 200, SCREEN_SIZE[1] - 50))
    if player.health <= 0:
        screenBuf.blit(font.render("YOU LOSE", False, (0, 0, 0)), (200, 200))
    screen.blit(screenBuf, (0, 0))

    #Loop
    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.mixer.quit()
pygame.quit()