import pygame
pygame.init()


# ================= SETUP =================
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Chaos Shooter")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 20)
BIG = pygame.font.SysFont("arial", 42)
SMALL = pygame.font.SysFont("arial", 16)

WHITE=(255,255,255)
BLACK=(15,15,20)
RED=(220,60,60)
BLUE=(60,120,255)
GREEN=(0,220,100)
PURPLE=(180,0,220)
ORANGE=(255,140,0)
YELLOW=(255,220,0)
GRAY=(80,80,100)
CYAN=(120,255,255)  

