# name_input.py
import pygame
import settings

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
        self.cursor_timer = pygame.time.get_ticks()  # Pro blikání kurzoru

        # Barvy a fonty - Použijeme barvy ze settings, aby to bylo konzistentní s PauseMenu
        # Pokud nemáte tyto barvy v settings.py, budete je muset tam přidat.
        self.WHITE = settings.WHITE  # Např. (255, 255, 255)
        self.GRAY = (70, 70, 70)  # Barva pro input box
        self.BORDER_COLOR = (200, 200, 200)  # Barva okraje input boxu
        self.TEXT_COLOR = (255, 255, 255)  # Barva textu v input boxu

        # Fonty - také by měly být načteny ze settings pro konzistenci
        # Předpokládám, že settings.FONT_ROBOT_PATH existuje a je cesta k fontu
        self.font = pygame.font.Font(settings.FONT_ROBOT_PATH, 50)

        # Parametry dialogového rámečku (stejné jako u potvrzovacího dialogu v PauseMenu)
        self.dialog_width = 500  # Použito 500 jako v PauseMenu
        self.dialog_height = 250  # Upravena výška, aby se vešly prvky, 200 bylo málo
        # Vypočítáme pozici dialogu, aby byl vycentrován na obrazovce
        self.dialog_x = (settings.SCREEN_WIDTH // 2)
        self.dialog_y = (settings.SCREEN_HEIGHT // 2) + settings.VYSKA_HORNIHO_PANELU

        # Vstupní pole - Inicializujeme s jeho skutečnými rozměry,
        # pozici pak doladíme v draw metodě, aby bylo vycentrováno uvnitř dialogu
        self.input_box = pygame.Rect(0, 0, 400, 50)  # Šířka 400, výška 50

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
                    self.cursor_visible = False  # Skryje kurzor
                    return self.player_name  # Vrátí zadané jméno
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                # Přidá znak, pokud je tisknutelný a jméno není příliš dlouhé (max. 8 znaků)
                if event.unicode.isprintable() and len(self.player_name) < 8:
                    self.player_name += event.unicode
            self.cursor_visible = True  # Resetuje blikání kurzoru po každém stisku
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
        Vykreslí všechny elementy pro zadávání jména na obrazovku,
        umístěné uvnitř centrálního dialogového rámečku.
        Vykresluje také poloprůhledný overlay přes celé pozadí (které už vykresluje main.py).

        Args:
            screen (pygame.Surface): Pygame surface, na kterou se má vykreslit.
        """
        # --- Krok 1: Vykreslení ztmaveného overlay přes celé pozadí hry ---
        # Použijeme stejný styl jako pro overlay v PauseMenu (obvykle se to děje v main.py nebo Game)
        # Ale pokud chceme zajistit, že je VŽDY ztmaveno, i když se NameInput volá jinak,
        # můžeme to udělat i zde. Nicméně doporučuji to dělat V main.py/Game před voláním NameInput.draw().
        # Zde to pro tento příklad necháme být, aby to odpovídalo původnímu chování NameInput,
        # kde se očekává, že pozadí se nakreslí jinde.

        # K vytvoření stylu rámečku z PauseMenu potřebujeme:
        # A. dialog_rect pro umístění dialogu
        dialog_rect = pygame.Rect(self.dialog_x, self.dialog_y, self.dialog_width, self.dialog_height)

        # B. Vyplnění pozadí dialogu (podobně jako u tlačítek v PauseMenu)
        # settings.BARVA_POD_TEXT_NABIDKY je barva pozadí menu/dialogů
        pygame.draw.rect(screen, settings.BARVA_POD_TEXT_NABIDKY, dialog_rect, border_radius=10)

        # C. Ohraničení dialogu
        pygame.draw.rect(screen, settings.WHITE, dialog_rect, 3, border_radius=10)  # Bílý rámeček, tloušťka 3px

        # --- Krok 2: Vykreslení textu výzvy "Zadejte jméno:" ---
        # Použijeme font, který je již inicializován s FONT_ROBOT_PATH
        prompt_text = "Zadejte jméno:"
        prompt_surface = self.font.render(prompt_text, True, self.WHITE)

        # Umístíme text relativně k dialog_rect, nikoli k celé obrazovce
        # Vertikální pozice: 50 pixelů od horního okraje dialogu
        prompt_rect = prompt_surface.get_rect(center=(dialog_rect.centerx, dialog_rect.top + 70))
        screen.blit(prompt_surface, prompt_rect)

        # --- Krok 3: Pozicování a vykreslení vstupního pole (input_box) ---
        # Vycentrujeme input_box horizontálně v dialogu
        self.input_box.centerx = dialog_rect.centerx
        # Umístíme input_box pod text výzvy s mezerou 20 pixelů
        self.input_box.y = prompt_rect.bottom + 20

        pygame.draw.rect(screen, self.GRAY, self.input_box, border_radius=30)
        pygame.draw.rect(screen, self.BORDER_COLOR, self.input_box, 2, border_radius=30)

        # --- Krok 4: Vykreslení zadaného textu jména uvnitř input_boxu ---
        text_surface = self.font.render(self.player_name, True, self.TEXT_COLOR)
        # Text je vycentrován v input boxu
        text_x = self.input_box.x + (self.input_box.width - text_surface.get_width()) // 2
        text_y = self.input_box.y

        # --- Krok 5: Vykreslení blikajícího kurzoru ---
        if self.cursor_visible and self.input_active:
            cursor_x = text_x + text_surface.get_width() + 5  # Kousek za textem
            cursor_y = text_y
            pygame.draw.line(screen, self.WHITE, (cursor_x, cursor_y),
                             (cursor_x, cursor_y + self.font.get_height()))

        # --- Krok 6: Zpráva pro pokračování po zadání jména ---
        if not self.input_active:
            pokracuj_text = self.font.render("Jméno potvrzeno. Klikněte myší pro spuštění hry.", True,
                                             self.WHITE)
            # Umístíme text pro pokračování pod input_box s mezerou
            pokracuj_rect = pokracuj_text.get_rect(center=(dialog_rect.centerx, self.input_box.bottom + 50))
            screen.blit(pokracuj_text, pokracuj_rect)