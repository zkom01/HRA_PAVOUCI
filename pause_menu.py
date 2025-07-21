import pygame
import settings
from button import Button  # Předpokládám, že máš vlastní třídu Button

class PauseMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.paused = False
        self.quit_requested = False
        self.restart_requested = False
        button_width = 200
        button_height = 60
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        # Tlačítka s akcemi
        self.buttons = [
            Button("Pokračovat", center_x, center_y + 80, button_width, button_height, self.resume_game),
            Button("Restart", center_x, center_y + 160, button_width, button_height, self.restart_game),
            Button("Ukončit", center_x, center_y + 240, button_width, button_height, self.quit_game),
        ]

    def update_screen_size(self, width, height):
        self.screen_width = width
        self.screen_height = height
        center_x = self.screen_width // 2
# použij for pro aktualizaci buttons aby jsi mohl přidávat tlačítka!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Aktualizuj pozici tlačítek
        self.buttons[0].rect.centerx = center_x
        self.buttons[1].rect.centerx = center_x
        self.buttons[2].rect.centerx = center_x

    def resume_game(self):
        self.paused = False

    def restart_game(self):
        self.paused = False

    def quit_game(self):
        self.paused = False
        self.quit_requested = True

    def show_menu(self):
        self.paused = True
        self.quit_requested = False
        self.restart_requested = False

        clock = pygame.time.Clock()

        while self.paused:
            # self.screen.fill((30, 30, 30))  # Pozadí menu

            for button in self.buttons:
                button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_requested = True
                    self.paused = False
                for button in self.buttons:
                    button.handle_event(event)

            pygame.display.flip()
            clock.tick(settings.FPS)

        if self.quit_requested:
            return "quit"
        elif self.restart_requested:
            return "restart"
        else:
            return "resume"
