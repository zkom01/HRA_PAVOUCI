"""
Modul Player obsahuje třídu Player, která reprezentuje ovladatelného hráče ve hře.
Hráč se pohybuje po obrazovce, sbírá sudy a má dočasnou imunitu.
"""

import pygame
import settings # Pro přístup k nastavení

class Player(pygame.sprite.Sprite):
    """
    Třída reprezentující hráče ve hře.

    Hráč je spritový objekt, který se může pohybovat, sbírat segmenty (sudy),
    a má mechaniku imunity po zásahu.

    Atributy:
        direction (str): Aktuální směr pohybu hráče ('left', 'right', 'up', 'down' nebo None).
        original_image (pygame.Surface): Původní obrázek hráče před úpravami.
        image (pygame.Surface): Aktuální obrázek hráče (může se měnit kvůli efektu imunity).
        rect (pygame.Rect): Obdélník definující pozici a rozměry hráče.
        mask (pygame.mask.Mask): Maska pro pixel-perfect detekci kolizí.
        mezera_mezi_sudy (int): Vzdálenost mezi segmenty hada (sudy).
        had_segmenty (list): Seznam objektů Sud, které tvoří tělo "hada".
        pozice_hlavy (list): Historie pozic hlavy hráče, slouží pro sledování segmentů.
        rychlostni_koeficient (float): Násobitel rychlosti hráče, mění se v průběhu hry.
        speed (int): Základní rychlost pohybu hráče (pixely za snímek).
        imunita_aktivni (bool): True, pokud je hráč aktuálně imunní vůči poškození.
        imunita_start_cas (int): Čas v milisekundách, kdy imunita začala.
        doba_imunity (int): Doba trvání imunity v milisekundách.
    """
    def __init__(self, x: int, y: int, image_name: str, rychlost: int):
        """
        Inicializuje novou instanci hráče.

        Args:
            x (int): Počáteční X souřadnice středu hráče.
            y (int): Počáteční Y souřadnice středu hráče.
            image_name (str): Název souboru obrázku hráče (např. "player.png").
            rychlost (int): Základní rychlost pohybu hráče.
        """
        super().__init__()
        self.direction = None # Počáteční směr pohybu
        # Načtení a příprava obrázku hráče. convert_alpha() pro průhlednost.
        self.original_image = pygame.image.load(settings.PLAYER_IMAGE).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) # Maska pro přesné kolize
        self.rect.center = (x, y) # Nastavení počáteční pozice

        self.mezera_mezi_sudy = settings.MEZERA_MEZI_SUDY # Vzdálenost mezi segmenty hada
        self.had_segmenty = [] # Seznam objektů Sud, které tvoří tělo "hada"
        self.pozice_hlavy = [] # Historie pozic hlavy pro pohyb segmentů

        self.rychlostni_koeficient = settings.RYCHLOST_1 # Výchozí rychlostní koeficient
        self.speed = rychlost # Základní rychlost hráče

        # Proměnné pro systém imunity
        self.imunita_aktivni = False
        self.imunita_start_cas = 0
        self.doba_imunity = settings.DOBA_IMUNITY

    def pridej_segment(self, segment: pygame.sprite.Sprite):
        """
        Přidá nový segment (sud) k tělu hada.

        Args:
            segment (pygame.sprite.Sprite): Objekt sudu, který se má přidat.
        """
        self.had_segmenty.append(segment)

    def stisknute_klavesy_player(self, udalost: pygame.event.Event):
        """
        Zpracovává události stisku kláves pro ovládání směru hráče.

        Args:
            udalost (pygame.event.Event): Událost Pygame (typu KEYDOWN).
        """
        if udalost.key == pygame.K_LEFT or udalost.key == pygame.K_a:
            self.direction = 'left'
        elif udalost.key == pygame.K_RIGHT or udalost.key == pygame.K_d:
            self.direction = 'right'
        elif udalost.key == pygame.K_UP or udalost.key == pygame.K_w:
            self.direction = 'up'
        elif udalost.key == pygame.K_DOWN or udalost.key == pygame.K_s:
            self.direction = 'down'

    def move(self):
        """
        Aktualizuje pozici hráče na základě jeho směru a aktuální rychlosti.
        Zajišťuje "warp" efekt (projití skrz okraje obrazovky a objevení se na protější straně)
        s ohledem na horní panel.
        """
        # Pohyb hráče na základě aktuálního směru a rychlosti s koeficientem
        if self.direction == 'left':
            self.rect.x -= self.speed * self.rychlostni_koeficient
        elif self.direction == 'right':
            self.rect.x += self.speed * self.rychlostni_koeficient
        elif self.direction == 'up':
            self.rect.y -= self.speed * self.rychlostni_koeficient
        elif self.direction == 'down':
            self.rect.y += self.speed * self.rychlostni_koeficient

        # Zajištění "warp" efektu (projití skrz okraj obrazovky a objevení se na protější straně)
        # S ohledem na horní panel (settings.VYSKA_HORNIHO_PANELU)
        # Vertikální warp
        if self.rect.bottom < settings.VYSKA_HORNIHO_PANELU:  # Pokud hráč projede horním okrajem herní plochy
            self.rect.top = settings.SCREEN_HEIGHT - 20   # Objeví se dole (s malým odsazením od spodního okraje)
        elif self.rect.top > settings.SCREEN_HEIGHT - 20:  # Pokud hráč projede spodním okrajem herní plochy
            self.rect.bottom = settings.VYSKA_HORNIHO_PANELU + 20  # Objeví se nahoře (s malým odsazením pod horním panelem)

        # Horizontální warp
        if self.rect.right < 5:  # Pokud hráč projede levým okrajem obrazovky
            self.rect.left = settings.SCREEN_WIDTH - 5  # Objeví se vpravo (s malým odsazením od pravého okraje)
        elif self.rect.left > settings.SCREEN_WIDTH - 5:  # Pokud hráč projede pravým okrajem obrazovky
            self.rect.right = 5  # Objeví se vlevo (s malým odsazením od levého okraje)

        # Ukládá aktuální pozici středu hlavy hráče do historie.
        # To je klíčové pro správné umístění segmentů hada.
        if self.direction:  # Pozice se ukládá pouze, pokud se hráč pohybuje
            self.pozice_hlavy.insert(0, (self.rect.centerx, self.rect.centery))

        # Omezuje délku historie pozic hlavy, aby se předešlo nekonečnému růstu seznamu
        # a optimalizovala se paměť. Délka je závislá na počtu segmentů a mezeře.
        # +10 pro malou rezervu, aby segmenty nezmizely příliš brzy.
        required_length = (len(self.had_segmenty) + 1) * self.mezera_mezi_sudy + 10
        if len(self.pozice_hlavy) > required_length:
            self.pozice_hlavy.pop()  # Odstraní nejstarší pozici z historie

    def update_segmenty_hada(self):
        """
        Aktualizuje pozice všech segmentů hada (sudu) tak, aby sledovaly trajektorii hráče.
        Každý segment se umístí na pozici z historie pozic hlavy, s odstupem definovaným
        'mezera_mezi_sudy'.
        """
        if self.had_segmenty: # Pokud hráč má nějaké sudy
            if not self.pozice_hlavy: # Pokud není k dispozici žádná historie pozic, nic nedělej
                return

            for i, segment in enumerate(self.had_segmenty):
                # Vypočítá index v historii pozic, na který se má daný segment umístit.
                # Čím dál je segment od hlavy, tím starší pozici potřebuje.
                history_index = (i + 1) * self.mezera_mezi_sudy
                # Zajišťuje, aby index nepřekročil velikost seznamu historie.
                history_index = min(history_index, len(self.pozice_hlavy) - 1)

                # Bezpečnostní kontrola pro případ, že historie je příliš krátká.
                if history_index < 0:
                    history_index = 0

                # Nastaví pozici segmentu na pozici z historie.
                target_x, target_y = self.pozice_hlavy[history_index]
                segment.rect.center = (target_x, target_y)

    def aktivovat_imunitu(self):
        """
        Aktivuje stav imunity pro hráče. Hráč je dočasně chráněn před poškozením.
        Zaznamená čas začátku imunity.
        """
        self.imunita_aktivni = True
        self.imunita_start_cas = pygame.time.get_ticks() # Zaznamená aktuální herní čas v ms

    def kontrola_imunity(self):
        """
        Kontroluje, zda je imunita hráče stále aktivní.
        Pokud ano, mění průhlednost obrázku hráče pro vizuální indikaci.
        Po vypršení doby imunity imunitu deaktivuje a obnoví plnou průhlednost.
        """
        if self.imunita_aktivni:
            aktualni_herni_cas = pygame.time.get_ticks()
            # Pokud uplynula doba imunity, deaktivuje ji.
            if aktualni_herni_cas - self.imunita_start_cas > self.doba_imunity:
                self.imunita_aktivni = False
                self.image.set_alpha(255) # Obnoví plnou průhlednost (100% viditelnost)
            else:
                # Blikající efekt pro vizuální indikaci imunity.
                # Mění průhlednost každých 200 ms.
                if (aktualni_herni_cas // 200) % 2 == 0:
                    self.image.set_alpha(255) # Plná viditelnost
                else:
                    self.image.set_alpha(100) # Částečně průhledné
        else:
            self.image.set_alpha(255) # Zajistí plnou viditelnost, pokud imunita není aktivní

    def update(self):
        """
        Aktualizuje stav hráče v každém herním snímku.
        Volá metody pro pohyb, aktualizaci segmentů a kontrolu imunity.
        Tuto metodu by měla volat herní smyčka.
        """
        self.move() # Pohyb hráče
        self.update_segmenty_hada() # Aktualizace pozic sudů
        self.kontrola_imunity() # Kontrola a vizuální indikace imunity
