import pygame
from constants import *



def show_menu(screen):
    font = pygame.font.SysFont(None, 80)
    button_font = pygame.font.SysFont(None, 50)
    dev_font = pygame.font.SysFont(None, 30)
    clock = pygame.time.Clock()

    screen_width, screen_height = screen.get_size()

    # Définition des boutons centrés verticalement
    button_width, button_height = 250, 60
    spacing = 20
    start_y = screen_height // 2 - (button_height * 3 + spacing * 2) // 2

    buttons = {
        "Facile": pygame.Rect(screen_width // 2 - button_width // 2, start_y, button_width, button_height),
        "Moyenne": pygame.Rect(screen_width // 2 - button_width // 2, start_y + button_height + spacing, button_width, button_height),
        "Difficile": pygame.Rect(screen_width // 2 - button_width // 2, start_y + 2 * (button_height + spacing), button_width, button_height)
    }

    while True:
        screen.fill(BLACK)

        # Grand titre "Hello !"
        title_text = font.render("Hello !", True, WHITE)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 80))

        for name, rect in buttons.items():
            pygame.draw.rect(screen,    RED, rect, border_radius=10)
            text = button_font.render(name, True, WHITE)
            screen.blit(text, (rect.x + (rect.width - text.get_width()) // 2, rect.y + 10))

        # Noms des développeurs en bas
        dev_text = dev_font.render("Motaouakel - Mohamed - Hamza", True, WHITE)
        screen.blit(dev_text, (screen_width // 2 - dev_text.get_width() // 2, screen_height - 40))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for difficulty, rect in buttons.items():
                    if rect.collidepoint(mouse_pos):
                        if difficulty == "Facile":
                            return 10
                        elif difficulty == "Moyenne":
                            return 20
                        elif difficulty == "Difficile":
                            return 30