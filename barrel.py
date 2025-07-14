import pygame

class Sud(pygame.sprite.Sprite):
    """
    Třída Sud (Barrel) reprezentuje segmenty "hada" hráče, které se přidávají
    po sebrání dostatečného množství jídla.
    """

    def __init__(self, x, y, image_name):
        """
        Konstruktor třídy Sud.
        :param x: Počáteční X souřadnice sudu.
        :param y: Počáteční Y souřadnice sudu.
        :param image_name: Název souboru obrázku pro sud (načítá se z 'media/img/').
        """
        super().__init__()  # Volá konstruktor rodičovské třídy pygame.sprite.Sprite
        self.image = pygame.image.load(f"media/img/{image_name}").convert_alpha()  # Načte obrázek sudu
        self.rect = self.image.get_rect()  # Získá obdélník z obrázku
        self.mask = pygame.mask.from_surface(self.image)  # Maska pro sudy pro pixel-perfect kolize
        self.rect.center = (x, y)  # Nastaví počáteční pozici sudu (na střed)