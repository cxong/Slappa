import pygame
import copy
import math
import os
import random
import sys
#from camera import *
from config import *
#from enemy import *
#from gravity_engine import *
from keyboard import *
from player import *
from sprite import *
#from vec import *

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.display.set_caption("Slappa!")
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Input devices
keys = Keyboard()


def load_from_path(path, load):
    assets = []
    for dir_name, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.endswith(".txt"):
                continue
            assets.append(load(os.path.join(dir_name, file_name)))
    return assets


# Sounds
pygame.mixer.music.load("sounds/Blackmoor Ninjas.mp3")
def load_sounds_from_folder(folder):
    def load_sound(path):
        return pygame.mixer.Sound(path)
    return load_from_path("sounds/" + folder, load_sound)
soundHits = load_sounds_from_folder("hits")
soundSwings = load_sounds_from_folder("swings")
soundPain = pygame.mixer.Sound("sounds/meow.ogg")
soundJump = pygame.mixer.Sound("sounds/jump.ogg")
soundDeaths = load_sounds_from_folder("deaths")

# Images
imageBackground = pygame.image.load("images/bg.png")
player = Player("images/players/cat.png", (64, 64))
def load_sprites_from_folder(folder):
    def load_sprite(path):
        return Sprite(pygame.image.load(path))
    return load_from_path("images/" + folder, load_sprite)
things = load_sprites_from_folder("things")
#imageSamurai = pygame.image.load("images/enemies/samurai.gif")

# Other
font = pygame.font.SysFont("Comic Sans", 32)

# Game state
FRAME_TIME = 17
screenBuf = pygame.Surface(SCREEN_SIZE)
score = 0
enemies = []
'''
def addEnemy(x, y):
    s = copy.copy(samurai)
    s.x = x
    s.y = y
    enemies.append(s)
'''

# Game loop
clock.tick()
pygame.mixer.music.play()
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
    enemies = [enemy for enemy in enemies if enemy.health > 0]
    # TODO: add enemies
    for enemy in enemies:
        enemy.update(clock.get_time())

    #Render
    screenBuf.fill((255, 255, 255))
    screenBuf.blit(imageBackground, (0, 0))
    player.draw(screenBuf)
    for enemy in enemies:
        enemy.draw(screenBuf)
    screenBuf.blit(font.render("HP: " + str(player.health), False, (255, 0, 0)), (50, 50))
    screenBuf.blit(font.render("Score: " + str(score), False, (0, 255, 0)), (500, 50))
    screenBuf.blit(font.render("WAD: punch", False, (0, 0, 0)), (50, SCREEN_SIZE[1] - 50))
    screenBuf.blit(font.render("Arrows: move", False, (0, 0, 0)), (SCREEN_SIZE[0] - 200, SCREEN_SIZE[1] - 50))
    if player.health <= 0:
        screenBuf.blit(font.render("YOU LOSE", False, (0, 0, 0)), (200, 200))
    screen.blit(screenBuf, (0, 0))

    #Loop
    pygame.display.flip()
    clock.tick_busy_loop(FRAME_TIME)

pygame.mixer.quit()
pygame.quit()