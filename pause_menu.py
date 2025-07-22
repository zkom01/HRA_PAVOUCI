"""
Modul PauseMenu obsahuje třídu PauseMenu, která vytváří a spravuje pauzovací obrazovku ve hře.
Nabízí možnosti pro pokračování hry, restartování nebo ukončení.
"""

import pygame
import settings
from button import Button  # Předpokládám, že máš vlastní třídu Button

class PauseMenu:
    """
    Třída PauseMenu spravuje zobrazení a interakci s pauzovacím menu hry.

    Umožňuje hráči pozastavit hru a zvolit si mezi pokračováním, restartem nebo ukončením hry.

    Atributy:
        screen (pygame.Surface): Hlavní Pygame surface, na kterou se menu vykresluje.
        screen_width (int): Aktuální šířka obrazovky.
        screen_height (int): Aktuální výška obrazovky.
        paused (bool): Logická hodnota indikující, zda je hra v režimu pauzy.
        quit_requested (bool): Logická hodnota indikující, zda hráč požádal o ukončení hry.
        restart_requested (bool): Logická hodnota indikující, zda hráč požádal o restart hry.
        buttons (list[Button]): Seznam objektů Button, které tvoří menu.
    """

    def __init__(self, screen: pygame.Surface, screen_width: int, screen_height: int):
        """
        Inicializuje novou instanci pauzovacího menu.

        Args:
            screen (pygame.Surface): Hlavní Pygame surface pro vykreslování.
            screen_width (int): Počáteční šířka okna hry.
            screen_height (int): Počáteční výška okna hry.
        """
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.paused = False
        self.quit_requested = False
        self.restart_requested = False

        # Nastavení rozměrů a pozice tlačítek
        button_width = 200
        button_height = 60
        # Počáteční Y pozice prvního tlačítka, od níž se odvozují ostatní
        start_y = (self.screen_height // 2) + 80
        # Mezera mezi tlačítky
        button_spacing = 80 

        # Vytvoření tlačítek menu s callback funkcemi
        self.buttons: list[Button] = [
            Button("Pokračovat", self.screen_width // 2, start_y, button_width, button_height, self.resume_game),
            Button("Restart", self.screen_width // 2, start_y + button_spacing, button_width, button_height, self.restart_game),
            Button("Ukončit", self.screen_width // 2, start_y + (2 * button_spacing), button_width, button_height, self.quit_game),
        ]

    def update_screen_size(self, width: int, height: int):
        """
        Aktualizuje rozměry obrazovky a přepočítá pozice tlačítek.

        Tato metoda by měla být volána, pokud se velikost okna hry změní,
        aby se tlačítka správně vycentrovala.

        Args:
            width (int): Nová šířka obrazovky.
            height (int): Nová výška obrazovky.
        """
        self.screen_width = width
        self.screen_height = height
        center_x = self.screen_width // 2
        
        # Aktualizace Y pozice pro centrování tlačítek po změně velikosti okna.
        # Výchozí Y pozice pro první tlačítko.
        start_y = (self.screen_height // 2) + 80 
        button_spacing = 80

        # Aktualizuj pozice tlačítek pomocí for cyklu
        # To je lepší pro rozšiřitelnost, pokud přidáš více tlačítek.
        for i, button in enumerate(self.buttons):
            button.rect.centerx = center_x
            button.rect.centery = start_y + (i * button_spacing)


    def resume_game(self):
        """
        Callback funkce pro tlačítko "Pokračovat".
        Nastaví stav hry na nepozastavený.
        """
        self.paused = False

    def restart_game(self):
        """
        Callback funkce pro tlačítko "Restart".
        Nastaví stav hry na nepozastavený a signalizuje požadavek na restart.
        """
        self.paused = False
        self.restart_requested = True

    def quit_game(self):
        """
        Callback funkce pro tlačítko "Ukončit".
        Nastaví stav hry na nepozastavený a signalizuje požadavek na ukončení.
        """
        self.paused = False
        self.quit_requested = True

    def show_menu(self) -> str:
        """
        Zobrazí pauzovací menu a zpracovává uživatelské vstupy, dokud není menu opuštěno.

        Vykresluje tlačítka, reaguje na kliknutí a na událost zavření okna.

        Returns:
            str: Řetězec indikující výsledek interakce s menu:
                 "resume" (pokračovat ve hře), "restart" (restartovat hru) nebo "quit" (ukončit hru).
        """
        self.paused = True          # Aktivuje stav pauzy
        self.quit_requested = False # Resetuje požadavky před zobrazením menu
        self.restart_requested = False # Resetuje požadavky před zobrazením menu

        clock = pygame.time.Clock() # Pro kontrolu FPS menu

        # Hlavní smyčka pauzovacího menu
        while self.paused:
            # Volitelné: Zde můžeš vykreslit tmavé pozadí nebo jiný vizuální prvek menu
            # self.screen.fill((30, 30, 30))  # Příklad tmavého pozadí menu

            # Vykreslení všech tlačítek na obrazovku
            for button in self.buttons:
                button.draw(self.screen)

            # Zpracování událostí
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Pokud uživatel zavře okno, nastaví požadavek na ukončení hry
                    self.quit_requested = True
                    self.paused = False # Ukončí smyčku menu
                
                # Předá událost každému tlačítku pro zpracování kliknutí
                for button in self.buttons:
                    button.handle_event(event)

            pygame.display.flip() # Aktualizuje celou obrazovku pro zobrazení menu
            clock.tick(settings.FPS) # Omezí počet snímků za sekundu pro menu

        # Po ukončení smyčky menu vrátí výsledek akce
        if self.quit_requested:
            return "quit"
        elif self.restart_requested:
            return "restart"
        else:
            return "resume"
