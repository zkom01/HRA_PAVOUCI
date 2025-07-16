import pygame
import settings  # Importujeme modul settings
from barrel import Sud  # Importujeme třídu Sud
from pause_menu import PauseMenu


class Game:
    def __init__(self, hrac_group, jidla_group, pavouci_group, sudy_group, pavouk_max_obj, pavouk_tery_obj,
                 pavouk_niky_obj, pavouk_eda_obj, pavouk_hana_obj, obrazovka):
        self.screen = obrazovka
        self.menu = PauseMenu(obrazovka)

        self.hrac_group = hrac_group
        self.jidla_group = jidla_group
        self.pavouci_group = pavouci_group
        self.sudy_group = sudy_group

        self.zivoty = settings.ZIVOTY
        self.pocet_kapek_na_sud = settings.POCET_KAPEK_NA_SUD
        self.score = 0
        self.kapky_od_posledniho_sudu = 0

        self.rychlost = 1 # slouží k vypsání rychlosti na horním panelu
        self.rychlost_played_2 = False
        self.rychlost_played_5 = False
        self.rychlost_played_8 = False

        self.pavouk_max = pavouk_max_obj
        self.pavouk_tery = pavouk_tery_obj
        self.pavouk_niky = pavouk_niky_obj
        self.pavouk_eda = pavouk_eda_obj
        self.pavouk_hana = pavouk_hana_obj

        self.tery_added = False
        self.niky_added = False
        self.max_added = False
        self.eda_added = False
        self.hana_added = False

        self.game_paused = False
        self.lets_continue = True
        self.is_fullscreen = False

        pygame.mixer.music.load(settings.MUSIC_PATH)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

        self.zvuk_kapky = pygame.mixer.Sound(settings.ZVUK_KAPKY_PATH)
        self.zvuk_kapky.set_volume(0.2)
        self.kanal1 = pygame.mixer.Channel(0)

        self.kousanec_sound = pygame.mixer.Sound(settings.KOUSANEC_SOUND_PATH)
        self.kousanec_sound.set_volume(0.2)
        self.kanal2 = pygame.mixer.Channel(1)

        self.rychlost_sound = pygame.mixer.Sound(settings.RYCHLOST_SOUND_PATH)
        self.kanal3 = pygame.mixer.Channel(3)

        self.angry_sound = pygame.mixer.Sound(settings.ANGRY_SOUND_PATH)
        self.angry_sound.set_volume(0.3)
        self.kanal4 = pygame.mixer.Channel(4)
        self.alarm_hraje = False

        self.font_robot = pygame.font.Font(settings.FONT_ROBOT_PATH, 50)
        self.font_robot_big = pygame.font.Font(settings.FONT_ROBOT_PATH, 80)
        self.font_robot_big_1 = pygame.font.Font(settings.FONT_ROBOT_PATH, 90)
        self.font_robot_small = pygame.font.Font(settings.FONT_ROBOT_PATH, 25)

        self.barva_textu = settings.BARVA_TEXTU
        self.white = settings.WHITE
        self.main_color = settings.SCREEN_COLOR
        self.barva_textu_nabidky = self.barva_textu
        self.barva_pod_text_nabidky = settings.SCREEN_COLOR

        # Načtení pozadí JEDNOU
        self.original_pozadi_image = pygame.image.load(settings.POZADI_IMAGE_PATH).convert_alpha()
        # Škálování pozadí JEDNOU při inicializaci
        self.scaled_pozadi_image = pygame.transform.scale(self.original_pozadi_image,
                                                          (settings.SCREEN_WIDTH,
                                                           settings.SCREEN_HEIGHT - settings.VYSKA_HORNIHO_PANELU))

        # # Předpřipravíme text "PAUZA" pro efektivnější vykreslování
        # self.pause_text0 = self.font_robot_big_1.render("PAUZA", True, self.main_color)
        # self.pause_text = self.font_robot_big.render("PAUZA", True, self.barva_textu)
        # self.pause_text0_rect = self.pause_text0.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        # self.pause_text_rect = self.pause_text.get_rect(center=((settings.SCREEN_WIDTH // 2) + 13, (settings.SCREEN_HEIGHT // 2) + 7))
        #
        #
        # # Nabídka při PAUSE
        # self.konec_text = self.font_robot_big_1.render("KONEC HRY", True, self.barva_pod_text_nabidky)
        # self.konec_text_rect = self.konec_text.get_rect(
        #     center=(settings.SCREEN_WIDTH - 400, (settings.SCREEN_HEIGHT // 2)))
        # self.konec_text0 = self.font_robot_big.render("KONEC HRY", True, self.barva_textu)
        # self.konec_text0_rect = self.konec_text0.get_rect(
        #     center=(settings.SCREEN_WIDTH - 400, settings.SCREEN_HEIGHT // 2))

        # Statické texty pro horní panel (renderujeme jen jednou)
        self.nadpis_text = self.font_robot.render("PAVOUCI_KOMARKOVI", True, self.barva_textu)
        self.nadpis_text_rect = self.nadpis_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.VYSKA_HORNIHO_PANELU // 2))

    def kresleni_pozadi(self):
        # Nyní používáme již škálovaný obrázek
        pozadi_image_rect = self.scaled_pozadi_image.get_rect(topleft=(0, settings.VYSKA_HORNIHO_PANELU))
        self.screen.blit(self.scaled_pozadi_image, pozadi_image_rect)

    def kresleni_horniho_panelu(self, score, lives, speed):
        pocet_sudu = len(list(self.hrac_group)[0].had_segmenty)  # Přistup k player objektu

        self.screen.fill(self.main_color, (0, 0, settings.SCREEN_WIDTH, settings.VYSKA_HORNIHO_PANELU)) # Vyplnění barvou
        pygame.draw.line(self.screen, self.white, (0, settings.VYSKA_HORNIHO_PANELU),
                         (settings.SCREEN_WIDTH, settings.VYSKA_HORNIHO_PANELU))

        # Tyto texty se mění, takže se musí renderovat v každém snímku
        score_text = self.font_robot_small.render(f"POCET_KAPEK: {score}", True, self.barva_textu)
        score_text_rect = score_text.get_rect(topleft=(10, 0))

        barel_text = self.font_robot_small.render(f"POCET_SUDU: {pocet_sudu}", True, self.barva_textu)
        barel_text_rect = barel_text.get_rect(topleft=(10, 25))

        rychlost_text = self.font_robot.render(f"RYCHLOST HRY: {speed}", True, self.barva_textu)
        rychlost_text_rect = rychlost_text.get_rect(center=(450, settings.VYSKA_HORNIHO_PANELU // 2))

        lives_text = self.font_robot.render(f"ZIVOTY: {lives}", True, self.barva_textu)
        lives_text_rect = lives_text.get_rect(topright=(settings.SCREEN_WIDTH - 10, 0))

        # Používáme self.screen přímo
        self.screen.blit(lives_text, lives_text_rect)
        self.screen.blit(barel_text, barel_text_rect)
        self.screen.blit(rychlost_text, rychlost_text_rect)
        self.screen.blit(self.nadpis_text, self.nadpis_text_rect) # Používáme předrenderovaný nadpis
        self.screen.blit(score_text, score_text_rect)

        # if self.game_paused:
        #     self.screen.blit(self.konec_text, self.konec_text_rect)
        #     self.screen.blit(self.konec_text0, self.konec_text0_rect)

    def update_stav_is_angry(self):
        any_spider_angry = False
        for jeden_pavouk in self.pavouci_group:
            if jeden_pavouk.is_angry:
                any_spider_angry = True
                break

        if any_spider_angry:
            self.main_color = settings.ANGRY_COLOR
            if not self.alarm_hraje:
                self.kanal4.play(self.angry_sound, loops=-1)
                self.alarm_hraje = True
        else:
            self.main_color = settings.SCREEN_COLOR
            if self.alarm_hraje:
                self.kanal4.stop()
                self.alarm_hraje = False

    def update_rychlosti(self):
        hrac_obj = list(self.hrac_group)[0]  # Předpokládáme, že ve skupině je jen jeden hráč
        velikost = len(hrac_obj.had_segmenty)

        if velikost >= 8 and not self.rychlost_played_8:
            self.kanal3.play(self.rychlost_sound)
            self.rychlost_played_8 = True
            hrac_obj.rychlostni_koeficient = settings.RYCHLOST_MAX
            hrac_obj.mezera_mezi_sudy = 4
            self.rychlost = "MAX"

        if velikost >= 5 and not self.rychlost_played_5:
            self.kanal3.play(self.rychlost_sound)
            self.rychlost_played_5 = True
            hrac_obj.rychlostni_koeficient = settings.RYCHLOST_3
            hrac_obj.mezera_mezi_sudy = 4
            self.rychlost = 3

        if velikost >= 2 and not self.rychlost_played_2:
            self.kanal3.play(self.rychlost_sound)
            self.rychlost_played_2 = True
            hrac_obj.rychlostni_koeficient = settings.RYCHLOST_2
            hrac_obj.mezera_mezi_sudy = 5
            self.rychlost = 2

        for pavouk in self.pavouci_group:
            pavouk.rychlostni_koeficient = hrac_obj.rychlostni_koeficient

    def prida_odebere_pavouka(self):
        hrac_obj = list(self.hrac_group)[0]  # Předpokládáme, že ve skupině je jen jeden hráč
        if len(hrac_obj.had_segmenty) >= 0: # Tahle podmínka je vždy splněna, pavouk Max se přidá vždy
            if not self.max_added:
                self.pavouci_group.add(self.pavouk_max)
                self.pavouk_max.rychlostni_koeficient = hrac_obj.rychlostni_koeficient
                hrac_obj.aktivovat_imunitu()
                self.max_added = True

        if len(hrac_obj.had_segmenty) >= 2:
            if not self.tery_added:
                self.pavouci_group.add(self.pavouk_tery)
                self.pavouk_tery.rychlostni_koeficient = hrac_obj.rychlostni_koeficient
                hrac_obj.aktivovat_imunitu()
                self.tery_added = True

        if len(hrac_obj.had_segmenty) >= 3:
            if not self.niky_added:
                self.pavouci_group.add(self.pavouk_niky)
                self.pavouk_niky.rychlostni_koeficient = hrac_obj.rychlostni_koeficient
                hrac_obj.aktivovat_imunitu()
                self.niky_added = True

        if len(hrac_obj.had_segmenty) >= 5:
            if not self.eda_added:
                self.pavouci_group.add(self.pavouk_eda)
                self.pavouk_eda.rychlostni_koeficient = hrac_obj.rychlostni_koeficient
                hrac_obj.aktivovat_imunitu()
                self.eda_added = True

        if len(hrac_obj.had_segmenty) >= 5:  # Zkontrolujte tuto podmínku - dvě stejné podmínky (eda a hana)
            if not self.hana_added:
                self.pavouci_group.add(self.pavouk_hana)
                self.pavouk_hana.rychlostni_koeficient = hrac_obj.rychlostni_koeficient
                hrac_obj.aktivovat_imunitu()
                self.hana_added = True

        if len(hrac_obj.had_segmenty) >= 12:
            pass # Sem byste mohl přidat nějakou logiku, pokud by to bylo potřeba

    @staticmethod
    def get_offset(sprite1, sprite2):
        offset_x = sprite2.rect.x - sprite1.rect.x
        offset_y = sprite2.rect.y - sprite1.rect.y
        return offset_x, offset_y

    def kontrola_kolize(self):
        hrac_obj = list(self.hrac_group)[0]  # Předpokládáme, že ve skupině je jen jeden hráč

        for jedno_jidlo in self.jidla_group:
            offset_j = self.get_offset(hrac_obj, jedno_jidlo)
            if hrac_obj.mask.overlap(jedno_jidlo.mask, offset_j):
                self.kanal1.play(self.zvuk_kapky)
                jedno_jidlo.rect.topleft = jedno_jidlo.nahodna_pozice()
                self.score += 1
                self.kapky_od_posledniho_sudu += 1
                if self.kapky_od_posledniho_sudu >= self.pocet_kapek_na_sud:
                    new_sud = Sud(hrac_obj.rect.centerx, hrac_obj.rect.centery,
                                  settings.BARREL_IMAGE)  # Použijte nastavení
                    self.sudy_group.add(new_sud)
                    hrac_obj.pridej_segment(new_sud)
                    self.kapky_od_posledniho_sudu = 0

        for pavouk_obj in self.pavouci_group:
            offset_p = self.get_offset(hrac_obj, pavouk_obj)
            if hrac_obj.mask.overlap(pavouk_obj.mask, offset_p):
                if not hrac_obj.imunita_aktivni:
                    self.kanal2.play(self.kousanec_sound)
                    aktualni_pocet_sudu = len(hrac_obj.had_segmenty)
                    if aktualni_pocet_sudu >= 1:
                        odstraneny_sud = hrac_obj.had_segmenty.pop()
                        self.sudy_group.remove(odstraneny_sud)
                        self.kapky_od_posledniho_sudu = 0
                    else:
                        self.zivoty -= 1
                        self.kapky_od_posledniho_sudu = 0

                    hrac_obj.aktivovat_imunitu()
                pavouk_obj.rect.x = -500
                pavouk_obj.rect.y = -500

    def pause(self):
        self.game_paused = not self.game_paused
        if self.game_paused:
            pygame.mixer.music.pause()
            result = self.menu.show_menu()
            if result == "restart":
                print("Restart hry")
                # Tady přidej reset_game() nebo jinou logiku
        else:
            pygame.mixer.music.unpause()

    def stisknute_klavesy(self):
        player_obj = list(self.hrac_group)[0]  # Předpokládáme, že ve skupině je jen jeden hráč
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.lets_continue = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause()
                if event.key == pygame.K_F11:
                    self.fullscreen()
                if not self.game_paused:
                    player_obj.stisknute_klavesy_player(event)

    # def pohyb_mysi(self):
    #     if self.game_paused:
    #         mouse_pos = pygame.mouse.get_pos()
    #         # Použijte self.screen pro zjištění rozměrů, nebo settings.SCREEN_WIDTH/HEIGHT
    #         # Optimalizace: Tyto texty by se měly renderovat jen při změně mouse_pos nebo stavu
    #         # Ale pro teď je ponecháme pro funkčnost.
    #         if self.konec_text_rect.collidepoint(mouse_pos):
    #             self.barva_pod_text_nabidky = self.white
    #             self.barva_textu_nabidky = settings.BARVA_HOVER
    #             if pygame.mouse.get_pressed()[0]:
    #                 self.lets_continue = False
    #         else:
    #             self.barva_pod_text_nabidky = settings.SCREEN_COLOR
    #             self.barva_textu_nabidky = self.barva_textu
    #         self.konec_text = self.font_robot_big_1.render("KONEC HRY", True, self.barva_pod_text_nabidky)
    #         self.konec_text_rect = self.konec_text.get_rect(
    #             center=(settings.SCREEN_WIDTH - 400, settings.SCREEN_HEIGHT // 2))
    #         self.konec_text0 = self.font_robot_big.render("KONEC HRY", True, self.barva_textu_nabidky)
    #         self.konec_text0_rect = self.konec_text0.get_rect(
    #             center=(settings.SCREEN_WIDTH - 400, settings.SCREEN_HEIGHT // 2))

    @staticmethod
    def get_relative_positions(group, current_width, current_height):
        relative_positions = []
        for obj in group:
            if hasattr(obj, 'rect') and obj.rect:
                relative_positions.append((obj, obj.rect.centerx / current_width, obj.rect.centery / current_height))
        return relative_positions

    @staticmethod
    def apply_relative_positions(relative_positions_data, new_width, new_height):
        for obj, rel_x, rel_y in relative_positions_data:
            if hasattr(obj, 'rect') and obj.rect:
                obj.rect.centerx = int(rel_x * new_width)
                obj.rect.centery = int(rel_y * new_height)

    def fullscreen(self):
        # Není potřeba 'global screen'
        original_screen_width = self.screen.get_width()
        original_screen_height = self.screen.get_height()

        # Přepněte stav fullscreenu hned na začátku
        self.is_fullscreen = not self.is_fullscreen

        # Získejte relativní pozice před změnou rozlišení
        player_relative_positions = self.get_relative_positions(self.hrac_group, original_screen_width,
                                                                original_screen_height)
        jidla_relative_positions = self.get_relative_positions(self.jidla_group, original_screen_width,
                                                               original_screen_height)
        pavouci_relative_positions = self.get_relative_positions(self.pavouci_group, original_screen_width,
                                                                 original_screen_height)
        sudy_relative_positions = self.get_relative_positions(self.sudy_group, original_screen_width,
                                                                 original_screen_height) # Přidáno pro sudy

        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((settings.MONITOR_WIDTH, settings.MONITOR_HEIGHT), pygame.FULLSCREEN)
            settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT = self.screen.get_size()  # Aktualizujeme globální nastavení
        else:
            self.screen = pygame.display.set_mode((settings.ORIGINAL_SCREEN_WIDTH, settings.ORIGINAL_SCREEN_HEIGHT))
            settings.SCREEN_WIDTH = settings.ORIGINAL_SCREEN_WIDTH  # Aktualizujeme globální nastavení
            settings.SCREEN_HEIGHT = settings.ORIGINAL_SCREEN_HEIGHT  # Aktualizujeme globální nastavení

        # Zde znovu škálujeme pozadí, protože se změnilo rozlišení
        self.scaled_pozadi_image = pygame.transform.scale(self.original_pozadi_image,
                                                          (settings.SCREEN_WIDTH,
                                                           settings.SCREEN_HEIGHT - settings.VYSKA_HORNIHO_PANELU))

        # Aplikujte relativní pozice na základě nových rozměrů
        self.apply_relative_positions(player_relative_positions, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.apply_relative_positions(jidla_relative_positions, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.apply_relative_positions(pavouci_relative_positions, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.apply_relative_positions(sudy_relative_positions, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT) # Použito pro sudy

        # Aktualizujte pozice textů závislých na rozměrech obrazovky
        # self.pause_text0_rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
        # self.pause_text_rect.center = ((settings.SCREEN_WIDTH // 2) + 13, (settings.SCREEN_HEIGHT // 2) + 7)
        # self.konec_text_rect.center = (settings.SCREEN_WIDTH - 400, (settings.SCREEN_HEIGHT // 2))
        # self.konec_text0_rect.center = (settings.SCREEN_WIDTH - 400, settings.SCREEN_HEIGHT // 2)
        self.nadpis_text_rect.center = (settings.SCREEN_WIDTH // 2, settings.VYSKA_HORNIHO_PANELU // 2)

    def kresleni(self):
        self.screen.fill(self.main_color) # Používáme self.screen přímo
        self.kresleni_pozadi()
        self.jidla_group.draw(self.screen) # Používáme self.screen přímo
        self.sudy_group.draw(self.screen) # Používáme self.screen přímo
        self.pavouci_group.draw(self.screen) # Používáme self.screen přímo
        self.hrac_group.draw(self.screen) # Používáme self.screen přímo
        self.kresleni_horniho_panelu(self.score, self.zivoty, self.rychlost)
        # if self.game_paused:
        #     self.screen.blit(self.pause_text0, self.pause_text0_rect)
        #     self.screen.blit(self.pause_text, self.pause_text_rect)

        pygame.display.update()

    def update(self):
        self.prida_odebere_pavouka()
        self.kontrola_kolize()
        self.update_stav_is_angry()
        self.update_rychlosti()

    def run(self):
        hrac_obj = list(self.hrac_group)[0]  # Předpokládáme, že ve skupině je jen jeden hráč
        while self.lets_continue:
            self.stisknute_klavesy()
            # self.pohyb_mysi()
            if not self.game_paused:
                self.update()
                self.hrac_group.update()
                self.pavouci_group.update(hrac_obj.rect)  # Pavouci potřebují rect hráče
            self.kresleni()
            pygame.time.Clock().tick(settings.FPS)  # Používáme Clock ze settings.py