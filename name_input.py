# name_input.py
import pygame

class NameInput:
    """
    Třída pro zadávání jména hráče před spuštěním hry.
    Spravuje vykreslování vstupního pole, kurzoru a zpracování klávesových událostí.
    """
    def __init__(self, screen):
        """
        Inicializuje instanci NameInput.

        Args:
            screen (pygame.Surface): Objekt Surface, na který se bude vykreslovat.
        """
        self.screen = screen
        self.player_name = ""
        self.input_active = True  # Určuje, zda je vstupní pole aktivní pro psaní
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks() # Pro blikání kurzoru

        # Barvy (můžete je později přesunout do settings.py pro jednotnost)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (70, 70, 70)
        self.LIGHT_GRAY = (100, 100, 100)
        self.BORDER_COLOR = (200, 200, 200)
        self.TEXT_COLOR = (255, 255, 255)

        # Fonty
        self.font_large = pygame.font.SysFont(None, 74)
        self.font_medium = pygame.font.SysFont(None, 50)

        # Vstupní pole
        # Pozice se zatím počítá centrálně, později ji přizpůsobíme dialogu
        self.input_box = pygame.Rect(screen.get_width() // 2 - 200, self.screen.get_height() // 2 + 60, 400, 50)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """
        Zpracovává události Pygame (např. stisky kláves) pro zadávání jména.

        Args:
            event (pygame.event.Event): Událost Pygame k zpracování.

        Returns:
            str | None: Vrátí zadané jméno, pokud bylo potvrzeno klávesou Enter
                        a je delší než 0, jinak None.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.player_name:
                    self.input_active = False  # Zneaktivní input po stisku Enter
                    self.cursor_visible = False # Skryje kurzor
                    return self.player_name  # Vrátí zadané jméno
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                # Přidá znak, pokud je tisknutelný a jméno není příliš dlouhé
                if event.unicode.isprintable() and len(self.player_name) < 15: # Omezení délky jména
                    self.player_name += event.unicode
            self.cursor_visible = True # Resetuje blikání kurzoru po každém stisku
            self.cursor_timer = pygame.time.get_ticks()
        return None  # Jméno zatím nebylo potvrzeno

    def update(self):
        """
        Aktualizuje stav NameInput, zejména blikání kurzoru.
        Tato metoda by měla být volána v každém snímku hlavní smyčky.
        """
        if self.input_active:
            dt = pygame.time.get_ticks() - self.cursor_timer
            if dt > 500:  # Bliká každých 500 ms
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = pygame.time.get_ticks()

    def draw(self, screen: pygame.Surface):
        """
        Vykreslí všechny elementy pro zadávání jména na obrazovku.

        Args:
            screen (pygame.Surface): Pygame surface, na kterou se má vykreslit.
        """
        screen.fill(self.BLACK) # Vyplní celé pozadí černou barvou

        # Text výzvy "Zadejte jméno:"
        prompt = self.font_large.render("Zadejte jméno:", True, self.WHITE)
        prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - prompt.get_height() // 2 - 80))
        screen.blit(prompt, prompt_rect)

        # Vstupní pole
        pygame.draw.rect(screen, self.GRAY, self.input_box, border_radius=30)
        pygame.draw.rect(screen, self.BORDER_COLOR, self.input_box, 2, border_radius=30)

        # Zadaný text jména
        text_surface = self.font_medium.render(self.player_name, True, self.TEXT_COLOR)
        # Text je vycentrován v input boxu
        text_x = self.input_box.x + (self.input_box.width - text_surface.get_width()) // 2
        text_y = self.input_box.y + (self.input_box.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        # Blikající kurzor
        if self.cursor_visible and self.input_active:
            cursor_x = text_x + text_surface.get_width() + 5 # Kousek za textem
            cursor_y = text_y
            pygame.draw.line(screen, self.WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + self.font_medium.get_height()), 2)

        # Zpráva pro pokračování po zadání jména
        if not self.input_active:
            pokracuj_text = self.font_medium.render("Jméno potvrzeno. Klikněte myší pro spuštění hry.", True, self.WHITE)
            pokracuj_rect = pokracuj_text.get_rect(center=(screen.get_width() // 2, self.input_box.bottom + 50))
            screen.blit(pokracuj_text, pokracuj_rect)