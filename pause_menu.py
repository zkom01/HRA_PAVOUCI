import pygame
import sys
from button import Button


class PauseMenu:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.paused = False
        self.restart_requested = False
        self.buttons = [
            Button("Pokračovat", 300, 200, 200, 60, self.resume_game),
            Button("Restart", 300, 280, 200, 60, self.restart_game),
            Button("Ukončit", 300, 360, 200, 60, self.quit_game),
        ]

    def resume_game(self):
        self.paused = False

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()

    def restart_game(self):
        self.restart_requested = True

    def show_menu(self):
        self.paused = True
        self.restart_requested = False

        while self.paused:
            self.screen.fill((30, 30, 30))
            for button in self.buttons:
                button.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                for button in self.buttons:
                    button.handle_event(event)
            pygame.display.flip()
            self.clock.tick(60)
            if self.restart_requested:
                return "restart"

        # Přidáme return statement sem.
        # Pokud se smyčka ukončila a nebyl požadován restart, znamená to, že se hra obnovila.
        return "resume"  # nebo cokoli jiného, co indikuje obnovení hry