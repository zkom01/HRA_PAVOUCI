"""
Modul Spider obsahuje třídu Pavouk, která reprezentuje nepřátelské pavouky ve hře.
Pavouci se pohybují po herní ploše, reagují na blízkost hráče změnou chování (pronásledování)
a vizuálního vzhledu.
"""

import pygame
import random
import settings # Importujeme modul settings pro přístup k nastavení

class Pavouk(pygame.sprite.Sprite):
    """
    Třída Pavouk (Spider) reprezentuje nepřátelský objekt ve hře.

    Pavouci se pohybují po obrazovce, mohou měnit směr náhodně,
    nebo pronásledovat hráče, pokud je v jejich blízkosti.
    Mají dva vizuální stavy: klidný a "naštvaný".

    Atributy:
        original_image (pygame.Surface): Původní obrázek pavouka pro klidný stav.
        image (pygame.Surface): Aktuální obrázek pavouka (mění se mezi klidným a "naštvaným").
        rect (pygame.Rect): Obdélník definující pozici a rozměry pavouka.
        mask (pygame.mask.Mask): Maska pro pixel-perfect detekci kolizí.
        image_angry (pygame.Surface): Obrázek pavouka pro "naštvaný" stav.
        original_speed (int): Základní rychlost pavouka v klidovém stavu.
        angry_speed (float): Rychlost pavouka, když je "naštvaný" (násobek original_speed).
        speed (float): Aktuální rychlost pavouka (mění se podle stavu klidný/angry).
        rychlostni_koeficient (float): Globální koeficient rychlosti, ovlivněný stavem hry.
        direct_x (int): Směr pohybu pavouka po ose X (-1: doleva, 0: žádný, 1: doprava).
        direct_y (int): Směr pohybu pavouka po ose Y (-1: nahoru, 0: žádný, 1: dolů).
        pavouk_postava_vzdalenost (int): Maximální vzdálenost, pod kterou se pavouk "naštve".
        change_dir_timer (int): Počítadlo snímků pro určení, kdy náhodně změnit směr v klidovém stavu.
        is_angry (bool): True, pokud je pavouk "naštvaný" a pronásleduje hráče.
    """

    def __init__(self, x: int, y: int, image_name: str, image_angry_name: str, rychlost: int):
        """
        Konstruktor třídy Pavouk.

        Args:
            x (int): Počáteční X souřadnice pavouka.
            y (int): Počáteční Y souřadnice pavouka.
            image_name (str): Název souboru obrázku pro normální (klidný) stav pavouka.
            image_angry_name (str): Název souboru obrázku pro "naštvaný" stav pavouka.
            rychlost (int): Základní rychlost pavouka.
        """
        super().__init__()  # Volá konstruktor rodičovské třídy pygame.sprite.Sprite

        # Načtení a nastavení normálního obrázku pavouka
        self.original_image = pygame.image.load(f"media/img/{image_name}").convert_alpha()
        self.image = self.original_image  # Aktuální obrázek pavouka
        self.rect = self.image.get_rect()  # Získá obdélník z obrázku
        self.rect.topleft = (x, y)  # Nastaví počáteční pozici pavouka
        self.mask = pygame.mask.from_surface(self.image)  # Maska pro pixel-perfect kolize

        # Načtení a příprava obrázku "naštvaného" pavouka
        self.image_angry = pygame.image.load(f"media/img/{image_angry_name}").convert_alpha()

        # Nastavení rychlostí pavouka
        self.original_speed = rychlost  # Původní (klidná) rychlost pavouka
        # Zvýšená rychlost, když je pavouk "naštvaný", násobená globálním koeficientem
        self.angry_speed = rychlost * settings.ANGRY_SPEED_MULTIPLIER # Použijte dedikovanou konstantu pro násobitel
        self.speed = float(self.original_speed) # Aktuální rychlost pavouka, typ float pro přesnější pohyb
        self.rychlostni_koeficient = settings.RYCHLOST_1 # Globální koeficient z nastavení

        # Nastavení počátečního náhodného směru pohybu
        self.direct_x, self.direct_y = self.novy_smer()
        self.pavouk_postava_vzdalenost = settings.ANGRY_VZDALENOST # Vzdálenost (v pixelech), pod kterou se pavouk "naštve"
        self.change_dir_timer = 0  # Časovač pro náhodnou změnu směru pavouka v klidovém stavu
        self.is_angry = False  # Logická proměnná, zda je pavouk "naštvaný" a pronásleduje hráče

    @staticmethod
    def novy_smer() -> tuple[int, int]:
        """
        Statická metoda, která vrací náhodný směr pohybu (nahoru, dolů, doleva, doprava)
        pro klidový stav pavouka.

        Returns:
            tuple[int, int]: Tuple (dx, dy) představující změnu souřadnic pro daný směr.
                             -1 pro pohyb doleva/nahoru, 1 pro pohyb doprava/dolů, 0 pro žádný pohyb.
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
        # Měl by vždy vrátit hodnotu díky random.choice, ale pro jistotu fallback.
        return 0, 0

    def move(self, player_rect: pygame.Rect):
        """
        Aktualizuje pozici pavouka na základě jeho aktuální rychlosti a směru.
        Zajišťuje, aby pavouk zůstal v rámci hranic herní obrazovky (včetně horního panelu).
        Pokud je pavouk "naštvaný" (self.is_angry je True), směřuje k hráči.
        Jinak se pohybuje náhodně a občas změní směr.

        Args:
            player_rect (pygame.Rect): Obdélník (rect) hráče pro cílení pohybu v "naštvaném" stavu.
        """
        if self.is_angry:
            # V "naštvaném" stavu se pavouk přímo snaží dosáhnout hráče.
            # Vypočítá se delta X a Y k hráči.
            delta_x = player_rect.centerx - self.rect.centerx
            delta_y = player_rect.centery - self.rect.centery

            # Pavouk se pohybuje primárně po delší ose k hráči, aby se vyhnul diagonálnímu pohybu,
            # který by mohl být méně předvídatelný nebo působit nepřirozeně.
            if abs(delta_x) > abs(delta_y):
                self.direct_x = 1 if delta_x > 0 else -1
                self.direct_y = 0 # Pohyb jen horizontálně
            else:
                self.direct_y = 1 if delta_y > 0 else -1
                self.direct_x = 0 # Pohyb jen vertikálně
        else:
            # V klidovém stavu pavouk náhodně mění směr.
            self.change_dir_timer += 1
            # Náhodná doba mezi změnami směru (60 až 120 snímků).
            if self.change_dir_timer >= random.randint(60, 120):
                self.change_dir_timer = 0
                self.direct_x, self.direct_y = self.novy_smer() # Získání nového náhodného směru

        # Aplikace pohybu na pozici pavouka, s ohledem na aktuální rychlost a herní koeficient.
        self.rect.x += self.speed * self.rychlostni_koeficient * self.direct_x
        self.rect.y += self.speed * self.rychlostni_koeficient * self.direct_y

        # Kontrola hranic obrazovky: pavouk se neodrazí, ale je "přilepen" k hranici a změní směr.
        # Horizontální hranice
        if self.rect.left < 0:
            self.rect.left = 0
            self.direct_x, self.direct_y = self.novy_smer()
        elif self.rect.right > settings.SCREEN_WIDTH:
            self.rect.right = settings.SCREEN_WIDTH
            self.direct_x, self.direct_y = self.novy_smer()

        # Vertikální hranice (respektuje horní panel)
        if self.rect.top < settings.VYSKA_HORNIHO_PANELU:
            self.rect.top = settings.VYSKA_HORNIHO_PANELU
            self.direct_x, self.direct_y = self.novy_smer()
        elif self.rect.bottom > settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT
            self.direct_x, self.direct_y = self.novy_smer()

    def priblizeni(self, player_rect: pygame.Rect):
        """
        Kontroluje vzdálenost pavouka od hráče.
        Pokud je hráč blízko (v rámci `pavouk_postava_vzdalenost`), pavouk se "naštve",
        změní svůj vizuální vzhled na `image_angry` a zrychlí, aby ho pronásledoval.
        Jinak se vrátí do klidového stavu s normálním obrázkem a rychlostí.

        Args:
            player_rect (pygame.Rect): Obdélník (rect) hráče pro výpočet vzdálenosti.
        """
        # Výpočet Euklidovské vzdálenosti mezi středem pavouka a středem hráče.
        vzdalenost_x = player_rect.centerx - self.rect.centerx
        vzdalenost_y = player_rect.centery - self.rect.centery
        vzdalenost = (vzdalenost_x ** 2 + vzdalenost_y ** 2) ** 0.5

        if vzdalenost < self.pavouk_postava_vzdalenost:
            # Pavouk je blízko hráče, přejde do "naštvaného" stavu.
            self.image = self.image_angry
            self.speed = self.angry_speed * self.rychlostni_koeficient
            self.is_angry = True
        else:
            # Pavouk je daleko od hráče, vrátí se do klidového stavu.
            self.image = self.original_image
            self.speed = self.original_speed * self.rychlostni_koeficient
            self.is_angry = False

    def update(self, player_rect: pygame.Rect, player_direction: str | None):
        """
        Aktualizuje stav pavouka v každém herním snímku.
        Tato metoda je volána herní smyčkou.
        Pavouci se hýbou a kontrolují blízkost hráče pouze, když se hýbe i hráč.

        Args:
            player_rect (pygame.Rect): Obdélník (rect) hráče, nutný pro pohyb a kontrolu přiblížení.
            player_direction (str | None): Směr pohybu hráče. Pavouci se hýbou jen tehdy,
                                           když se hýbe hráč (jeho direction není None).
        """
        # Pavouci se hýbou a reagují na hráče pouze, když se hráč skutečně pohybuje.
        if player_direction:
            self.move(player_rect) # Aktualizuje pozici pavouka
            self.priblizeni(player_rect) # Kontroluje a mění stav pavouka na základě vzdálenosti od hráče
