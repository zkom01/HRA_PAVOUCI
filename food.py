"""
Modul Food obsahuje třídu Jidlo, která reprezentuje sbíratelné objekty (např. kapky oleje)
ve hře. Jídlo se objevuje na náhodných pozicích na herní ploše.
"""

import pygame
import random
import settings # Importujeme modul settings pro přístup k nastavení

class Jidlo(pygame.sprite.Sprite):
    """
    Třída Jidlo (Food) reprezentuje jeden sbíratelný objekt ve hře.

    Když hráč sebere jídlo, zvýší se mu skóre a přiblíží se k získání nového sudu.
    Jídlo se po sebrání objeví na nové náhodné pozici.

    Atributy:
        image (pygame.Surface): Načtený obrázek jídla.
        rect (pygame.Rect): Obdélník definující pozici a rozměry jídla.
        mask (pygame.mask.Mask): Maska pro pixel-perfect detekci kolizí jídla.
    """

    def __init__(self, image_name: str):
        """
        Konstruktor třídy Jidlo.

        Inicializuje nový objekt jídla s daným obrázkem a nastaví jeho počáteční
        pozici na náhodné místo na herní ploše.

        Args:
            image_name (str): Název souboru obrázku pro jídlo (např. "food.png").
                              Obrázek se načítá z adresáře 'media/img/'.
        """
        super().__init__()  # Volá konstruktor rodičovské třídy pygame.sprite.Sprite

        # Načtení obrázku jídla a zajištění průhlednosti (pokud je v obrázku alpha kanál).
        self.image = pygame.image.load(f"media/img/{image_name}").convert_alpha()
        
        self.rect = self.image.get_rect()  # Získá obdélník (rect) z obrázku pro pozici a rozměry.
        self.mask = pygame.mask.from_surface(self.image)  # Vytvoří masku z obrázku pro pixel-perfect kolize.
        
        # Nastaví počáteční pozici jídla náhodně, s ohledem na horní panel.
        self.rect.topleft = self.nahodna_pozice()

    def nahodna_pozice(self) -> tuple[int, int]:
        """
        Generuje náhodnou pozici pro jídlo v rámci herní plochy.

        Zajišťuje, aby se jídlo objevilo uvnitř viditelné herní oblasti,
        tedy pod horním informačním panelem a v rámci okrajů obrazovky.

        Returns:
            tuple[int, int]: Tuple (x, y) s náhodnými souřadnicemi,
                             kde jídlo bude umístěno.
        """
        jidlo_width = self.image.get_width()   # Zjistí šířku obrázku jídla.
        jidlo_height = self.image.get_height() # Zjistí výšku obrázku jídla.
        
        # Vygeneruje náhodné souřadnice X tak, aby se jídlo vešlo v horizontálním směru.
        x = random.randint(0, settings.SCREEN_WIDTH - jidlo_width)
        
        # Vygeneruje náhodné souřadnice Y tak, aby se jídlo vešlo ve vertikálním směru
        # a bylo vždy pod horním panelem (settings.VYSKA_HORNIHO_PANELU).
        y = random.randint(settings.VYSKA_HORNIHO_PANELU, settings.SCREEN_HEIGHT - jidlo_height)
        
        return x, y
