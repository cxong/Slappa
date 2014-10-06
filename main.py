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
#from player import *
#from thing import *
#from vec import *

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.display.set_caption("Slappa!")
clock = pygame.time.Clock()

# Input devices
keys = Keyboard()

# Sounds
soundHits = []
for dirname, dirnames, filenames in os.walk("sounds/hits"):
    for filename in filenames:
        soundHits.append(pygame.mixer.Sound(os.path.join(dirname, filename)))
soundSwings = []
for dirname, dirnames, filenames in os.walk("sounds/swings"):
    for filename in filenames:
        soundSwings.append(pygame.mixer.Sound(os.path.join(dirname, filename)))
soundPain = pygame.mixer.Sound("pain.wav")
soundJump = pygame.mixer.Sound("sounds/jump.wav")
soundGrunt = pygame.mixer.Sound("sounds/grunt.wav")
soundDie = pygame.mixer.Sound("sounds/die.wav")

# Images
imageBackground = pygame.image.load("images/background.jpg")
imageSlappers = [
    (pygame.image.load("slapper0.gif"), 0, 0, 0),
    (pygame.image.load("slapper1.gif"), 0, 0, 0)]
imageSlapperJumps = [
    (pygame.image.load("slapper_j.gif"), 0, 0, 0)]
imageSlapperHits = [
    (pygame.image.load("slapper_h0.gif"), -20, 0, 0),
    (pygame.image.load("slapper_h1.gif"), -20, 0, 0),
    (pygame.image.load("slapper_h1.gif"), -20, 0, 0)]
imageSlapperHitUps = [
    (pygame.image.load("slapper_hu0.gif"), 0, 0, 23),
    (pygame.image.load("slapper_hu1.gif"), -10, -10, -23),
    (pygame.image.load("slapper_hu1.gif"), -10, -10, -23)]
imageSlapperHitDowns = [
    (pygame.image.load("slapper_hd0.gif"), -30, 0, 13),
    (pygame.image.load("slapper_hd1.gif"), -10, -10, 10),
    (pygame.image.load("slapper_hd1.gif"), -10, -10, 10)]
things = []
for dirname, dirnames, filenames in os.walk("images/things"):
    for filename in filenames:
        things.append(pygame.image.load(os.path.join(dirname, filename)))
imageSamurai = pygame.image.load("images/enemies/samurai.gif")

# Other
font = pygame.font.SysFont("Comic Sans", 32)

# Game state
FRAME_TIME = 17
screen = pygame.display.set_mode(SCREEN_SIZE)
screenBuf = pygame.Surface(SCREEN_SIZE)
player = Player(playerAssets)
gravityEngine = GravityEngine()
gravityEngine.items.append(player)
enemies = []
samurai = Enemy(1500, player, enemySamuraiAssets,
    Thing(thingImagesAndSounds[3][0], thingImagesAndSounds[3][1]),
    thingGenerator)
def addEnemy(x, y):
    s = copy.copy(samurai)
    s.x = x
    s.y = y
    enemies.append(s)

# Game loop
clock.tick()
while True:
    isQuit = False
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isQuit = True

    # Keys
    keys.update()
    if keys.isescape():
        isQuit = True

    #Update
    player.hit(keys.hit())
    player.move(keys.dir())
    if keys.isjump():
        player.jump()
    player.update(clock.get_time())

    # remove dead enemies
    enemies = [enemy for enemy in enemies if enemy.health > 0]
    # add enemies
    if len(enemies) < 4:
        while True:
            x = random.randrange(0, imageBackground.get_width())
            if x < camera.x or x > camera.x + camera.width:
                break
        addEnemy(x, 350)
    for enemy in enemies:
        if camera.contains(enemy):
            enemy.update(clock.get_time())
    thingGenerator.update(clock.get_time())
    thingGenerator.detectCollisions(
        player.getHitArea(), player.x, player.y - 35)
    thingGenerator.detectPlayerCollisions(player.getArea(), player)
    thingGenerator.detectEnemyCollisions(enemies)

    #Render
    screenBuf.fill((255, 255, 255))
    screenBuf.blit(imageBackground, (0, 0))
    player.draw(screenBuf, camera)
    for enemy in enemies:
        enemy.draw(screenBuf, camera)
    thingGenerator.draw(screenBuf, camera)
    screenBuf.blit(font.render("HP: " + str(player.health), False, (255, 0, 0)), (50, 50))
    screenBuf.blit(font.render("Score: " + str(player.score), False, (0, 255, 0)), (500, 50))
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