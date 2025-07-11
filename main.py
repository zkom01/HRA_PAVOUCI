import pygame  # Importuje knihovnu Pygame pro tvorbu her
import random  # Importuje modul random pro generování náhodných čísel

from screeninfo import get_monitors

########  další nápady - ukázat čas, dodělat konec hry a restart

# --- Inicializace hry ---
pygame.init()  # Inicializuje všechny moduly Pygame. Toto je nutné spustit před použitím jakékoli funkce Pygame.

# --- Nastavení obrazovky ---
# Získání rozměrů primárního monitoru
monitors = get_monitors()
monitor_width = monitors[0].width
monitor_height = monitors[0].height

screen_width = 1400  # Šířka okna hry v pixelech
screen_height = 700  # Výška okna hry v pixelech
original_screen_width = screen_width
original_screen_height = screen_height
screen = pygame.display.set_mode((screen_width, screen_height))  # Vytvoří herní okno s definovanou šířkou a výškou
pygame.display.set_caption("EDOVA_HRA")  # Nastaví titulek okna hry
screen_color = (0, 0, 0)  # Nastaví barvu pozadí obrazovky na černou (RGB hodnota)
ikona_image = pygame.image.load("media/img/robot.png")  # Načte obrázek ikony zadanou cestou
pygame.display.set_icon(ikona_image)  # Nastaví načtený obrázek jako ikonu okna hry

# --- Nastavení herních parametrů ---
vyska_horniho_panelu = 64  # Výška horního panelu (např. pro skóre, životy)
fps = 60  # Počet snímků za sekundu (Frame Per Second) - určuje plynulost hry
clock = pygame.time.Clock()  # Vytvoří objekt Clock pro řízení rychlosti hry (FPS)


# --- Třídy (Classes) ---
class Game:
    """
    Třída Game (Hra) spravuje hlavní logiku hry, jako je skóre, životy,
    kolize a vykreslování herních prvků na obrazovku. Také řídí stavy hry,
    např. pauzu.
    """

    def __init__(self, hrac_group, jidla_group, pavouci_group, sudy_group, pavouk_max_obj, pavouk_tery_obj,
                 pavouk_niky_obj, pavouk_eda_obj, pavouk_hana_obj):
        """
        Konstruktor třídy Game.
        :param hrac_group: Skupina spriteů pro hráče.
        :param jidla_group: Skupina spriteů pro jídlo.
        :param pavouci_group: Skupina spriteů pro pavouky (nepřátele).
        :param sudy_group: Skupina spriteů pro sudy (segmenty hada hráče).
        :param pavouk_max_obj: Objekt pavouka Max.
        :param pavouk_tery_obj: Objekt pavouka Tery.
        :param pavouk_niky_obj: Objekt pavouka Niky.
        """
        self.hrac_group = hrac_group
        self.jidla_group = jidla_group
        self.pavouci_group = pavouci_group
        self.sudy_group = sudy_group
        self.zivoty = 3  # Počáteční počet životů hráče
        self.score = 0  # Počáteční skóre hráče
        self.rychlost = 1
        self.kapky_od_posledniho_sudu = 0  # Počet sebraných "kapek" (jídla) od posledního přidání sudu
        self.pocet_kapek_na_sud = 3  # Kolik kapek (jídla) je potřeba sebrat pro přidání nového sudu
        self.rychlost_played_2 = False
        self.rychlost_played_5 = False
        self.rychlost_played_8 = False

        # Odkazy na konkrétní objekty pavouků pro jejich přidávání/odebírání
        self.pavouk_max = pavouk_max_obj
        self.pavouk_tery = pavouk_tery_obj
        self.pavouk_niky = pavouk_niky_obj
        self.pavouk_eda = pavouk_eda_obj
        self.pavouk_hana = pavouk_hana_obj

        # Logické proměnné pro sledování, zda byli pavouci přidáni
        self.tery_added = False
        self.niky_added = False
        self.max_added = False
        self.eda_added = False
        self.hana_added = False

        # Stav pauzy hry
        self.game_paused = False
        self.lets_continue = True  # Logická proměnná pro hlavní herní smyčku; dokud je True, hra běží
        self.is_fullscreen = False

        # Zvuky + Hudba v pozadí
        pygame.mixer.music.load("media/sounds/Desert_Nomad.ogg")  # Načte hudební soubor
        pygame.mixer.music.play(-1)  # Přehrává hudbu ve smyčce (-1)
        pygame.mixer.music.set_volume(0.3)  # Hlasitost
        self.zvuk_kapky = pygame.mixer.Sound("media/sounds/olej_sound.ogg")
        self.zvuk_kapky.set_volume(0.2)
        self.kousanec_sound = pygame.mixer.Sound("media/sounds/kousanec.ogg")
        self.kousanec_sound.set_volume(0.2)
        self.rychlost_sound = pygame.mixer.Sound("media/sounds/rychlost.ogg")

        # Fonty pro text ve hře
            # Načte font a nastaví velikost
        self.font_robot = pygame.font.Font("media/fonts/Super Rocky by All Super Font.ttf",50)
            # Větší font pro "PAUZA"
        self.font_robot_big = pygame.font.Font("media/fonts/Super Rocky by All Super Font.ttf",80)
            # Okraj kolem písma "PAUZA"
        self.font_robot_big_1 = pygame.font.Font("media/fonts/Super Rocky by All Super Font.ttf",90)
            # Menší font
        self.font_robot_small = pygame.font.Font("media/fonts/Super Rocky by All Super Font.ttf", 25)

        # Barvy používané při vykreslování textu a UI
        self.barva_textu = (50, 103, 6)  # Tmavě zelená barva pro text
        self.white = (255, 255, 255)  # Bílá barva
        self.main_color = screen_color  # Používá barvu pozadí obrazovky (černá) pro pozadí horního panelu
        self.barva_textu_nabidky = self.barva_textu
        self.barva_pod_text_nabidky = screen_color

        # Předpřipravíme text "PAUZA" pro efektivnější vykreslování
        self.pause_text0 = self.font_robot_big_1.render("PAUZA", True, self.main_color)
        self.pause_text = self.font_robot_big.render("PAUZA", True, self.barva_textu)
        self.pause_text0_rect = self.pause_text.get_rect()
        self.pause_text_rect = self.pause_text.get_rect()
        self.pause_text_rect.center = ((screen_width // 2) + 13, (screen_height // 2) + 7)
        self.pause_text0_rect.center = (screen_width // 2, screen_height // 2)

        # Nabídka při PAUSE
        self.konec_text = self.font_robot_big_1.render("KONEC HRY", True, self.barva_pod_text_nabidky)
        self.konec_text_rect = self.konec_text.get_rect(center=(screen_width - 400, (screen_height // 2)))
        self.konec_text0 = self.font_robot_big.render("KONEC HRY", True, self.barva_textu)
        self.konec_text0_rect = self.konec_text0.get_rect(center=(screen_width - 400, screen_height // 2))

    @staticmethod
    def kresleni_pozadi():
        """
        Vykresluje obrázek pozadí hry.
        """
        # Načte obrázek pozadí s průhledností
        pozadi_image = pygame.image.load("media/img/pozadi.png").convert_alpha()
        # Změní velikost obrázku pozadí
        pozadi_image = pygame.transform.scale(pozadi_image, (screen_width, screen_height - vyska_horniho_panelu))
        # Získá obdélník (rect) obrázku a umístí ho pod horní panel
        pozadi_image_rect = pozadi_image.get_rect(topleft=(0, vyska_horniho_panelu))
        screen.blit(pozadi_image, pozadi_image_rect)  # Nakreslí pozadí na obrazovku

    def kresleni_horniho_panelu(self, score, lives, speed):
        """
        Vykresluje horní panel s nadpisem, skóre, sudy a životy + menu při PAUSE.
        Tato metoda je volána v každém snímku a měla by se vykreslovat nad herními prvky.
        :param score: Aktuální skóre hry.
        :param lives: Aktuální počet životů hráče.
        :param speed: Aktuální skóre hry.
        """
        pocet_sudu = len(player.had_segmenty)  # Získá aktuální počet sudů (segmentů hada hráče)

        # Horní pruh s nadpisem a obdélníkem pozadí
            # Vykreslí černý obdélník pro horní panel
        pygame.draw.rect(screen, self.main_color,(0, 0, screen_width, vyska_horniho_panelu))
            # Vykreslí bílou čáru oddělující panel od herní plochy
        pygame.draw.line(screen, self.white, (0, vyska_horniho_panelu),(screen_width, vyska_horniho_panelu))

        # --- Nadpis a texty ---
            # Vykreslí text nadpisu
        nadpis_text = self.font_robot.render("PAVOUCI_KOMARKOVI", True, self.barva_textu)
            # Vycentruje nadpis v horním panelu
        nadpis_text_rect = nadpis_text.get_rect(center=(screen_width // 2, vyska_horniho_panelu // 2))

        # Zobrazení skóre
        score_text = self.font_robot_small.render(f"POCET_KAPEK: {score}", True, self.barva_textu)  # Vykreslí text skóre
        score_text_rect = score_text.get_rect(topleft=(10, 0))  # Umístí text skóre do levého horního rohu panelu

        # Zobrazení počtu sudů
        barel_text = self.font_robot_small.render(f"POCET_SUDU: {pocet_sudu}", True, self.barva_textu)  # Vykreslí text počtu sudů
        barel_text_rect = barel_text.get_rect(topleft=(10, 25))  # Umístí text počtu sudů pod text skóre

        # Zobrazení počtu sudů
        rychlost_text = self.font_robot.render(f"RYCHLOST HRY: {speed}", True,self.barva_textu)  # Vykreslí text počtu sudů
        rychlost_text_rect = rychlost_text.get_rect(center=(450, vyska_horniho_panelu // 2))  # Umístí text počtu sudů pod text skóre

        # Zobrazení životů
        lives_text = self.font_robot.render(f"ZIVOTY: {lives}", True, self.barva_textu)  # Vykreslí text životů
        lives_text_rect = lives_text.get_rect(topright=(screen_width - 10, 0))  # Umístí text životů do pravého horního rohu panelu

        # Vykreslení do screenu (blitting)
        screen.blit(lives_text, lives_text_rect)  # Nakreslí životy na obrazovku
        screen.blit(barel_text, barel_text_rect)  # Nakreslí počet sudů na obrazovku
        screen.blit(rychlost_text, rychlost_text_rect) # Nakreslí aktuální rychlost hry
        screen.blit(nadpis_text, nadpis_text_rect)  # Nakreslí nadpis na obrazovku
        screen.blit(score_text, score_text_rect)  # Nakreslí skóre na obrazovku
        if self.game_paused:
            screen.blit(self.konec_text, self.konec_text_rect)
            screen.blit(self.konec_text0, self.konec_text0_rect)

    def update_stav_is_angry(self):
        """
        Nastaví barvu pozadí na červenou, pokud je JAKÝKOLI pavouk "angry".
        Jinak ji nastaví na původní barvu obrazovky.
        """
        any_spider_angry = False
        for jeden_pavouk in self.pavouci_group:
            if jeden_pavouk.is_angry:
                any_spider_angry = True
                break  # Jakmile najdeme jednoho "angry" pavouka, můžeme smyčku ukončit

        if any_spider_angry:
            self.main_color = (128, 0, 0)  # Červená
        else:
            self.main_color = screen_color  # Původní barva (černá)

    def update_rychlosti(self):
        """
        Zrychluje hráče i pavouky podle skóre:
        - při skóre >= 6 se násobí rychlost ×1.3
        - při skóre >= 12 se násobí rychlost ×5
        Zároveň se při skóre 6 a 12 spustí zvuk.
        """
        velikost = len(player.had_segmenty)

        if velikost >= 8 and not self.rychlost_played_8:
            self.rychlost_sound.play()
            self.rychlost_played_8 = True
            player.rychlostni_koeficient = 1.5
            player.mezera_mezi_sudy = 4
            self.rychlost = 4

        if velikost >= 5 and not self.rychlost_played_5:
            self.rychlost_sound.play()
            self.rychlost_played_5 = True
            player.rychlostni_koeficient = 1.4
            player.mezera_mezi_sudy = 4
            self.rychlost = 3

        if velikost >= 2 and not self.rychlost_played_2:
            self.rychlost_sound.play()
            self.rychlost_played_2 = True
            player.rychlostni_koeficient = 1.2
            player.mezera_mezi_sudy = 5
            self.rychlost = 2

        for pavouk in self.pavouci_group:
            pavouk.rychlostni_koeficient = player.rychlostni_koeficient

    def prida_odebere_pavouka(self):
        """
        Přidává nebo odebírá pavouky podle počtu sudů hráče.
        Pokud hráč dosáhne určitého počtu sudů, přidá se nový pavouk a aktivuje se imunita.
        """
        # Pavouk Max
        if len(player.had_segmenty) >= 0:
            if not self.max_added:
                self.pavouci_group.add(self.pavouk_max)
                self.pavouk_max.rychlostni_koeficient = player.rychlostni_koeficient
                player.aktivovat_imunitu()  # Aktivuje imunitu hráče
                self.max_added = True

        # elif len(player.had_segmenty) == 0:
        #     if self.pavouk_max in self.pavouci_group:
        #         self.pavouci_group.remove(self.pavouk_max)
        #         self.max_added = False

        # Pavouk Tery
        if len(player.had_segmenty) >= 2:
            if not self.tery_added:
                self.pavouci_group.add(self.pavouk_tery)
                self.pavouk_tery.rychlostni_koeficient = player.rychlostni_koeficient
                player.aktivovat_imunitu()  # Aktivuje imunitu hráče
                self.tery_added = True

        # elif len(player.had_segmenty) < 2:
        #     if self.pavouk_tery in self.pavouci_group:
        #         self.pavouci_group.remove(self.pavouk_tery)
        #         self.tery_added = False

        # Pavouk Niky
        if len(player.had_segmenty) >= 3:
            if not self.niky_added:
                self.pavouci_group.add(self.pavouk_niky)
                self.pavouk_niky.rychlostni_koeficient = player.rychlostni_koeficient
                player.aktivovat_imunitu()  # Aktivuje imunitu hráče
                self.niky_added = True

        # elif len(player.had_segmenty) < 4:
        #     if self.pavouk_niky in self.pavouci_group:
        #         self.pavouci_group.remove(self.pavouk_niky)
        #         self.niky_added = False

        # Pavouk Eda
        if len(player.had_segmenty) >= 5:
            if not self.eda_added:
                self.pavouci_group.add(self.pavouk_eda)
                self.pavouk_eda.rychlostni_koeficient = player.rychlostni_koeficient
                player.aktivovat_imunitu()
                self.eda_added = True

        # elif len(player.had_segmenty) < 5:
        #     if self.pavouk_eda in self.pavouci_group:
        #         self.pavouci_group.remove(self.pavouk_eda)
        #         self.eda_added = False

        # Pavouk Hana
        if len(player.had_segmenty) >= 5:
            if not self.hana_added:
                self.pavouci_group.add(self.pavouk_hana)
                self.pavouk_hana.rychlostni_koeficient = player.rychlostni_koeficient
                player.aktivovat_imunitu()
                self.hana_added = True

        # elif len(player.had_segmenty) < 5:
        #     if self.pavouk_hana in self.pavouci_group:
        #         self.pavouci_group.remove(self.pavouk_hana)
        #         self.hana_added = False


        # Další logika pro více než 12 sudů
        if len(player.had_segmenty) >= 12:
            pass  # Zde můžete přidat další logiku, např. nového, silnějšího pavouka

    @staticmethod
    def get_offset(sprite1, sprite2):
        """
        Vypočítá offset sprite2 vzhledem k sprite1 pro pixel-perfect kolizi.
        Pixel-perfect kolize umožňuje přesnější detekci kolizí na základě průhlednosti obrázků,
        namísto pouhých obdélníků (rect).
        :param sprite1: První sprite (např. hráč).
        :param sprite2: Druhý sprite (např. jídlo, pavouk).
        :return: Tuple (offset_x, offset_y) představující posun sprite2 vzhledem k sprite1.
        """
        offset_x = sprite2.rect.x - sprite1.rect.x
        offset_y = sprite2.rect.y - sprite1.rect.y
        return offset_x, offset_y

    def kontrola_kolize(self):
        """
        Kontroluje kolize mezi hráčem a jídlem, a mezi hráčem a pavouky.
        Aplikuje herní logiku pro tyto kolize (zvýšení skóre/sudů, snížení životů/sudů).
        """
        # --- Pixel-perfect kolize hráče s jídlem ---
        for hrac_obj in self.hrac_group:  # Prochází všechny objekty hráče ve skupině (obvykle jen jeden)
            for jedno_jidlo in self.jidla_group:  # Prochází všechny objekty jídla ve skupině
                offset_j = self.get_offset(hrac_obj, jedno_jidlo)  # Získá offset pro pixel-perfect kolizi
                # Kontrola kolize pomocí masek
                if hrac_obj.mask.overlap(jedno_jidlo.mask, offset_j):
                    self.zvuk_kapky.stop()
                    self.zvuk_kapky.play()
                    # Přesune jídlo na náhodnou novou pozici v rámci herní plochy
                    jedno_jidlo.rect.topleft = jidlo.nahodna_pozice(jedno_jidlo.image)
                    self.score += 1  # Zvýší skóre
                    self.kapky_od_posledniho_sudu += 1  # Zvýší počítadlo kapek pro sud
                    # Pokud bylo sebráno dostatek kapek, přidá se nový sud
                    if self.kapky_od_posledniho_sudu >= self.pocet_kapek_na_sud:
                        # Vytvoří nový objekt sudu na pozici hráče
                        new_sud = Sud(hrac_obj.rect.centerx, hrac_obj.rect.centery, "sud_90.png")
                        self.sudy_group.add(new_sud)  # Přidá nový sud do skupiny sudů
                        hrac_obj.pridej_segment(new_sud)  # Přidá sud jako segment k hráči (hadovi)
                        self.kapky_od_posledniho_sudu = 0  # Resetuje počítadlo kapek
            # --- Pixel-perfect kolize hráče s pavoukem ---
            for pavouk_obj in self.pavouci_group:  # Prochází všechny objekty pavouků
                offset_p = self.get_offset(hrac_obj, pavouk_obj)  # Získá offset pro pixel-perfect kolizi
                # Kontrola kolize pomocí masek
                if hrac_obj.mask.overlap(pavouk_obj.mask, offset_p):
                    # Zde aplikujeme logiku imunity
                    if not hrac_obj.imunita_aktivni:  # Pouze pokud hráč NENÍ imunní
                        # self.kousanec_sound.stop()
                        self.kousanec_sound.play()
                        aktualni_pocet_sudu = len(hrac_obj.had_segmenty)  # Získá aktuální počet sudů hráče
                        if aktualni_pocet_sudu >= 1:  # Pokud má hráč alespoň jeden sud
                            odstraneny_sud = hrac_obj.had_segmenty.pop()  # Odebere poslední sud ze seznamu hráče
                            self.sudy_group.remove(odstraneny_sud)  # Odebere sud ze skupiny spriteů sudů
                            self.kapky_od_posledniho_sudu = 0  # Resetuje počítadlo kapek
                        else:  # Pokud hráč nemá žádné sudy (a srazí se s pavoukem)
                            self.zivoty -= 1  # Sníží počet životů
                            self.kapky_od_posledniho_sudu = 0  # Resetuje počítadlo kapek

                        hrac_obj.aktivovat_imunitu()  # Aktivuje imunitu hráče po kolizi (dává mu čas na reakci)
                    # Přesune pavouka mimo obrazovku po kolizi, aby se okamžitě znovu nesrazil
                    pavouk_obj.rect.x = -500
                    pavouk_obj.rect.y = -500
                    # # Původní přesunutí na náhodnou pozici (alternativa):
                    # pavouk_obj.rect.x = random.randint(0, screen_width - pavouk_obj.rect.width)
                    # pavouk_obj.rect.y = random.randint(vyska_horniho_panelu,screen_height - pavouk_obj.rect.height)


    def pause(self):
        self.game_paused = not self.game_paused
        if self.game_paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def stisknute_klavesy(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.lets_continue = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause()
                if event.key == pygame.K_F11:
                    hra.fullscreen()
                if not self.game_paused:
                    player.stisknute_klavesy_player(event)

    def pohyb_mysi(self):
        if self.game_paused:
            mouse_pos = pygame.mouse.get_pos()  # Získá aktuální pozici kurzoru myši
            # Kontrola, zda se myš dotýká text_rect
            if self.konec_text_rect.collidepoint(mouse_pos): # Pokud je pozice myši na textu KONEC HRY
               self.barva_pod_text_nabidky = self.white
               self.barva_textu_nabidky = (58, 88, 255)
               if pygame.mouse.get_pressed()[0]:
                   self.lets_continue = False
            else:
                self.barva_pod_text_nabidky = screen_color
                self.barva_textu_nabidky = self.barva_textu
            # Vždy vygeneruj nový Surface s aktuální barvou pozadí textu a umístění
            self.konec_text = self.font_robot_big_1.render("KONEC HRY", True, self.barva_pod_text_nabidky)
            self.konec_text_rect = self.konec_text.get_rect(center=(screen_width - 400, screen_height // 2))
            self.konec_text0 = self.font_robot_big.render("KONEC HRY", True, self.barva_textu_nabidky)
            self.konec_text0_rect = self.konec_text0.get_rect(center=(screen_width - 400, screen_height // 2))

    @staticmethod
    def get_relative_positions(group, current_width, current_height):
        """
        Uloží relativní pozice všech objektů ve skupině.

        Args:
            group (pygame.sprite.Group): Skupina objektů (např. player_group, jidlo_group).
            current_width (int): Aktuální šířka obrazovky.
            current_height (int): Aktuální výška obrazovky.

        Returns:
            list: Seznam dvojic (objekt, (rel_x, rel_y)).
        """
        relative_positions = []
        for obj in group:
            if hasattr(obj, 'rect') and obj.rect:
                relative_positions.append((obj, obj.rect.centerx / current_width, obj.rect.centery / current_height))
        return relative_positions

    @staticmethod
    def apply_relative_positions(relative_positions_data, new_width, new_height):
        """
        Nastaví absolutní pozice objektům na základě uložených relativních pozic.

        Args:
            relative_positions_data (list): Seznam dvojic (objekt, (rel_x, rel_y))
                                            získaných z _get_relative_positions.
            new_width (int): Nová šířka obrazovky.
            new_height (int): Nová výška obrazovky.
        """
        for obj, rel_x, rel_y in relative_positions_data:
            if hasattr(obj, 'rect') and obj.rect:
                obj.rect.centerx = int(rel_x * new_width)
                obj.rect.centery = int(rel_y * new_height)

    def fullscreen(self):
        global screen, screen_width, screen_height, original_screen_width, original_screen_height

        self.is_fullscreen = not self.is_fullscreen  # Přepne stav fullscreen
        # self.game_paused = True
        # --- Uložení relativních pozic před změnou rozlišení ---
        player_relative_positions = self.get_relative_positions(player_group, screen_width, screen_height)
        jidla_relative_positions = self.get_relative_positions(jidlo_group, screen_width, screen_height)
        pavouci_relative_positions = self.get_relative_positions(pavouk_group, screen_width, screen_height)

        if self.is_fullscreen:
            # Přepne na fullscreen režim
            screen = pygame.display.set_mode((monitor_width, monitor_height), pygame.FULLSCREEN)
            # Aktualizuje šířku a výšku obrazovky pro vykreslování
            screen_width, screen_height = screen.get_size()

        else:
            # Vrátí se do okenního režimu
                # Použijte původní rozměry okna
            screen = pygame.display.set_mode((original_screen_width, original_screen_height))
            screen_width = original_screen_width
            screen_height = original_screen_height

        # --- Přepočet a nastavení nových pozic ---
        # Pozice UI prvků, které závisí na rozměrech obrazovky
        self.pause_text_rect.center = ((screen_width // 2) + 13, (screen_height // 2) + 7)
        self.pause_text0_rect.center = (screen_width // 2, screen_height // 2)

        self.apply_relative_positions(player_relative_positions, screen_width, screen_height)
        self.apply_relative_positions(jidla_relative_positions, screen_width, screen_height)
        self.apply_relative_positions(pavouci_relative_positions, screen_width, screen_height)

    def kresleni(self):
        screen.fill(self.main_color)
        self.kresleni_pozadi()
        self.jidla_group.draw(screen)
        self.sudy_group.draw(screen)
        self.pavouci_group.draw(screen)
        self.hrac_group.draw(screen)
        self.kresleni_horniho_panelu(self.score, self.zivoty, self.rychlost)
        if self.game_paused:
            screen.blit(self.pause_text0, self.pause_text0_rect)
            screen.blit(self.pause_text, self.pause_text_rect)

        pygame.display.update()

    def update(self):
        """
        Aktualizuje stav hry v každém snímku.
        Volá metodu pro kontrolu kolizí a přidávání/odebírání pavouků.
        """
        self.prida_odebere_pavouka()  # Přidává/odebírá pavouky podle počtu sudů hráče
        self.kontrola_kolize()  # Zkontroluje a vyřeší kolize mezi herními prvky
        self.update_stav_is_angry()
        self.update_rychlosti()
        # # Debug výpis:
        # print(f"Player segmenty: {len(player.had_segmenty)}  kapek: {self.score}")
        # print(f"Player koeficient: {player.rychlostni_koeficient:.2f}, player speed {player.speed * player.rychlostni_koeficient:.2f}")
        # for pavouk in self.pavouci_group:
        #     print(f"  {pavouk} koeficient: {pavouk.rychlostni_koeficient:.2f}, speed: {pavouk.speed:.2f} naštvaný: {pavouk.is_angry}")
        # print("---")


    def run(self):
        while self.lets_continue:
            self.stisknute_klavesy()
            self.pohyb_mysi()
            if not self.game_paused:
                self.update()
                player_group.update()
                pavouk_group.update(player.rect)
            self.kresleni()
            clock.tick(fps)

class Jidlo(pygame.sprite.Sprite):
    """
    Třída Jidlo (Food) reprezentuje sbíratelné objekty ve hře (např. kapky oleje).
    """

    def __init__(self, image):
        """
        Konstruktor třídy Jidlo.
        :param image: Název souboru obrázku pro jídlo.
        """
        super().__init__()  # Volá konstruktor rodičovské třídy pygame.sprite.Sprite
        self.image = pygame.image.load(f"media/img/{image}").convert_alpha()  # Načte obrázek jídla
        self.rect = self.image.get_rect()  # Získá obdélník (rect) z obrázku
        self.mask = pygame.mask.from_surface(self.image)  # Vytvoří masku z obrázku pro pixel-perfect kolize
        self.rect.topleft = (self.nahodna_pozice(self.image))  # Nastaví pozici jídla

    def nahodna_pozice(self, image):
        self.image = image  # Uloží obrázek do atributu instance
        jidlo_width = self.image.get_width()  # Zjistí šířku obrázku
        jidlo_height = self.image.get_height()  # Zjistí výšku obrázku
        # Vygeneruje náhodné souřadnice X a Y tak, aby se obrázek vešel na obrazovku
        x = random.randint(0, screen_width - jidlo_width)
        y = random.randint(vyska_horniho_panelu, screen_height - jidlo_height)
        return x, y


class Sud(pygame.sprite.Sprite):
    """
    Třída Sud (Barrel) reprezentuje segmenty "hada" hráče, které se přidávají
    po sebrání dostatečného množství jídla.
    """

    def __init__(self, x, y, image):
        """
        Konstruktor třídy Sud.
        :param x: Počáteční X souřadnice sudu.
        :param y: Počáteční Y souřadnice sudu.
        :param image: Název souboru obrázku pro sud.
        """
        super().__init__()  # Volá konstruktor rodičovské třídy pygame.sprite.Sprite
        self.image = pygame.image.load(f"media/img/{image}").convert_alpha()  # Načte obrázek sudu
        self.rect = self.image.get_rect()  # Získá obdélník z obrázku
        self.mask = pygame.mask.from_surface(self.image)  # Maska pro sudy pro pixel-perfect kolize
        self.rect.center = (x, y)  # Nastaví počáteční pozici sudu (na střed)


class Pavouk(pygame.sprite.Sprite):
    """
    Třída Pavouk (Spider) reprezentuje nepřátelské objekty, které se pohybují
    po obrazovce a mohou hráči ubírat sudy nebo životy. Mění chování a vzhled
    na základě vzdálenosti od hráče.
    """

    def __init__(self, x, y, image, image_angry, rychlost):
        """
        Konstruktor třídy Pavouk.
        :param x: Počáteční X souřadnice pavouka.
        :param y: Počáteční Y souřadnice pavouka.
        :param image: Název souboru obrázku pro normální (klidný) stav pavouka.
        :param image_angry: Název souboru obrázku pro "naštvaný" stav pavouka (když je blízko hráče).
        :param rychlost: Počáteční rychlost pavouka.
        """
        super().__init__()  # Volá konstruktor rodičovské třídy pygame.sprite.Sprite
        self.original_image = pygame.image.load(f"media/img/{image}").convert_alpha()  # Načte normální obrázek pavouka
        self.image = self.original_image  # Aktuální obrázek pavouka
        self.rect = self.image.get_rect()  # Získá obdélník z obrázku
        self.rect.topleft = (x, y)  # Nastaví počáteční pozici pavouka
        self.mask = pygame.mask.from_surface(self.image)  # Maska pro pixel-perfect kolize

        # Načtení a příprava obrázku "naštvaného" pavouka
        self.image_angry = pygame.image.load(f"media/img/{image_angry}").convert_alpha()

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
            # Pavouk se pohybuje agresivně po ose X nebo Y ve směru k hráči.
            # Nejprve resetujeme směr, abychom ho mohli nově nastavit na základě pozice hráče.
            self.direct_x = 0
            self.direct_y = 0

            delta_x = player_rect.centerx - self.rect.centerx
            delta_y = player_rect.centery - self.rect.centery

            # Pohyb prioritně po delší ose (X nebo Y) pro "hadí" pohyb
            if abs(delta_x) > abs(delta_y):  # Je větší rozdíl v X než v Y?
                if delta_x > 0:
                    self.direct_x = 1  # Jdi doprava
                else:
                    self.direct_x = -1  # Jdi doleva
            else:  # Je větší rozdíl v Y než v X? (nebo jsou si rovny)
                if delta_y > 0:
                    self.direct_y = 1  # Jdi dolů
                else:
                    self.direct_y = -1  # Jdi nahoru

        else:
            # Pokud není naštvaný, občas změní náhodný směr, aby se pohyboval nepředvídatelně.
            self.change_dir_timer += 1
            if self.change_dir_timer >= random.randint(60, 120):  # Změna směru každých 1-2 sekundy (60-120 snímků)
                self.change_dir_timer = 0
                self.direct_x, self.direct_y = self.novy_smer()

        # Pohyb pavouka na základě aktuálního směru (cíleného nebo náhodného) a rychlosti
        self.rect.x += self.speed * self.rychlostni_koeficient * self.direct_x
        self.rect.y += self.speed * self.rychlostni_koeficient * self.direct_y

        # Kontrola hranic obrazovky (pavouk se neodrazí, ale zůstane v herní oblasti)
        if self.rect.left < 0:
            self.rect.left = 0
            self.direct_x, self.direct_y = self.novy_smer()  # Změna směru, když narazí na okraj
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
            self.direct_x, self.direct_y = self.novy_smer()

        if self.rect.top < vyska_horniho_panelu:  # Respektuje horní panel
            self.rect.top = vyska_horniho_panelu
            self.direct_x, self.direct_y = self.novy_smer()
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.direct_x, self.direct_y = self.novy_smer()

    def priblizeni(self, player_rect):
        """
        Kontroluje vzdálenost pavouka od hráče. Pokud je hráč blízko, pavouk se "naštve",
        změní obrázek a zrychlí, aby ho pronásledoval.
        :param player_rect: Obdélník (rect) hráče pro výpočet vzdálenosti.
        """
        # Výpočet Eukleidovské vzdálenosti mezi středy pavouka a hráče
        vzdalenost_x = player_rect.centerx - self.rect.centerx
        vzdalenost_y = player_rect.centery - self.rect.centery
        vzdalenost = (vzdalenost_x ** 2 + vzdalenost_y ** 2) ** 0.5

        if vzdalenost < self.pavouk_postava_vzdalenost:  # Pokud je vzdálenost menší než nastavená hodnota
            self.image = self.image_angry  # Změní obrázek na "naštvaný"
            self.speed = self.angry_speed * self.rychlostni_koeficient # Zvýší rychlost
            self.is_angry = True  # Nastaví stav na "naštvaný"
        else:
            self.image = self.original_image  # Vrátí původní obrázek
            self.speed = self.original_speed * self.rychlostni_koeficient # Vrátí původní rychlost
            self.is_angry = False  # Nastaví stav na normální

    def update(self, player_rect):
        """
        Aktualizuje stav pavouka v každém snímku.
        Volá metody pro pohyb a kontrolu přiblížení k hráči.
        :param player_rect: Obdélník (rect) hráče, nutný pro pohyb a přiblížení.
        """
        # Pohybuje pavoukem a kontroluje přiblížení k hráči
        # Používám 'player.direction' jako jednoduchou podmínku pro začátek pohybu pavouků
        # až po prvním pohybu hráče.
        if player.direction:
            self.move(player_rect)
        self.priblizeni(player_rect)  # Zkontroluje přiblížení k hráči

class Player(pygame.sprite.Sprite):
    """
    Třída Player (Hráč) reprezentuje hlavního hrdinu hry (robota/hada).
    Stará se o pohyb, sbírání sudů, imunitu a interakci s klávesnicí.
    """

    def __init__(self, x, y, image, rychlost):
        """
        Konstruktor třídy Player.
        :param x: Počáteční X souřadnice hráče.
        :param y: Počáteční Y souřadnice hráče.
        :param image: Název souboru obrázku pro hráče.
        :param rychlost: Rychlost pohybu hráče.
        """
        super().__init__()  # Volá konstruktor rodičovské třídy pygame.sprite.Sprite
        self.direction = None  # Aktuální směr pohybu hráče (None, 'left', 'right', 'up', 'down')
        self.original_image = pygame.image.load(f"media/img/{image}").convert_alpha()  # Načte původní obrázek hráče
        self.image = self.original_image  # Aktuální obrázek hráče
        self.rect = self.image.get_rect()  # Získá obdélník z obrázku
        self.mask = pygame.mask.from_surface(self.image)  # Maska pro pixel-perfect kolize
        self.rect.center = (x, y)  # Nastaví počáteční pozici hráče na střed
        self.mezera_mezi_sudy = 6  # Mezera v pixelech mezi segmenty hada (sudy)
        self.had_segmenty = []  # Seznam objektů Sud, které tvoří tělo hada
        self.pozice_hlavy = []  # Historie pozic hlavy hráče pro sledování segmentů hada
        self.rychlostni_koeficient = 1.0
        self.speed = rychlost # Rychlost pohybu hráče

        # Parametry imunity
        self.imunita_aktivni = False  # Stav imunity (True = imunní, False = neimunní)
        self.imunita_start_cas = 0  # Čas, kdy imunita začala (v milisekundách)
        self.doba_imunity = 2000  # Doba trvání imunity v milisekundách (např. 2 sekundy)

    def pridej_segment(self, segment):
        """
        Přidá nový sud jako segment k tělu hada hráče.
        :param segment: Objekt Sud, který má být přidán.
        """
        self.had_segmenty.append(segment)

    def stisknute_klavesy_player(self, udalost):
        """
        Zpracovává události stisknutí kláves pro pohyb hráče.
        :param udalost: Objekt události z Pygame (pouze pro typ KEYDOWN).
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
        Aktualizuje pozici hráče na základě jeho směru a rychlosti.
        Zajišťuje, aby hráč "prošel" skrz okraje obrazovky (warp efekt)
        s ohledem na horní panel.
        """
        if self.direction == 'left':
            self.rect.x -= self.speed * self.rychlostni_koeficient
        elif self.direction == 'right':
            self.rect.x += self.speed * self.rychlostni_koeficient
        elif self.direction == 'up':
            self.rect.y -= self.speed * self.rychlostni_koeficient
        elif self.direction == 'down':
            self.rect.y += self.speed * self.rychlostni_koeficient

        # Zajištění "warp" efektu (projití skrz okraj obrazovky a objevení se na protější straně)
        # S ohledem na horní panel (vyska_horniho_panelu)
        if self.rect.bottom < vyska_horniho_panelu:  # Pokud je hráč nad horním panelem (mimo herní plochu)
            self.rect.top = screen_height - 20  # Objeví se dole
        if self.rect.top > screen_height - 20:  # Pokud je hráč pod spodním okrajem
            self.rect.bottom = vyska_horniho_panelu + 20  # Objeví se nahoře (pod panelem)
        if self.rect.right < 5:  # Pokud je hráč vlevo mimo obrazovku
            self.rect.left = screen_width - 5  # Objeví se vpravo
        if self.rect.left > screen_width - 5:  # Pokud je hráč vpravo mimo obrazovku
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
        """
        Aktualizuje pozice všech segmentů hada (sudů) tak, aby následovaly hlavu hráče.
        """
        if self.had_segmenty:  # Pouze pokud hráč má nějaké sudy
            if not self.pozice_hlavy:  # Pokud není k dispozici historie pozic hlavy (mělo by se dít jen na začátku)
                return

            for i, segment in enumerate(self.had_segmenty):  # Prochází každý sud
                # Vypočítá index v historii pozic hlavy, který by měl daný segment sledovat.
                # Čím dál segment je, tím starší pozici sleduje.
                history_index = (i + 1) * self.mezera_mezi_sudy
                # Zajišťuje, že index nepřekročí délku historie, aby se předešlo chybě Index out of range
                history_index = min(history_index, len(self.pozice_hlavy) - 1)

                # Zabezpečení proti zápornému indexu (mělo by se stát pouze při velmi krátké historii)
                if history_index < 0:
                    history_index = 0

                target_x, target_y = self.pozice_hlavy[history_index]  # Získá cílovou pozici pro segment
                segment.rect.center = (target_x, target_y)  # Nastaví pozici segmentu

    def aktivovat_imunitu(self):
        """
        Aktivuje imunitu hráče na určitou dobu. Nastaví stav imunity na aktivní
        a zaznamená čas jejího spuštění.
        """
        self.imunita_aktivni = True  # Nastaví imunitu na aktivní
        self.imunita_start_cas = pygame.time.get_ticks()  # Uloží aktuální čas jako začátek imunity

    def kontrola_imunity(self):
        """
        Zajišťuje blikání hráče, když je aktivní imunita, a vypíná imunitu po uplynutí času.
        Tato metoda by se měla volat v každém snímku (např. v Player.update()).
        """
        if self.imunita_aktivni:
            aktualni_herni_cas = pygame.time.get_ticks()  # Získá aktuální herní čas v milisekundách
            # Kontroluje, zda uplynulá doba od aktivace imunity překročila nastavenou dobu trvání
            if aktualni_herni_cas - self.imunita_start_cas > self.doba_imunity:
                self.imunita_aktivni = False  # Imunita vypršela, deaktivujeme ji
                self.image.set_alpha(255)  # Vrátí plnou neprůhlednost obrázku hráče (přestane blikat)
            else:
                # Blikání: Mění alpha hodnotu (průhlednost) obrázku v intervalu 200ms
                # `// 200` zajistí, že se hodnota mění každých 200 ms, `% 2 == 0` přepíná mezi 0 a 1
                if (aktualni_herni_cas // 200) % 2 == 0:
                    self.image.set_alpha(255)  # Plně viditelná (alpha 255)
                else:
                    self.image.set_alpha(100)  # Částečně průhledná (alpha 100 pro efekt blikání)
        else:
            # Zajistí, že je hráč plně viditelný, pokud není imunní
            self.image.set_alpha(255)

    def update(self):
        """
        Aktualizuje stav hráče v každém snímku.
        Volá metody pro pohyb, aktualizaci segmentů hada a správu imunity.
        """
        self.move()  # Pohyb hráče
        self.update_segmenty_hada()  # Aktualizace pozic segmentů hada
        self.kontrola_imunity()  # Správa imunity a blikání


# --- Vytvoření herních objektů a skupin ---

# Vytvoření instancí pavouků s počátečními pozicemi mimo obrazovku a rychlostmi
# Tito pavouci budou přidáváni dynamicky na základě herního postupu.
pavouk_max = Pavouk(-500, -500, "pavoukMax_165.png", "pavoukMaxAngry_165.png", 6)
pavouk_tery = Pavouk(-500, screen_height + 500, "pavoukTery_165.png", "pavoukTeryAngry_165.png", 6)
pavouk_niky = Pavouk(screen_width + 500, -500, "pavoukNiky_165.png", "pavoukNikyAngry_165.png", 6)
pavouk_eda = Pavouk(screen_width + 500, screen_height + 500,"pavoukEda_185.png", "pavoukEdaAngry_185.png",6)
pavouk_hana = Pavouk(screen_width + 500, screen_height + 500,"pavoukHana_185.png", "pavoukHanaAngry_185.png",6)
# Vytvoříme skupinu spriteů pro pavouky
pavouk_group = pygame.sprite.Group()
# pavouk_group.add(pavouk_hana,pavouk_eda,pavouk_niky,pavouk_tery,pavouk_max)


# Vytvoření instance hráče s počáteční pozicí uprostřed obrazovky a rychlostí
player = Player(screen_width // 2, screen_height // 2, "robot.png", 10)
# Vytvoříme skupinu spriteů pro hráče
player_group = pygame.sprite.Group()
# Přidání hráče do skupiny
player_group.add(player)

# Vytvoření instancí jídla na náhodných pozicích (mimo horní panel)
jidlo = Jidlo("olej.png")
jidlo1 = Jidlo("olej.png")
# Vytvoříme skupinu spriteů pro jídlo
jidlo_group = pygame.sprite.Group()
# Přidá jídlo do skupiny
jidlo_group.add(jidlo, jidlo1)

# Vytvoření počáteční instance sudu (mimo obrazovku, bude se přidávat dynamicky)
# Tento "dummy" sud se nepřidá do had_segmenty hráče na začátku, ale zajistí, že skupina není prázdná,
# což může být užitečné pro některé operace Pygame (i když v tomto kódu to není nezbytně nutné).
# Skutečné sudy se přidávají dynamicky po sebrání kapek.
sud = Sud(-500, -500, "sud_90.png")
# Vytvoříme skupinu spriteů pro sudy (segmenty hada)
sud_group = pygame.sprite.Group()
sud_group.add(sud)  # Sud se nepřidává, protože by se zobrazil. Přidá se až po sebrání kapek.

# Vytvoříme instanci třídy Game a předáme jí všechny potřebné skupiny spriteů a objekty pavouků
hra = Game(player_group, jidlo_group, pavouk_group, sud_group, pavouk_max, pavouk_tery, pavouk_niky, pavouk_eda, pavouk_hana)

# ------------------------------------------------------------------------------------------------------
# --- Spuštění hry ---
hra.fullscreen()
hra.run()
# --- Ukončení hry ---
pygame.quit()  # Odinicializuje všechny moduly Pygame. Toto by mělo být voláno před ukončením programu.
# ------------------------------------------------------------------------------------------------------