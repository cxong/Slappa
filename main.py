import physics
from bubble import *
from enemy_generator import *
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
bubbles = Group()
enemies = Group()
thing_group = Group()
hurt_boxes = Group()

# Images/templates
imageBackground = pygame.image.load("images/bg.png")
assets.images['explosion'] = pygame.image.load("images/explosion.png")
assets.images['cat'] = pygame.image.load("images/players/cat.png")
players = Group()
players.add(Player(SCREEN_SIZE[0] / 2, FLOOR_Y, 'cat', (64, 64), hurt_boxes))
enemy_generator = EnemyGenerator(enemies, players, thing_group)
assets.images['zombie'] = pygame.image.load("images/enemies/zombie.png")
assets.images['monster'] = pygame.image.load("images/enemies/monster.png")
assets.images['flying'] = pygame.image.load("images/enemies/flying.png")

# Other
font = pygame.font.Font("MedievalSharp.ttf", 32)


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
    enemy_generator.update(clock.get_time())
    # remove out of bounds things
    thing_group.update(clock.get_time())
    hurt_boxes.update(clock.get_time())
    bubbles.update(clock.get_time())

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
        if not t.is_enemy:
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
    for bubble in bubbles:
        bubble.draw(screenBuf)
    screenBuf.blit(font.render("HP: " + str(player.health), True, (255, 128, 64)), (50, 50))
    screenBuf.blit(font.render("Score: " + str(score), True, (0, 255, 0)), (500, 50))
    screenBuf.blit(font.render("WAD: punch", True, (0, 0, 0)), (50, SCREEN_SIZE[1] - 50))
    screenBuf.blit(font.render("Arrows: move", True, (0, 0, 0)), (SCREEN_SIZE[0] - 300, SCREEN_SIZE[1] - 50))
    screenBuf.blit(font.render("x %f y %f" % (player.x, player.y), True, (0, 0, 0)), (SCREEN_SIZE[0] - 300, SCREEN_SIZE[1] - 100))
    if player.health <= 0:
        screenBuf.blit(font.render("YOU LOSE", True, (255, 255, 255)), (300, 200))
    screen.blit(screenBuf, (0, 0))

    #Loop
    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.mixer.quit()
pygame.quit()