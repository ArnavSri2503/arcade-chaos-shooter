import pygame
import settings as s

from bullets import Bullet, HomingBullet
from weapons import NormalWeapon, SpreadWeapon, RapidWeapon, HomingWeapon, LaserWeapon


class Player:
    def __init__(self):
        self.x = s.WIDTH // 2
        self.y = s.HEIGHT - 80
        self.hp = 5
        self.cd = 0
        self.inv = 0
        self.laser_timer = 0

        self.inventory = [NormalWeapon()]
        self.current_weapon_index = 0

    def get_weapon(self):
        if not self.inventory:
            return None
        return self.inventory[self.current_weapon_index]

    def next_weapon(self):
        if self.inventory:
            self.current_weapon_index = (self.current_weapon_index + 1) % len(self.inventory)

    def prev_weapon(self):
        if self.inventory:
            self.current_weapon_index = (self.current_weapon_index - 1) % len(self.inventory)

    def update(self, keys):
        speed = 6 if not keys[pygame.K_LSHIFT] else 2.5

        if keys[pygame.K_LEFT]:
            self.x -= speed
        if keys[pygame.K_RIGHT]:
            self.x += speed

        self.x = max(20, min(s.WIDTH - 20, self.x))

        if self.cd > 0:
            self.cd -= 1
        if self.inv > 0:
            self.inv -= 1
        if self.laser_timer > 0:
            self.laser_timer -= 1

    def shoot(self, bullets, enemies):
        weapon = self.get_weapon()
        if weapon is None:
            return

        if self.cd > 0:
            return

        weapon.shoot(self, bullets, enemies)

        if isinstance(weapon, RapidWeapon):
            if self.cd == 0:
                self.cd = 3
        elif isinstance(weapon, LaserWeapon):
            pass
        else:
            self.cd = 8

    def rect(self):
        return pygame.Rect(self.x - 15, self.y - 15, 30, 30)

    def draw(self, screen, off):
        if self.inv % 10 < 5:
            pygame.draw.polygon(screen, s.BLUE, [
                (self.x + off[0], self.y - 15 + off[1]),
                (self.x - 15 + off[0], self.y + 15 + off[1]),
                (self.x + 15 + off[0], self.y + 15 + off[1])
            ])

        if self.laser_timer > 0:
            beam_x = self.x + off[0]

            pygame.draw.line(screen, s.GREEN, (beam_x, self.y + off[1]), (beam_x, 0), 10)
            pygame.draw.line(screen, s.CYAN, (beam_x, self.y + off[1]), (beam_x, 0), 6)
            pygame.draw.line(screen, s.WHITE, (beam_x, self.y + off[1]), (beam_x, 0), 2)