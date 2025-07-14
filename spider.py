import pygame
import random
import settings # Importujeme modul settings pro přístup k nastavení

class Pavouk(pygame.sprite.Sprite):
    """
    Třída Pavouk (Spider) reprezentuje nepřátelské objekty, které se pohybují
    po obrazovce a mohou hráči ubírat sudy nebo životy. Mění chování a vzhled
    na základě vzdálenosti od hráče.
    """

    def __init__(self, x, y, image_name, image_angry_name, rychlost):
        """
        Konstruktor třídy Pavouk.
        :param x: Počáteční X souřadnice pavouka.
        :param y: Počáteční Y souřadnice pavouka.
        :param image_name: Název souboru obrázku pro normální (klidný) stav pavouka.
        :param image_angry_name: Název souboru obrázku pro "naštvaný" stav pavouka.
        :param rychlost: Počáteční rychlost pavouka.
        """
        super().__init__()  # Volá konstruktor rodičovské třídy pygame.sprite.Sprite
        self.original_image = pygame.image.load(f"media/img/{image_name}").convert_alpha()  # Načte normální obrázek pavouka
        self.image = self.original_image  # Aktuální obrázek pavouka
        self.rect = self.image.get_rect()  # Získá obdélník z obrázku
        self.rect.topleft = (x, y)  # Nastaví počáteční pozici pavouka
        self.mask = pygame.mask.from_surface(self.image)  # Maska pro pixel-perfect kolize

        # Načtení a příprava obrázku "naštvaného" pavouka
        self.image_angry = pygame.image.load(f"media/img/{image_angry_name}").convert_alpha()

        self.original_speed = rychlost  # Původní (klidná) rychlost pavouka
        self.angry_speed = rychlost * 1.2  # Zvýšená rychlost, když je pavouk "naštvaný"
        self.speed = self.original_speed  # Aktuální rychlost pavouka
        self.rychlostni_koeficient = 1.0

        self.direct_x, self.direct_y = self.novy_smer()  # Nastaví počáteční náhodný směr pohybu
        self.pavouk_postava_vzdalenost = 300  # Vzdálenost (v pixelech), pod kterou se pavouk "naštve"
        self.change_dir_timer = 0  # Časovač pro náhodnou změnu směru pavouka v klidovém stavu
        self.is_angry = False  # Logická proměnná, zda je pavouk "naštvaný" a pronásleduje hráče

    @staticmethod
    def novy_smer():
        """
        Statická metoda, která vrací náhodný směr pohybu (nahoru, dolů, doleva, doprava)
        pro klidový stav pavouka.
        :return: Tuple (dx, dy) představující změnu souřadnic pro daný směr.
        """
        nahodny_smer = random.choice(['up', 'down', 'left', 'right'])  # Vybere náhodný směr
        if nahodny_smer == 'up':
            return 0, -1
        elif nahodny_smer == 'down':
            return 0, 1
        elif nahodny_smer == 'left':
            return -1, 0
        elif nahodny_smer == 'right':
            return 1, 0
        return 0, 0  # Měl by vždy vrátit hodnotu, takže 0,0 jako fallback

    def move(self, player_rect):
        """
        Aktualizuje pozici pavouka na základě jeho rychlosti a směru.
        Zajišťuje, aby pavouk zůstal v rámci hranic obrazovky a občas změní směr.
        Když je "naštvaný", směřuje k hráči.
        :param player_rect: Obdélník (rect) hráče pro cílení pohybu.
        """
        if self.is_angry:
            self.direct_x = 0
            self.direct_y = 0

            delta_x = player_rect.centerx - self.rect.centerx
            delta_y = player_rect.centery - self.rect.centery

            if abs(delta_x) > abs(delta_y):
                if delta_x > 0:
                    self.direct_x = 1
                else:
                    self.direct_x = -1
            else:
                if delta_y > 0:
                    self.direct_y = 1
                else:
                    self.direct_y = -1
        else:
            self.change_dir_timer += 1
            if self.change_dir_timer >= random.randint(60, 120):
                self.change_dir_timer = 0
                self.direct_x, self.direct_y = self.novy_smer()

        self.rect.x += self.speed * self.rychlostni_koeficient * self.direct_x
        self.rect.y += self.speed * self.rychlostni_koeficient * self.direct_y

        # Kontrola hranic obrazovky (pavouk se neodrazí, ale zůstane v herní oblasti)
        if self.rect.left < 0:
            self.rect.left = 0
            self.direct_x, self.direct_y = self.novy_smer()
        elif self.rect.right > settings.SCREEN_WIDTH: # Použijte nastavení
            self.rect.right = settings.SCREEN_WIDTH
            self.direct_x, self.direct_y = self.novy_smer()

        if self.rect.top < settings.VYSKA_HORNIHO_PANELU:  # Respektuje horní panel
            self.rect.top = settings.VYSKA_HORNIHO_PANELU
            self.direct_x, self.direct_y = self.novy_smer()
        elif self.rect.bottom > settings.SCREEN_HEIGHT: # Použijte nastavení
            self.rect.bottom = settings.SCREEN_HEIGHT
            self.direct_x, self.direct_y = self.novy_smer()

    def priblizeni(self, player_rect):
        """
        Kontroluje vzdálenost pavouka od hráče. Pokud je hráč blízko, pavouk se "naštve",
        změní obrázek a zrychlí, aby ho pronásledoval.
        :param player_rect: Obdélník (rect) hráče pro výpočet vzdálenosti.
        """
        vzdalenost_x = player_rect.centerx - self.rect.centerx
        vzdalenost_y = player_rect.centery - self.rect.centery
        vzdalenost = (vzdalenost_x ** 2 + vzdalenost_y ** 2) ** 0.5

        if vzdalenost < self.pavouk_postava_vzdalenost:
            self.image = self.image_angry
            self.speed = self.angry_speed * self.rychlostni_koeficient
            self.is_angry = True
        else:
            self.image = self.original_image
            self.speed = self.original_speed * self.rychlostni_koeficient
            self.is_angry = False

    def update(self, player_rect):
        """
        Aktualizuje stav pavouka v každém snímku.
        Volá metody pro pohyb a kontrolu přiblížení k hráči.
        :param player_rect: Obdélník (rect) hráče, nutný pro pohyb a přiblížení.
        """
        # Pohybuje pavoukem a kontroluje přiblížení k hráči
        # Používám 'player.direction' jako jednoduchou podmínku pro začátek pohybu pavouků
        # až po prvním pohybu hráče.
        # POZNÁMKA: player.direction musíte získat z instance hráče, např. předáním jako parametr update metody Pavouka.
        # V Game třídě se to děje takto: self.pavouci_group.update(player.rect)
        # ale kontrola player.direction se musí přidat, pokud je potřeba.
        # Pro zjednodušení jsem odstranil přímou závislost na player.direction v Pavouk.update,
        # pokud chcete, aby se pavouci začali pohybovat až po prvním pohybu hráče,
        # musíte tuto logiku implementovat v Game.update nebo předat player.direction do Pavouka.
        self.move(player_rect)
        self.priblizeni(player_rect)