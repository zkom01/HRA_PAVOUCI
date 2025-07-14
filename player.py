import pygame
import settings # Pro přístup k nastavení

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name, rychlost):
        super().__init__()
        self.direction = None
        self.original_image = pygame.image.load(f"media/img/{image_name}").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (x, y)
        self.mezera_mezi_sudy = 6
        self.had_segmenty = []
        self.pozice_hlavy = []
        self.rychlostni_koeficient = 1.0
        self.speed = rychlost

        self.imunita_aktivni = False
        self.imunita_start_cas = 0
        self.doba_imunity = 2000

    def pridej_segment(self, segment):
        self.had_segmenty.append(segment)

    def stisknute_klavesy_player(self, udalost):
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
        Aktualizuje pozici hráče na základě jeho směru a rychlosti.
        Zajišťuje, aby hráč "prošel" skrz okraje obrazovky (warp efekt)
        s ohledem na horní panel.
        """
        # Pohyb hráče na základě aktuálního směru
        if self.direction == 'left':
            self.rect.x -= self.speed * self.rychlostni_koeficient
        elif self.direction == 'right':
            self.rect.x += self.speed * self.rychlostni_koeficient
        elif self.direction == 'up':
            self.rect.y -= self.speed * self.rychlostni_koeficient
        elif self.direction == 'down':
            self.rect.y += self.speed * self.rychlostni_koeficient

        # Zajištění "warp" efektu (projití skrz okraj obrazovky a objevení se na protější straně)
        # S ohledem na horní panel (settings.VYSKA_HORNÍHO_PANELU)
        if self.rect.bottom < settings.VYSKA_HORNIHO_PANELU:  # Pokud je hráč nad horním panelem (mimo herní plochu)
            self.rect.top = settings.SCREEN_HEIGHT - 20  # Objeví se dole
        elif self.rect.top > settings.SCREEN_HEIGHT - 20:  # Pokud je hráč pod spodním okrajem
            self.rect.bottom = settings.VYSKA_HORNIHO_PANELU + 20  # Objeví se nahoře (pod panelem)

        if self.rect.right < 5:  # Pokud je hráč vlevo mimo obrazovku
            self.rect.left = settings.SCREEN_WIDTH - 5  # Objeví se vpravo
        elif self.rect.left > settings.SCREEN_WIDTH - 5:  # Pokud je hráč vpravo mimo obrazovku
            self.rect.right = 5  # Objeví se vlevo

        # Ukládá pozici hlavy hráče do historie pro pohyb segmentů hada
        if self.direction:  # Pouze pokud se hráč pohybuje (tedy pokud direction není None)
            self.pozice_hlavy.insert(0, (self.rect.centerx, self.rect.centery))

        # Omezuje délku historie pozic hlavy, aby se předešlo nekonečnému růstu seznamu
        # Délka je závislá na počtu segmentů a mezeře mezi nimi
        required_length = (len(self.had_segmenty) + 1) * self.mezera_mezi_sudy + 10  # +10 pro malou rezervu
        if len(self.pozice_hlavy) > required_length:
            self.pozice_hlavy.pop()  # Odstraní nejstarší pozici z historie

    def update_segmenty_hada(self):
        if self.had_segmenty:
            if not self.pozice_hlavy:
                return

            for i, segment in enumerate(self.had_segmenty):
                history_index = (i + 1) * self.mezera_mezi_sudy
                history_index = min(history_index, len(self.pozice_hlavy) - 1)

                if history_index < 0:
                    history_index = 0

                target_x, target_y = self.pozice_hlavy[history_index]
                segment.rect.center = (target_x, target_y)

    def aktivovat_imunitu(self):
        self.imunita_aktivni = True
        self.imunita_start_cas = pygame.time.get_ticks()

    def kontrola_imunity(self):
        if self.imunita_aktivni:
            aktualni_herni_cas = pygame.time.get_ticks()
            if aktualni_herni_cas - self.imunita_start_cas > self.doba_imunity:
                self.imunita_aktivni = False
                self.image.set_alpha(255)
            else:
                if (aktualni_herni_cas // 200) % 2 == 0:
                    self.image.set_alpha(255)
                else:
                    self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.move()
        self.update_segmenty_hada()
        self.kontrola_imunity()