import math
import random
import pygame

import settings as s
import effects as fx

from player import Player
from enemies import Enemy, Boss


class Game:
    def __init__(self, mode="classic", loadout=None, screen=None):
        self.mode = mode
        self.loadout = loadout or []
        self.screen = screen
        self.reset()

    def reset(self):
        self.player = Player()
        self.player.hp = 1 if self.mode == "hardcore" else 5

        if self.loadout:
            self.player.inventory = self.loadout.copy()
            self.player.current_weapon_index = 0

        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.particles = []

        self.boss = None

        self.score = 0
        self.level = 1
        self.timer = 0

        self.phase = "wave"
        self.phase_timer = 0

        self.chaos_wave = 0
        self.chaos_timer = 0

        self.state = "playing"

        self.slowmo = 1
        fx.warning_timer = 0
        fx.transition_alpha = 0

    def explode(self, x, y, color=s.RED, count=30):
        fx.add_shake(10)
        for _ in range(count):
            self.particles.append(fx.Particle(x, y, color))

    def spawn_enemy(self, count=1):
        types = ["sniper", "charger", "orbit", "zigzag", "splitter"]
        for _ in range(count):
            self.enemies.append(
                Enemy(random.randint(40, 460), -40, random.choice(types))
            )

    def update(self):
        if self.state != "playing":
            return

        fx.update_transition()
        fx.update_shake()

        self.timer += 1
        self.phase_timer += 1

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        stage_speed = 0.45 if keys[pygame.K_LSHIFT] else 1.0

        targets = self.enemies + ([self.boss] if self.boss else [])
        self.player.shoot(self.bullets, targets)

        # ================= CLASSIC =================
        if self.mode == "classic":
            if self.phase == "wave":
                if self.timer % 70 == 0:
                    self.spawn_enemy(1)

                if self.score >= self.level * 300:
                    self.phase = "boss"
                    fx.warning_timer = 180
                    fx.transition_alpha = 255

            elif self.phase == "boss":
                if fx.warning_timer > 0:
                    fx.warning_timer -= 1
                    if fx.warning_timer == 120:
                        self.boss = Boss(self.level)
                    return

                if self.boss:
                    self.boss.update(self.enemy_bullets, self.player, stage_speed)
                    if self.boss.hp <= 0:
                        self.slowmo = 20
                        fx.transition_alpha = 180
                        self.explode(self.boss.x, self.boss.y, s.PURPLE, 70)
                        self.boss = None
                        self.phase = "chaos"
                        self.phase_timer = 0

            elif self.phase == "chaos":
                if self.timer % 10 == 0:
                    self.spawn_enemy(4)

                if self.phase_timer > 600:
                    self.phase = "wave"
                    self.phase_timer = 0
                    self.level += 1

        # ================= ENDLESS =================
        elif self.mode == "endless":
            spawn_rate = max(15, 70 - self.level * 5)

            if self.timer % spawn_rate == 0:
                self.spawn_enemy(1 + self.level // 2)

            if self.timer % 600 == 0:
                self.level += 1

        # ================= BOSSRUSH =================
        elif self.mode == "bossrush":
            if not self.boss and fx.warning_timer == 0:
                fx.warning_timer = 120
                fx.transition_alpha = 255

            if fx.warning_timer > 0:
                fx.warning_timer -= 1
                if fx.warning_timer == 1:
                    self.boss = Boss(self.level)
                return

            if self.boss:
                self.boss.update(self.enemy_bullets,self.player, stage_speed)
                if self.boss.hp <= 0:
                    self.slowmo = 20
                    fx.transition_alpha = 180
                    self.explode(self.boss.x, self.boss.y, s.PURPLE, 70)
                    self.score += 500 + self.level * 100
                    self.level += 1
                    self.boss = None

        # ================= CHAOS =================
        elif self.mode == "chaos":
            self.chaos_timer += 1

            if self.chaos_timer > 240:
                self.chaos_timer = 0
                self.chaos_wave = (self.chaos_wave + 1) % 3

            difficulty = min(3, self.level)
            max_enemies = 15 + difficulty * 5
            spawn_delay = 40 - difficulty * 5
            spawn_count = 3 + difficulty

            if self.chaos_wave == 0:
                if len(self.enemies) < max_enemies and self.timer % 60 == 0:
                    gap_x = random.randint(100, s.WIDTH - 100)
                    total = 8 + difficulty * 2

                    for i in range(total):
                        x = int(i * s.WIDTH / total)
                        if abs(x - gap_x) < 80:
                            continue
                        self.enemies.append(
                            Enemy(x, -40, random.choice(["sniper", "zigzag"]))
                        )

            elif self.chaos_wave == 1:
                if len(self.enemies) < max_enemies and self.timer % 50 == 0:
                    gap_x = int((s.WIDTH / 2) + math.sin(self.timer / 60) * 150)

                    for x in range(40, s.WIDTH, 40):
                        if abs(x - gap_x) < 60:
                            continue
                        self.enemies.append(Enemy(x, -40, "charger"))

            elif self.chaos_wave == 2:
                if len(self.enemies) < max_enemies and self.timer % spawn_delay == 0:
                    for _ in range(spawn_count):
                        x = random.randint(50, s.WIDTH - 50)
                        self.enemies.append(Enemy(x, -40, "zigzag"))

        # ================= HARDCORE =================
        elif self.mode == "hardcore":
            if self.timer % 40 == 0:
                self.spawn_enemy(2)

            if self.score > 400 and not self.boss and fx.warning_timer == 0:
                fx.warning_timer = 120
                fx.transition_alpha = 255

            if fx.warning_timer > 0:
                fx.warning_timer -= 1
                if fx.warning_timer == 1:
                    self.boss = Boss(self.level)
                return

            if self.boss:
                self.boss.update(self.enemy_bullets, self.player, stage_speed)
                if self.boss.hp <= 0:
                    self.slowmo = 20
                    fx.transition_alpha = 180
                    self.explode(self.boss.x, self.boss.y, s.PURPLE, 70)
                    self.score += 1000
                    self.boss = None

        for e in self.enemies:
            e.update(self.player, self.enemy_bullets, stage_speed)

        for b in self.bullets:
            b.update(stage_speed)

        for eb in self.enemy_bullets:
            eb.update(stage_speed)

        for p in self.particles:
            p.update(stage_speed)

        self.handle_collisions()

        self.bullets = [b for b in self.bullets if not b.offscreen()]
        self.enemy_bullets = [b for b in self.enemy_bullets if not b.offscreen()]
        self.enemies = [e for e in self.enemies if not e.offscreen()]
        self.particles = [p for p in self.particles if p.life > 0]

        if self.slowmo > 1:
            self.slowmo -= 1

        if self.player.hp <= 0:
            self.state = "game_over"

    def handle_collisions(self):

        # 🔹 bullet vs enemy
        for b in self.bullets[:]:
            for e in self.enemies[:]:
                if e.rect().collidepoint(b.x, b.y):
                    e.hp -= 1
                    e.flash = 5

                    if b in self.bullets:
                        self.bullets.remove(b)

                    fx.add_shake(4)

                    if e.hp <= 0:
                        self.explode(e.x, e.y)
                        self.enemies.remove(e)
                        self.score += 50
                    break
        
        # ================= LASER DAMAGE =================
        weapon = self.player.get_weapon()

        if weapon and weapon.name == "laser" and self.player.laser_timer > 0:
            laser_width = 24

            for e in self.enemies[:]:
                if abs(e.x - self.player.x) < laser_width:
                    e.hp -= 0.35
                    e.flash = 5

                    if e.hp <= 0:
                        self.explode(e.x, e.y, s.GREEN, 25)
                        self.enemies.remove(e)
                        self.score += 50

            if self.boss and abs(self.boss.x - self.player.x) < 60:
                self.boss.hp -= 0.45

        
        # 🔹 enemy bullets vs player
        for eb in self.enemy_bullets[:]:
            if self.player.rect().collidepoint(eb.x, eb.y) and self.player.inv == 0:
                self.player.hp -= 1
                self.player.inv = 60
                fx.add_shake(12)
                self.enemy_bullets.remove(eb)
        
        
        # 🔹 boss collisions
        if self.boss:
            for b in self.bullets[:]:
                if self.boss.rect().collidepoint(b.x, b.y):
                    self.boss.hp -= 1
                    if b in self.bullets:
                        self.bullets.remove(b)

    def draw(self):
        off = fx.get_offset()
        self.screen.fill(s.BLACK)

        for star in fx.stars:
            star[1] += star[2]
            if star[1] > s.HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, s.WIDTH)
            pygame.draw.circle(self.screen, s.GRAY, (star[0], star[1]), star[2])

        for p in self.particles:
            p.draw(self.screen, off)

        for b in self.bullets:
            b.draw(self.screen, off)

        for eb in self.enemy_bullets:
            eb.draw(self.screen, off)

        for e in self.enemies:
            e.draw(self.screen, off)

        if self.boss:
            self.boss.draw(self.screen, off)

        self.player.draw(self.screen, off)

        self.screen.blit(s.FONT.render(f"Score: {self.score}", True, s.WHITE), (10, 10))
        self.screen.blit(s.FONT.render(f"HP: {self.player.hp}", True, s.WHITE), (10, 35))
        self.screen.blit(s.FONT.render(f"Mode: {self.mode.upper()}", True, s.WHITE), (10, 60))

        if hasattr(self.player, "get_weapon"):
            weapon = self.player.get_weapon()
            if weapon:
                self.screen.blit(
                    s.FONT.render(f"Weapon: {weapon.name}", True, s.WHITE),
                    (10, 85),
                )
            

            for i, w in enumerate(self.player.inventory):
                color = s.CYAN if i == self.player.current_weapon_index else s.GRAY
                txt = s.SMALL.render(w.name, True, color)
                self.screen.blit(txt, (10, 110 + i * 20))

        if self.boss:
            pygame.draw.rect(self.screen, s.WHITE, (100, 10, 300, 15), 2)
            pygame.draw.rect(
                self.screen,
                s.PURPLE,
                (100, 10, 300 * (self.boss.hp / self.boss.max_hp), 15),
            )

        if self.mode == "chaos":
            wave_names = ["RING", "SHIFTING WALL", "ZIGZAG"]
            txt = s.SMALL.render(f"CHAOS: {wave_names[self.chaos_wave]}", True, s.CYAN)
            self.screen.blit(txt, (10, 220))

        if fx.warning_timer > 0:
            txt = s.BIG.render("WARNING: BOSS INCOMING", True, s.RED)
            self.screen.blit(txt, (s.WIDTH // 2 - txt.get_width() // 2, s.HEIGHT // 2))

        if self.state == "game_over":
            self.screen.blit(s.BIG.render("GAME OVER", True, s.RED), (140, 300))

        if fx.transition_alpha > 0:
            fade = pygame.Surface((s.WIDTH, s.HEIGHT))
            fade.set_alpha(fx.transition_alpha)
            fade.fill((0, 0, 0))
            self.screen.blit(fade, (0, 0))