"""
Modul Button obsahuje třídu Button, která poskytuje interaktivní tlačítka
pro uživatelské rozhraní hry. Tlačítka reagují na najetí myši a kliknutí,
spouštějí předdefinované akce.
"""

import pygame
import settings

class Button:
    """
    Třída Button reprezentuje interaktivní tlačítko v grafickém uživatelském rozhraní (GUI).

    Tlačítko má text, rozměry a pozici, mění barvu při najetí myší
    a spouští určenou funkci (callback) po kliknutí.

    Atributy:
        text (str): Text zobrazený na tlačítku.
        rect (pygame.Rect): Obdélník definující pozici a rozměry tlačítka.
        color_normal (tuple[int, int, int]): Barva tlačítka v normálním stavu (RGB).
        color_hover (tuple[int, int, int]): Barva tlačítka při najetí myši (RGB).
        text_color (tuple[int, int, int]): Barva textu na tlačítku (RGB).
        callback (callable): Funkce, která se zavolá, když se na tlačítko klikne.
        font (pygame.font.Font): Písmo použité pro text tlačítka.
    """

    def __init__(self, text: str, x: int, y: int, width: int, height: int, callback: callable):
        """
        Inicializuje novou instanci tlačítka.

        Args:
            text (str): Text, který se má zobrazit na tlačítku.
            x (int): X-ová souřadnice levého horního rohu tlačítka.
            y (int): Y-ová souřadnice levého horního rohu tlačítka.
            width (int): Šířka tlačítka.
            height (int): Výška tlačítka.
            callback (callable): Funkce bez argumentů, která se zavolá, když uživatel
                                 klikne na tlačítko.
        """
        self.text = text
        self.rect = pygame.Rect(x, y, width, height) # Vytvoří obdélníkovou oblast pro tlačítko
        
        # Barevná schémata pro různé stavy tlačítka
        self.color_normal = settings.SCREEN_COLOR   # Tmavší šedá pro normální stav
        self.color_hover = settings.WHITE # Světlejší šedá pro najetí myši
        self.text_color = settings.BARVA_TEXTU  # Bílá barva textu

        self.callback = callback # Funkce, která se spustí po kliknutí
        self.font = pygame.font.Font(settings.FONT_ROBOT_PATH, 40) # Nastavení písma pro text tlačítka

    def draw(self, surface: pygame.Surface):
        """
        Vykreslí tlačítko na danou Pygame surface.

        Tato metoda kontroluje pozici myši, aby určila, zda je na tlačítko najeto,
        a podle toho vybere barvu pozadí. Poté vykreslí zaoblený obdélník,
        okraj a vycentrovaný text.

        Args:
            surface (pygame.Surface): Pygame surface, na kterou se má tlačítko vykreslit.
        """
        mouse_pos = pygame.mouse.get_pos() # Získá aktuální pozici kurzoru myši
        is_hover = self.rect.collidepoint(mouse_pos) # Zjistí, zda se kurzor nachází nad tlačítkem
        
        # Vybere barvu na základě stavu najetí myši
        color = self.color_hover if is_hover else self.color_normal
        
        # Vykreslí pozadí tlačítka se zaoblenými rohy
        pygame.draw.rect(surface, color, self.rect, border_radius=20)
        # Vykreslí tenký okraj kolem tlačítka
        pygame.draw.rect(surface, settings.WHITE, self.rect, 3, border_radius=20)
        
        # Vykreslení textu na tlačítku
        text_surf = self.font.render(self.text, True, self.text_color) # Vytvoří surface s textem
        text_rect = text_surf.get_rect(center=self.rect.center)       # Získá obdélník textu a vycentruje ho na tlačítku
        text_rect.y -= 3 # použitý font je ve skutečnosti vyšší (diakritika) proto -3px
        surface.blit(text_surf, text_rect) # Nakreslí text na surface

    def handle_event(self, event: pygame.event.Event):
        """
        Zpracovává vstupní události Pygame pro interakci s tlačítkem.

        Pokud je událost kliknutí levým tlačítkem myši a pozice kliknutí
        spadá do oblasti tlačítka, zavolá se připojená callback funkce.

        Args:
            event (pygame.event.Event): Událost Pygame (např. kliknutí myši).
        """
        # Kontroluje, zda se jedná o stisknutí tlačítka myši a zda bylo stisknuto levé tlačítko (button == 1)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Kontroluje, zda kliknutí proběhlo uvnitř oblasti tlačítka
            if self.rect.collidepoint(event.pos):
                self.callback() # Pokud ano, zavolá připojenou funkci (callback)
