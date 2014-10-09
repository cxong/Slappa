import copy
import pygame
from enemy import *
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
soundHits = load_sounds_from_folder("hits")
soundSwings = load_sounds_from_folder("swings")
soundPain = pygame.mixer.Sound("sounds/meow.ogg")
soundDeaths = load_sounds_from_folder("deaths")

# Game state
FRAME_RATE = 60
screenBuf = pygame.Surface(SCREEN_SIZE)
score = 0
enemies = []
thing_group = []

# Images/templates
imageBackground = pygame.image.load("images/bg.png")
player = Player("images/players/cat.png", (64, 64))
things = load_things_from_folder("things")
monster = Enemy("images/enemies/monster.png",
                (64, 64),
                [player],
                things,
                thing_group)

# Other
font = pygame.font.Font("MedievalSharp.ttf", 32)


def add_enemy(template, x, y):
    s = copy.copy(template)
    s.set_up(x, y)
    enemies.append(s)
add_enemy(monster, 100, FLOOR_Y)
add_enemy(monster, 170, FLOOR_Y)
add_enemy(monster, 250, FLOOR_Y)

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
    player.hit(keys.hit())
    player.move(keys.dir())
    if keys.is_jump():
        player.jump()
    player.update(clock.get_time())

    # remove dead enemies
    enemies[:] = [enemy for enemy in enemies if enemy.health > 0]
    # TODO: add enemies periodically
    for enemy in enemies:
        enemy.update(clock.get_time())
    # remove out of bounds things
    thing_group[:] = [thing for thing in thing_group if thing.health > 0]
    for thing in thing_group:
        thing.update(clock.get_time())

    #Render
    screenBuf.fill((255, 255, 255))
    screenBuf.blit(imageBackground, (0, 0))
    for enemy in enemies:
        enemy.draw(screenBuf)
    player.draw(screenBuf)
    for thing in thing_group:
        thing.draw(screenBuf)
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