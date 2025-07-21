import pygame
import settings
from button import Button  # Předpokládám, že máš vlastní třídu Button

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.paused = False
        self.quit_requested = False
        self.restart_requested = False

        # Tlačítka s akcemi
        self.buttons = [
            Button("Pokračovat", settings.SCREEN_WIDTH // 2, 200, 200, 60, self.resume_game),
            Button("Restart", 300, 280, 200, 60, self.restart_game),
            Button("Ukončit", 300, 360, 200, 60, self.quit_game),
        ]

    def resume_game(self):
        self.paused = False

    def quit_game(self):
        self.quit_requested = True
        self.paused = False

    def restart_game(self):
        self.restart_requested = True
        self.paused = False

    def show_menu(self):
        self.paused = True
        self.quit_requested = False
        self.restart_requested = False

        clock = pygame.time.Clock()

        while self.paused:
            self.screen.fill((30, 30, 30))  # Pozadí menu

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
