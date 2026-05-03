from bullets import Bullet, HomingBullet

import pygame
import math
import settings as s



class Weapon:
    name = "base"

    def shoot(self, player, bullets, enemies):
        pass


class NormalWeapon(Weapon):
    name = "normal"

    def shoot(self, player, bullets, enemies):
        bullets.append(Bullet(player.x, player.y, 0))


class SpreadWeapon(Weapon):
    name = "spread"

    def shoot(self, player, bullets, enemies):
        bullets += [
            Bullet(player.x, player.y, -3),
            Bullet(player.x, player.y, 0),
            Bullet(player.x, player.y, 3)
        ]


class RapidWeapon(Weapon):
    name = "rapid"

    def shoot(self, player, bullets, enemies):
        bullets.append(Bullet(player.x, player.y, 0))
        player.cd = 3

class HomingWeapon(Weapon):
    name = "homing"

    def shoot(self, player, bullets, enemies):
        target = min(enemies, key=lambda e: abs(e.x - player.x)) if enemies else None
        bullets.append(HomingBullet(player.x, player.y, target))

        
class LaserWeapon(Weapon):
    name = "laser"

    def shoot(self, player, bullets, enemies):
        player.laser_timer = 2


class ShotgunWeapon(Weapon):
    name = "shotgun"

    def shoot(self, player, bullets, enemies):
        for i in range(-3, 4):
            bullets.append(Bullet(player.x, player.y, i))