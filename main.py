import pygame
import copy
import math
import os
import random
import sys
from config import *
#from enemy import *
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

# Images
imageBackground = pygame.image.load("images/bg.png")
player = Player("images/players/cat.png", (64, 64))
things = load_sprites_from_folder("things")
#imageSamurai = pygame.image.load("images/enemies/samurai.gif")

# Other
font = pygame.font.SysFont("Comic Sans", 32)

# Game state
FRAME_RATE = 60
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
    clock.tick(FRAME_RATE)

pygame.mixer.quit()
pygame.quit()