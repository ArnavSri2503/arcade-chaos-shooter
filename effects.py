import pygame
import random
import settings as s


# ================= FX =================
shake = 0
slowmo = 1
warning_timer = 0
transition_alpha = 0

stars = [
    [random.randint(0, s.WIDTH), random.randint(0, s.HEIGHT), random.randint(1,3)]
    for _ in range(80)
]


def add_shake(amount):
    global shake
    shake = max(shake, amount)


def update_shake():   # ✅ CRITICAL FIX
    global shake
    if shake > 0:
        shake -= 1


def get_offset():
    if shake > 0:
        return (
            random.randint(-shake, shake),
            random.randint(-shake, shake)
        )
    return (0, 0)

def update_transition():
    global transition_alpha

    if transition_alpha > 0:
        transition_alpha -= 20   # speed of fade


# ================= PARTICLES =================
class Particle:
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.dx = random.uniform(-5,5)
        self.dy = random.uniform(-5,5)
        self.life = random.randint(20,40)
        self.size = random.randint(2,6)
        self.color = color

    def update(self, stage_speed = 1.0):
        self.x += self.dx * stage_speed
        self.y += self.dy * stage_speed
        self.life -= 1
        self.size *= 0.9

    def draw(self, screen, off):   # ✅ FIXED
        if self.life > 0 and self.size > 0:
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.x+off[0]), int(self.y+off[1])),
                int(self.size)
            )