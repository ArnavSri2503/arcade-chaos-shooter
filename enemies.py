import pygame, math
import settings as s
import effects as fx   # ✅ for shake
from bullets import EnemyBullet   # ✅ specific import


# ================= ENEMY =================
class Enemy:
    def __init__(self,x,y,etype):
        self.x=x
        self.y=y
        self.type=etype
        self.hp=2
        self.t=0
        self.flash=0

    def update(self,player,enemy_bullets, stage_speed = 1.0):
        self.t+=1

        if self.type=='sniper':
            self.y+=2 * stage_speed
            if self.t%70==0:
                dx=player.x-self.x
                dy=player.y-self.y
                d=math.hypot(dx,dy) or 1
                enemy_bullets.append(
                    EnemyBullet(self.x,self.y,dx/d*4,dy/d*4)
                )

        elif self.type=='charger':
            dx=player.x-self.x
            dy=player.y-self.y
            d=math.hypot(dx,dy) or 1
            self.x+=dx/d*2 * stage_speed
            self.y+=dy/d*2 * stage_speed

        elif self.type=='orbit':
            self.y+=2 * stage_speed
            self.x+=math.cos(self.t/7)*4 * stage_speed

        elif self.type=='zigzag':
            self.y+=2 * stage_speed
            self.x+=math.sin(self.t/8)*4 * stage_speed

        elif self.type=='splitter':
            self.y+=3 * stage_speed

        self.flash = max(0, self.flash-1)

    def rect(self):
        return pygame.Rect(self.x-15,self.y-15,30,30)

    def draw(self,screen, off):   # ✅ pass screen
        color = s.YELLOW if self.flash else s.RED
        pygame.draw.rect(screen, color,
            (self.x-15+off[0], self.y-15+off[1], 30, 30))

    def offscreen(self):
        return self.y > s.HEIGHT + 40


# ================= BOSS =================
class Boss:
    def __init__(self,level):
        self.x = s.WIDTH//2
        self.y = -100
        self.hp = 100 + level*40
        self.max_hp = self.hp
        self.t = 0

    def update(self, enemy_bullets, player=None, stage_speed = 1.0):
        self.t += 1

        if self.y < 100:
            self.y += 2 * stage_speed

        self.x = s.WIDTH // 2 + math.sin(self.t / 45) * 120 * stage_speed

        fx.add_shake(1)

        # Phase 1: radial burst + aimed shots
        if self.hp > self.max_hp * 0.66:
            if self.t % 50 == 0:
                for a in range(0, 360, 30):
                    enemy_bullets.append(
                        EnemyBullet(
                            self.x,
                            self.y,
                            math.cos(math.radians(a)) * 3.5,
                            math.sin(math.radians(a)) * 3.5,
                        )
                    )

            if player and self.t % 35 == 0:
                dx = player.x - self.x
                dy = player.y - self.y
                d = math.hypot(dx, dy) or 1
                enemy_bullets.append(
                    EnemyBullet(self.x, self.y, dx / d * 5, dy / d * 5)
                )

        # Phase 2: spiral + side curtains
        elif self.hp > self.max_hp * 0.33:
            if self.t % 8 == 0:
                a = self.t * 9
                enemy_bullets.append(
                    EnemyBullet(
                        self.x,
                        self.y,
                        math.cos(math.radians(a)) * 4.2,
                        math.sin(math.radians(a)) * 4.2,
                    )
                )
                enemy_bullets.append(
                    EnemyBullet(
                        self.x,
                        self.y,
                        math.cos(math.radians(a + 180)) * 4.2,
                        math.sin(math.radians(a + 180)) * 4.2,
                    )
                )

            if self.t % 70 == 0:
                for x in range(40, s.WIDTH, 80):
                    enemy_bullets.append(EnemyBullet(x, self.y, 0, 4))

        # Phase 3: panic pattern with shifting safe lane NOOOOO
        # Phase 3: controlled chaos (SAFE ZONE shifting)
        else:
            # 🔹 moving safe lane
            if self.t % 25 == 0:
                gap_x = int(s.WIDTH // 2 + math.sin(self.t / 30) * 140)

                for x in range(20, s.WIDTH, 35):
                    if abs(x - gap_x) < 60:   # 🔥 bigger gap (was too small)
                        continue

                    enemy_bullets.append(
                        EnemyBullet(x, self.y, 0, 4.5)  # 🔥 slower bullets
                    )

            # 🔹 aimed pressure (LESS frequent, LESS spread)
            if player and self.t % 35 == 0:
                dx = player.x - self.x
                dy = player.y - self.y
                d = math.hypot(dx, dy) or 1

                # 🔥 reduced from 3 → 2 bullets
                for spread in (-0.2, 0.2):
                    enemy_bullets.append(
                        EnemyBullet(
                            self.x,
                            self.y,
                            (dx / d) * 5 + spread,
                            (dy / d) * 5
                        )
                    )

    def rect(self):
        return pygame.Rect(self.x-50,self.y-30,100,60)

    def draw(self,screen, off):   # ✅ pass screen
        pygame.draw.rect(screen, s.PURPLE,
            (self.x-50+off[0], self.y-30+off[1], 100, 60))