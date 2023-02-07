import pygame
import os
import random


pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Shoot me!")

WIDTH, HEIGHT = 1400, 800
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40
AMMUNITIONS_WIDTH, AMMUNITIONS_HEIGHT = 40, 40
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
ORANGE = (255,140,0)
GREEN = (124,252,0)
PURPLE = (233, 139, 255)

FPS = 60

SPEED = 5
BULLET_SPEED = 20
BULLET_WIDTH = 10
BULLET_HEIGHT = 6
MAX_BULLETS_RED = 5
MAX_BULLETS_YELLOW = 5
MAX_WALL_HEIGHT = 200
MIN_WALL_HEIGHT = 75
WALL_WIDTH = 20
COLLISION_TOLERANCE = 20

#sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Config", "hit.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Config", "gun.mp3"))
WIN_SOUND = pygame.mixer.Sound(os.path.join("Config", "win.mp3"))
GET_AMMO_SOUND = pygame.mixer.Sound(os.path.join("Config", "get_ammo.wav"))
GET_AMMO_SOUND.set_volume(2)

#BACKGROUND SOUND
pygame.mixer.music.load(os.path.join("Config", "background.mp3"))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

#create event for collision 
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

#images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Config",'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270) 
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Config",'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Config", 'space.png')), (WIDTH, HEIGHT))
BULLET_IMAGE = pygame.image.load(os.path.join("Config", "bullet.png"))
BULLET_SCALE = pygame.transform.scale(BULLET_IMAGE, (AMMUNITIONS_WIDTH, AMMUNITIONS_HEIGHT))

#fonts
HEALTH_FONT = pygame.font.SysFont('arial', 30)
WINNER_FONT = pygame.font.SysFont('valorax', 200)
INIT_FONT = pygame.font.SysFont('space mission', 50)
SHOOT_ME_FONT = pygame.font.SysFont('robus', 200)

red_score = 0
yellow_score = 0
