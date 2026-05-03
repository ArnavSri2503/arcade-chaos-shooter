import pygame
pygame.init()

import settings as s
from game import Game
from ui import draw_menu, draw_loadout
from weapons import (
    NormalWeapon,
    SpreadWeapon,
    RapidWeapon,
    HomingWeapon,
    LaserWeapon,
    ShotgunWeapon
)

screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
pygame.display.set_caption("Arcade Chaos Shooter")
clock = pygame.time.Clock()

available_weapons = [
    NormalWeapon,
    SpreadWeapon,
    RapidWeapon,
    HomingWeapon,
    LaserWeapon,
    ShotgunWeapon
]

state = "menu"   # menu / loadout / game
mode_selected = None
selected_loadout = []
max_slots = 3
game = None
running = True


def get_max_slots(mode):
    slot_map = {
        "classic": 3,
        "endless": 3,
        "bossrush": 2,
        "chaos": 4,
        "hardcore": 1,
    }
    return slot_map.get(mode, 3)


while running:
    clock.tick(60 if not game or game.slowmo <= 1 else 40)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        elif e.type == pygame.KEYDOWN:
            # ================= MENU =================
            if state == "menu":
                if e.key == pygame.K_1:
                    mode_selected = "classic"
                    selected_loadout = []
                    max_slots = get_max_slots(mode_selected)
                    state = "loadout"
                    continue

                elif e.key == pygame.K_2:
                    mode_selected = "endless"
                    selected_loadout = []
                    max_slots = get_max_slots(mode_selected)
                    state = "loadout"
                    continue

                elif e.key == pygame.K_3:
                    mode_selected = "bossrush"
                    selected_loadout = []
                    max_slots = get_max_slots(mode_selected)
                    state = "loadout"
                    continue

                elif e.key == pygame.K_4:
                    mode_selected = "chaos"
                    selected_loadout = []
                    max_slots = get_max_slots(mode_selected)
                    state = "loadout"
                    continue

                elif e.key == pygame.K_5:
                    mode_selected = "hardcore"
                    selected_loadout = []
                    max_slots = get_max_slots(mode_selected)
                    state = "loadout"
                    continue

            # ================= LOADOUT =================
            elif state == "loadout":
                if pygame.K_1 <= e.key <= pygame.K_6:
                    idx = e.key - pygame.K_1

                    if len(selected_loadout) < max_slots:
                        weapon_cls = available_weapons[idx]

                        already_taken = any(
                            isinstance(w, weapon_cls) for w in selected_loadout
                        )
                        if not already_taken:
                            selected_loadout.append(weapon_cls())

                elif e.key == pygame.K_BACKSPACE:
                    if selected_loadout:
                        selected_loadout.pop()

                elif e.key == pygame.K_RETURN:
                    if not selected_loadout:
                        selected_loadout = [NormalWeapon()]

                    game = Game(mode_selected, selected_loadout, screen)
                    state = "game"

                elif e.key == pygame.K_ESCAPE:
                    mode_selected = None
                    selected_loadout = []
                    state = "menu"

            # ================= GAME =================
            elif state == "game":
                if e.key == pygame.K_ESCAPE:
                    state = "menu"
                    mode_selected = None
                    selected_loadout = []
                    game = None

                elif e.key == pygame.K_q:
                    game.player.prev_weapon()

                elif e.key == pygame.K_e:
                    game.player.next_weapon()

    if state == "menu":
        draw_menu(screen)

    elif state == "loadout":
        draw_loadout(
            screen,
            selected_loadout,
            available_weapons,
            max_slots,
            mode_selected,
        )

    elif state == "game":
        game.update()
        game.draw()

    pygame.display.flip()

pygame.quit()