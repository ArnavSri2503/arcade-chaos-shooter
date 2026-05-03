import pygame
import settings as s


def draw_menu(screen):
    screen.fill(s.BLACK)

    title = s.BIG.render("ARCADE CHAOS SHOOTER", True, s.CYAN)
    screen.blit(title, (40, 60))

    modes = [
        "1 - Classic",
        "2 - Endless Survival",
        "3 - Boss Rush",
        "4 - Chaos Arena",
        "5 - Hardcore"
    ]

    desc = [
        "Wave -> Boss -> Chaos progression",
        "Infinite scaling enemy waves",
        "Continuous boss fights only",
        "Pattern-based controlled insanity",
        "1 HP challenge mode"
    ]

    for i in range(5):
        y = 180 + i * 70
        screen.blit(s.FONT.render(modes[i], True, s.WHITE), (80, y))
        screen.blit(s.SMALL.render(desc[i], True, s.GRAY), (100, y + 30))

    instructions = [
        "CONTROLS / HOW TO PLAY:",
        "Arrow Keys  - Move",
        "Hold Shift  - Focus / Slow Movement",
        "Weapons Auto-Fire Continuously",
        "Q / E - Cycle Weapons In Game",
        "ESC - Return To Menu",
        "Select a mode to continue"
    ]

    start_y = 560
    for i, text in enumerate(instructions):
        color = s.CYAN if i == 0 else s.WHITE
        screen.blit(s.SMALL.render(text, True, color), (20, start_y + i * 20))


def draw_loadout(screen, selected, available, max_slots, mode_selected):
    screen.fill(s.BLACK)

    title = s.BIG.render("SELECT LOADOUT", True, s.CYAN)
    screen.blit(title, (s.WIDTH // 2 - title.get_width() // 2, 40))

    mode_text = s.FONT.render(f"Mode: {mode_selected.upper()}", True, s.YELLOW)
    screen.blit(mode_text, (s.WIDTH // 2 - mode_text.get_width() // 2, 95))

    slot_text = s.FONT.render(f"Slots: {len(selected)}/{max_slots}", True, s.YELLOW)
    screen.blit(slot_text, (300, 140))

    screen.blit(s.FONT.render("AVAILABLE", True, s.WHITE), (70, 140))
    screen.blit(s.FONT.render("SELECTED", True, s.WHITE), (300, 180))

    for i, weapon_cls in enumerate(available):
        y = 180 + i * 45
        txt = s.FONT.render(f"{i+1} - {weapon_cls.name}", True, s.WHITE)
        screen.blit(txt, (70, y))

    for i, weapon in enumerate(selected):
        y = 220 + i * 35
        txt = s.FONT.render(weapon.name, True, s.GREEN)
        screen.blit(txt, (300, y))

    hint1 = s.SMALL.render("1-6: Add weapon", True, s.GRAY)
    hint2 = s.SMALL.render("Backspace: Remove last", True, s.GRAY)
    hint3 = s.SMALL.render("Enter: Start game", True, s.GRAY)
    hint4 = s.SMALL.render("Esc: Back to mode select", True, s.GRAY)
    hint5 = s.SMALL.render("Duplicates are blocked", True, s.GRAY)

    screen.blit(hint1, (40, 590))
    screen.blit(hint2, (40, 612))
    screen.blit(hint3, (260, 590))
    screen.blit(hint4, (260, 612))
    screen.blit(hint5, (170, 640))