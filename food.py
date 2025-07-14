import pygame
import random
import settings # Importujeme modul settings pro přístup k nastavení

class Jidlo(pygame.sprite.Sprite):
    """
    Třída Jidlo (Food) reprezentuje sbíratelné objekty ve hře (např. kapky oleje).
    """

    def __init__(self, image_name):
        """
        Konstruktor třídy Jidlo.
        :param image_name: Název souboru obrázku pro jídlo (načítá se z 'media/img/').
        """
        super().__init__()  # Volá konstruktor rodičovské třídy pygame.sprite.Sprite
        self.image = pygame.image.load(f"media/img/{image_name}").convert_alpha()  # Načte obrázek jídla
        self.rect = self.image.get_rect()  # Získá obdélník (rect) z obrázku
        self.mask = pygame.mask.from_surface(self.image)  # Vytvoří masku z obrázku pro pixel-perfect kolize
        # Nastaví počáteční pozici jídla náhodně, s ohledem na horní panel
        self.rect.topleft = self.nahodna_pozice()

    def nahodna_pozice(self):
        """
        Generuje náhodnou pozici pro jídlo v rámci herní plochy,
        s ohledem na rozměry obrazovky a horní panel ze settings.
        :return: Tuple (x, y) s náhodnými souřadnicemi.
        """
        jidlo_width = self.image.get_width()  # Zjistí šířku obrázku
        jidlo_height = self.image.get_height()  # Zjistí výšku obrázku
        # Vygeneruje náhodné souřadnice X a Y tak, aby se obrázek vešel na obrazovku
        # a byl pod horním panelem
        x = random.randint(0, settings.SCREEN_WIDTH - jidlo_width)
        y = random.randint(settings.VYSKA_HORNIHO_PANELU, settings.SCREEN_HEIGHT - jidlo_height)
        return x, y