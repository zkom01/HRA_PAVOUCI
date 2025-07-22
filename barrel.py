"""
Modul Barrel obsahuje třídu Sud, která reprezentuje jeden segment "hada" hráče.
Tyto sudy se přidávají k hráči, když sbírá jídlo.
"""

import pygame

class Sud(pygame.sprite.Sprite):
    """
    Třída Sud (Barrel) reprezentuje jednotlivé segmenty "hada" hráče.

    Každý objekt Sud je vizuální reprezentací části "těla" hráče a pohybuje se
    na základě historických pozic hlavy hráče. Slouží také pro detekci kolizí
    v případě, že by se "had" mohl s něčím srazit (i když ve tvém kódu
    primárně jen sleduje hráče).

    Atributy:
        image (pygame.Surface): Načtený obrázek sudu.
        rect (pygame.Rect): Obdélník definující pozici a rozměry sudu.
        mask (pygame.mask.Mask): Maska pro pixel-perfect detekci kolizí sudu.
    """

    def __init__(self, x: int, y: int, image_name: str):
        """
        Konstruktor třídy Sud.

        Inicializuje nový sud s danou pozicí a obrázkem.

        Args:
            x (int): Počáteční X souřadnice středu sudu.
            y (int): Počáteční Y souřadnice středu sudu.
            image_name (str): Název souboru obrázku pro sud (např. "barrel.png").
                              Obrázek se načítá z adresáře 'media/img/'.
        """
        super().__init__()  # Volá konstruktor rodičovské třídy pygame.sprite.Sprite

        # Načtení obrázku sudu a zajištění průhlednosti (pokud je v obrázku alpha kanál).
        self.image = pygame.image.load(f"media/img/{image_name}").convert_alpha()
        
        self.rect = self.image.get_rect()  # Získá obdélník z obrázku pro pozici a rozměry.
        self.mask = pygame.mask.from_surface(self.image)  # Vytvoří masku pro přesné kolize.
        
        self.rect.center = (x, y)  # Nastaví počáteční pozici sudu na zadané souřadnice (střed).
