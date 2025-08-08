import pygame
import settings
from button import Button

class PauseMenu:
    """
    Třída PauseMenu spravuje zobrazení a interakci s pauzovacím menu hry.

    Umožňuje hráči pozastavit hru a zvolit si mezi pokračováním, restartem nebo ukončením hry.
    """

    def __init__(self, screen: pygame.Surface, game_instance):
        self.screen = screen
        self.screen_width = settings.SCREEN_WIDTH
        self.screen_height = settings.SCREEN_HEIGHT
        self.paused = False
        self.quit_requested = False
        self.restart_requested = False
        self.new_game_requested = False
        self.game_instance = game_instance
        self.confirm_dialog_active = False # True, pokud se zobrazuje potvrzovací dialog
        self.current_action_pending = None # Uloží 'restart' nebo 'quit', pro které čekáme na potvrzení
        self.text_confirm_dialog = ""

        # Nastavení rozměrů a pozice tlačítek
        button_width = 400
        button_height = 60
        self.start_y = (self.screen_height // 2) - 80
        button_spacing = 80 

        # Vytvoření tlačítek hlavního menu s callback funkcemi
        self.buttons: list[Button] = [
            Button("Nová hra", self.screen_width // 2, self.start_y, button_width, button_height, self._request_new_game_confirmation),
            Button("Pokračovat", self.screen_width // 2, self.start_y, button_width, button_height, self.resume_game),
            Button("Restart", self.screen_width // 2, self.start_y + button_spacing, button_width, button_height, self._request_restart_confirmation), # Změněno
            Button("Ukončit", self.screen_width // 2, self.start_y + (2 * button_spacing), button_width, button_height, self._request_quit_confirmation), # Změněno
        ]

        # Tlačítka pro potvrzovací dialog (ANO / NE)
        # Používáme lambdy pro předání True/False do callback funkce confirm_action
        self.confirm_buttons: list[Button] = [
            Button("ANO", self.screen_width // 2 - 100, self.screen_height // 2 + 50, 150, 50, lambda: self._confirm_action(True)),
            Button("NE", self.screen_width // 2 + 100, self.screen_height // 2 + 50, 150, 50, lambda: self._confirm_action(False))
        ]
        # Poznamenejte si, že pro `confirm_buttons` jsem zmenšil šířku a výšku a posunul je, aby byly vedle sebe.
        # Také jsem upravil `start_y` pro `confirm_buttons` aby byly lépe vycentrovány vzhledem k textu.

    def update_screen_size(self, width: int, height: int):
        self.screen_width = width
        self.screen_height = height
        center_x = self.screen_width // 2
        
        self.start_y = (self.screen_height // 2) - 80
        button_spacing = 80

        for i, button in enumerate(self.buttons):
            button.rect.centerx = center_x
            button.rect.centery = self.start_y + (i * button_spacing)

        # Aktualizuj pozice potvrzovacích tlačítek také
        self.confirm_buttons[0].rect.center = (self.screen_width // 2 - 100, self.screen_height // 2 + 50)
        self.confirm_buttons[1].rect.center = (self.screen_width // 2 + 100, self.screen_height // 2 + 50)


    def resume_game(self):
        self.paused = False

    # NOVÉ CALLBACK FUNKCE PRO TLAČÍTKA "RESTART" A "UKONČIT A "NOVÁ HRA" "
    def _request_new_game_confirmation(self):
        """Nastaví stav pro zobrazení potvrzení pro restart."""
        self.confirm_dialog_active = True
        self.current_action_pending = "new_game"
        self.text_confirm_dialog = "NOVÁ HRA"

    def _request_restart_confirmation(self):
        """Nastaví stav pro zobrazení potvrzení pro restart."""
        self.confirm_dialog_active = True
        self.current_action_pending = "restart"
        self.text_confirm_dialog = "RESTART"

    def _request_quit_confirmation(self):
        """Nastaví stav pro zobrazení potvrzení pro ukončení."""
        self.confirm_dialog_active = True
        self.current_action_pending = "ukončit"
        self.text_confirm_dialog = "UKONČIT"

    def _confirm_action(self, confirmed: bool):
        """
        Zpracuje výsledek potvrzovacího dialogu.
        Args:
            confirmed (bool): True, pokud uživatel potvrdil akci (ANO), False pokud ne (NE).
        """
        self.confirm_dialog_active = False # Skryjeme potvrzovací dialog
        if confirmed:
            if self.current_action_pending == "restart":
                self.restart_requested = True
                self.paused = False # Ukončí smyčku menu
            elif self.current_action_pending == "ukončit":
                self.quit_requested = True
                self.paused = False # Ukončí smyčku menu
            elif self.current_action_pending == "new_game":
                self.new_game_requested = True
                self.paused = False # Ukončí smyčku menu
        else:
            # Pokud uživatel zvolil NE, resetujeme čekající akci a zůstaneme v hlavním menu pauzy
            self.current_action_pending = None
            # Není potřeba nic dělat, show_menu smyčka bude pokračovat a zobrazí hlavní menu
            self.game_instance.kresleni()


    def show_menu(self) -> str:
        self.paused = True
        self.quit_requested = False
        self.restart_requested = False
        self.new_game_requested = False
        self.confirm_dialog_active = False # Zajištění, že začínáme v hlavním menu
        self.current_action_pending = None
        self.update_screen_size(settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT)

        clock = pygame.time.Clock()

        while self.paused:
            if not self.confirm_dialog_active:
                # Vykreslení hlavních tlačítek menu
                for button in self.buttons:
                    button.draw(self.screen)
            else:
                dialog_width = 500
                dialog_height = 200
                dialog_rect = pygame.Rect(0, 0, dialog_width, dialog_height)
                dialog_rect.center = (self.screen_width // 2, self.screen_height // 2)

                # Vyplnění pozadí dialogu (podobně jako u tlačítek)
                pygame.draw.rect(self.screen, settings.POZADI_MENU, dialog_rect, border_radius=20)
                # Volitelné: ohraničení dialogu
                pygame.draw.rect(self.screen, settings.BORDER, dialog_rect, 3,
                                 border_radius=20)  # Bílý rámeček, tloušťka 3px

                # Text výzvy
                prompt_text = f"Opravdu {self.text_confirm_dialog}?"
                font_large = pygame.font.Font(settings.FONT_ROBOT_PATH, 50)
                prompt_surface = font_large.render(prompt_text, True, settings.BARVA_TEXTU_MENU )
                # Umístíme text relativně k dialog_rect, nikoli k celé obrazovce
                prompt_rect = prompt_surface.get_rect(center=(dialog_rect.centerx, dialog_rect.top + 50))
                self.screen.blit(prompt_surface, prompt_rect)

                # Vykreslení ANO/NE tlačítek
                # Aktualizujeme pozice ANO/NE tlačítek tak, aby byly relativní k dialog_rect
                # nebo se jen ujistíme, že jejich absolutní pozice sedí uvnitř dialog_rect
                self.confirm_buttons[0].rect.center = (dialog_rect.centerx - 100, dialog_rect.bottom - 50)
                self.confirm_buttons[1].rect.center = (dialog_rect.centerx + 100, dialog_rect.bottom - 50)

                for button in self.confirm_buttons:
                    button.draw(self.screen)

            # Zpracování událostí
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_requested = True
                    self.paused = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = False # Resume hru
                    elif event.key == pygame.K_F11:
                        self.game_instance.fullscreen()
                        self.game_instance.kresleni() # Vykreslí herní scénu po změně fullscreenu
                # Zpracování kliknutí jen na aktivní sadu tlačítek
                if not self.confirm_dialog_active:
                    for button in self.buttons:
                        button.handle_event(event)
                else:
                    for button in self.confirm_buttons:
                        button.handle_event(event)

            pygame.display.flip()
            clock.tick(settings.FPS)

        if self.quit_requested:
            return "quit"
        elif self.restart_requested:
            return "restart"
        elif self.new_game_requested:
            return "new_game"
        else:
            return "resume"