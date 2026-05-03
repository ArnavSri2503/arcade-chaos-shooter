import pygame, math
import settings as s   # ✅ SAFE import


# ================= BULLETS =================
class Bullet:
    def __init__(self,x,y,dx):
        self.x=x
        self.y=y
        self.dx=dx

    def update(self, stage_speed):
        self.x+=self.dx * stage_speed
        self.y-=10 * stage_speed

    def draw(self,screen, off):   # ✅ pass screen in
        pygame.draw.circle(screen, s.CYAN,(int(self.x+off[0]),int(self.y+off[1])),4)
        pygame.draw.circle(screen, s.WHITE,(int(self.x+off[0]),int(self.y+off[1])),2)
        pygame.draw.line(screen, s.CYAN,
            (int(self.x+off[0]),int(self.y+off[1])+6),
            (int(self.x+off[0]),int(self.y+off[1])+12),2)

    def offscreen(self):
        return self.y<-20


class HomingBullet:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target

        self.vx = 0
        self.vy = -6
        self.speed = 7
        self.turn_rate = 0.18
        self.life = 120

    def update(self, stage_speed = 1.0):
        self.life -= 1

        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)

            if dist > 0:
                desired_vx = (dx / dist) * self.speed
                desired_vy = (dy / dist) * self.speed

                self.vx += (desired_vx - self.vx) * self.turn_rate
                self.vy += (desired_vy - self.vy) * self.turn_rate

        self.x += self.vx * stage_speed
        self.y += self.vy * stage_speed

    def draw(self, screen, off):
        px = int(self.x + off[0])
        py = int(self.y + off[1])

        pygame.draw.circle(screen, s.PURPLE, (px, py), 5)
        pygame.draw.circle(screen, s.WHITE, (px, py), 2)

    def offscreen(self):
        return (
            self.y < -30
            or self.y > s.HEIGHT + 30
            or self.x < -30
            or self.x > s.WIDTH + 30
            or self.life <= 0
        )

class EnemyBullet:
    def __init__(self,x,y,dx,dy):
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy

    def update(self, stage_speed = 1.0):
        self.x+=self.dx * stage_speed
        self.y+=self.dy * stage_speed   

    def draw(self,screen, off):   # ✅ pass screen
        pygame.draw.circle(screen, s.ORANGE,
            (int(self.x+off[0]),int(self.y+off[1])),4)

    def offscreen(self):
        return self.y > s.HEIGHT+20 or self.y < -20