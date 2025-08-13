"""
Modul Game obsahuje hlavní herní logiku a smyčku.

Třída Game inicializuje herní prostředí, spravuje herní objekty (hráč, jídlo, pavouci, sudy),
zpracovává interakce (kolize, stisky kláves), aktualizuje herní stav a vykresluje vše na obrazovku.
"""
from typing import Protocol

import pygame
import settings
from barrel import Sud
from pause_menu import PauseMenu
from name_input import NameInput
from score import Score


# Definujte protokol pro objekty, které mají 'rect' atribut
# (jinak hlásí chybu "Unresolved attribute reference 'rect' for class 'Sprite'").
class RectHolder(Protocol):
    rect: pygame.Rect

class Game:
    """
    Hlavní třída hry, která řídí celou herní smyčku, logiku, vykreslování a stav hry.

    Atributy:
        screen (pygame.Surface): Objekt Surface, na který se vše vykresluje.
        pause_menu (PauseMenu): Instance menu pro pozastavení hry.
        hrac_group (pygame.sprite.Group): Skupina spritů pro hráče.
        jidla_group (pygame.sprite.Group): Skupina spritů pro objekty jídla.
        pavouci_group (pygame.sprite.Group): Skupina spritů pro pavouky.
        sudy_group (pygame.sprite.Group): Skupina spritů pro sudy.
        zivoty (int): Aktuální počet životů hráče.
        pocet_kapek_na_sud (int): Počet kapek jídla potřebných pro získání sudu.
        score (int): Aktuální skóre hráče (počet sebraných kapek).
        kapky_od_posledniho_sudu (int): Počet sebraných kapek od posledního získaného sudu.
        rychlost (str/int): Aktuální úroveň rychlosti hry (pro zobrazení na panelu).
        rychlost_played_X (bool): Flagy indikující, zda už byl zvuk rychlosti pro danou úroveň přehrán.
        pavouk_X_obj (Pavouk): Instance jednotlivých pavouků.
        X_added (bool): Flagy indikující, zda už byl daný pavouk přidán do hry.
        game_paused (bool): True, pokud je hra pozastavena, jinak False.
        lets_continue (bool): True, pokud má herní smyčka běžet, jinak False (pro ukončení hry).
        is_fullscreen (bool): True, pokud je hra v režimu celé obrazovky, jinak False.
        zvuk_kapky (pygame.mixer.Sound): Zvuk přehrávaný při sebrání kapky.
        kousanec_sound (pygame.mixer.Sound): Zvuk přehrávaný při kousnutí pavoukem.
        rychlost_sound (pygame.mixer.Sound): Zvuk přehrávaný při změně rychlosti.
        angry_sound (pygame.mixer.Sound): Zvuk alarmu, když je pavouk "angry".
        alarm_hraje (bool): True, pokud hraje alarm "angry" pavouka.
        font_robot_X (pygame.font.Font): Různé velikosti fontů pro texty ve hře.
        barva_textu (tuple): Barva textu.
        white (tuple): Bílá barva.
        main_color (tuple): Hlavní barva pozadí (mění se, když jsou pavouci "angry").
        barva_textu_nabidky (tuple): Barva textu v menu.
        barva_pod_text_nabidky (tuple): Barva pozadí pod textem v menu.
        original_pozadi_image (pygame.Surface): Původní obrázek pozadí.
        scaled_pozadi_image (pygame.Surface): Škálovaný obrázek pozadí pro aktuální rozlišení.
        nadpis_text (pygame.Surface): Předrenderovaný text nadpisu pro horní panel.
        nadpis_text_rect (pygame.Rect): Obdélník pro umístění nadpisu.
    """

    def __init__(self, hrac_group, jidla_group, pavouci_group, sudy_group, pavouk_max_obj, pavouk_tery_obj,
                 pavouk_niky_obj, pavouk_eda_obj, pavouk_hana_obj, obrazovka):
        """
        Inicializuje herní objekt.

        Args:
            hrac_group (pygame.sprite.Group): Skupina spritů obsahující hráče.
            jidla_group (pygame.sprite.Group): Skupina spritů obsahující jídlo.
            pavouci_group (pygame.sprite.Group): Skupina spritů obsahující pavouky.
            sudy_group (pygame.sprite.Group): Skupina spritů obsahující sudy (segmenty hada).
            pavouk_max_obj (Pavouk): Instance pavouka Max.
            pavouk_tery_obj (Pavouk): Instance pavouka Tery.
            pavouk_niky_obj (Pavouk): Instance pavouka Niky.
            pavouk_eda_obj (Pavouk): Instance pavouka Eda.
            pavouk_hana_obj (Pavouk): Instance pavouka Hana.
            obrazovka (pygame.Surface): Objekt Surface hlavního okna hry.
        """
        self.ulozit_score = True
        self.screen = obrazovka
        # --- Fáze zadávání jména ---
        # Vytvoření instance NameInput
        self.name_input_screen = NameInput(self.screen, self)
        self.player_name_entered = False  # Flag, který bude True, až když je jméno hotové

        # Inicializace menu pro pauzu, předáváme aktuální obrazovku a její rozměry.
        self.pause_menu = PauseMenu(self.screen, self)
        self.score_list = Score(self.screen)
        self.score = settings.SCORE

        # Skupiny spritů pro snadnou správu herních objektů.
        self.hrac_group = hrac_group
        self.jidla_group = jidla_group
        self.pavouci_group = pavouci_group
        self.sudy_group = sudy_group
        self.hrac_obj = list(self.hrac_group)[0]  # Získejte referenci na hráče
        self.player_name = settings.PLAYER_NAME

        # Herní stavové proměnné.
        self.zivoty = settings.ZIVOTY
        self.pocet_kapek_na_sud = settings.POCET_KAPEK_NA_SUD
        self.kapky_od_posledniho_sudu = 0

        # Proměnné pro řízení rychlosti hry a zvukových efektů.
        self.rychlost = 1  # Slouží k vypsání rychlosti na horním panelu
        self.rychlost_played_2 = False
        self.rychlost_played_5 = False
        self.rychlost_played_8 = False

        # Reference na jednotlivé instance pavouků.
        self.pavouk_max = pavouk_max_obj
        self.pavouk_tery = pavouk_tery_obj
        self.pavouk_niky = pavouk_niky_obj
        self.pavouk_eda = pavouk_eda_obj
        self.pavouk_hana = pavouk_hana_obj

        # Flagy pro sledování, zda už byl pavouk přidán do hry.
        self.tery_added = False
        self.niky_added = False
        self.max_added = False
        self.eda_added = False
        self.hana_added = False
        self.any_spider_angry = False

        # Stavové flagy pro hru.
        self.game_paused = False
        self.lets_continue = True  # Určuje, zda má hlavní herní smyčka běžet
        self.is_fullscreen = False

        # Inicializace hudby a zvukových efektů.
        pygame.mixer.music.load(settings.MUSIC_PATH)
        pygame.mixer.music.play(-1)  # Spustí hudbu ve smyčce
        pygame.mixer.music.set_volume(0.3)

        self.zvuk_kapky = pygame.mixer.Sound(settings.ZVUK_KAPKY_PATH)
        self.zvuk_kapky.set_volume(0.2)
        self.kanal1 = pygame.mixer.Channel(0)  # Vyhrazený kanál pro zvuk kapky

        self.kousanec_sound = pygame.mixer.Sound(settings.KOUSANEC_SOUND_PATH)
        self.kousanec_sound.set_volume(0.2)
        self.kanal2 = pygame.mixer.Channel(1)  # Vyhrazený kanál pro zvuk kousnutí

        self.rychlost_sound = pygame.mixer.Sound(settings.RYCHLOST_SOUND_PATH)
        self.kanal3 = pygame.mixer.Channel(3)  # Vyhrazený kanál pro zvuk rychlosti

        self.angry_sound = pygame.mixer.Sound(settings.ANGRY_SOUND_PATH)
        self.angry_sound.set_volume(0.3)
        self.kanal4 = pygame.mixer.Channel(4)  # Vyhrazený kanál pro "angry" alarm
        self.alarm_hraje = False  # Sleduje, zda alarm právě hraje

        # Nastavení fontů pro renderování textu.
        self.font_robot = pygame.font.Font(settings.FONT_ROBOT_PATH, 50)
        self.font_robot_big = pygame.font.Font(settings.FONT_ROBOT_PATH, 80)
        self.font_robot_big_1 = pygame.font.Font(settings.FONT_ROBOT_PATH, 90)
        self.font_robot_small = pygame.font.Font(settings.FONT_ROBOT_PATH, 25)

        # Nastavení barev.
        self.barva_textu = settings.BARVA_TEXTU
        self.white = settings.WHITE
        self.main_color = settings.SCREEN_COLOR  # Dynamicky se mění při "angry" stavu
        self.barva_textu_nabidky = self.barva_textu
        self.barva_pod_text_nabidky = settings.SCREEN_COLOR

        # Načtení a škálování pozadí pouze jednou při inicializaci pro optimalizaci.
        self.original_pozadi_image = pygame.image.load(settings.POZADI_IMAGE_PATH).convert_alpha()
        self.scaled_pozadi_image = pygame.transform.scale(
            self.original_pozadi_image,
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT - settings.VYSKA_HORNIHO_PANELU)
        )

        # Statické texty pro horní panel, renderujeme jen jednou.
        self.nadpis_text = self.font_robot.render("PAVOUCI_KOMARKOVI", True, self.barva_textu)
        self.nadpis_text_rect = self.nadpis_text.get_rect(
            center=(settings.SCREEN_WIDTH // 2, settings.VYSKA_HORNIHO_PANELU // 2)
        )

    def zadani_jmena(self):
        # Smyčka pro zadávání jména

        self.name_input_screen.reset()
        self.player_name_entered = False
        while not self.player_name_entered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  # Ukončí program, pokud uživatel zavře okno

                # Zpracování události třídou NameInput
                returned_name = self.name_input_screen.handle_event(event)

                # Pokud handle_event vrátí jméno, znamená to, že bylo potvrzeno
                if returned_name:
                    settings.PLAYER_NAME = returned_name  # Uložíme jméno do settings
                    self.player_name_entered = True  # Nastavíme flag pro ukončení smyčky zadávání jména

            # Aktualizace a vykreslení obrazovky zadávání jména
            self.name_input_screen.update()  # Aktualizuje kurzor
            self.name_input_screen.draw(self.screen)  # Vykreslí aktuální stav na obrazovku

            pygame.display.flip()  # Aktualizuje celou obrazovku
            pygame.time.Clock().tick(settings.FPS)  # Řídí FPS pro fázi zadávání jména


    def kresleni_pozadi(self):
        """
        Vykreslí pozadí herní obrazovky.

        Používá předem škálovaný obrázek pozadí.
        """
        # Nyní používáme již škálovaný obrázek a umisťujeme ho pod horní panel.
        pozadi_image_rect = self.scaled_pozadi_image.get_rect(topleft=(0, settings.VYSKA_HORNIHO_PANELU))
        self.screen.blit(self.scaled_pozadi_image, pozadi_image_rect)

    def kresleni_horniho_panelu(self):
        """
        Vykresluje horní informační panel s aktuálním skóre, počtem sudů, rychlostí a životy.

        """
        # Přistup k player objektu. Předpokládá se, že v hrací skupině je jen jeden hráč.
        pocet_sudu = len(list(self.hrac_group)[0].had_segmenty)

        # Vyplnění pozadí horního panelu.
        self.screen.fill(self.main_color, (0, 0, settings.SCREEN_WIDTH, settings.VYSKA_HORNIHO_PANELU))
        # Vykreslení oddělovací čáry pod horním panelem.
        pygame.draw.line(self.screen, self.white, (0, settings.VYSKA_HORNIHO_PANELU),
                         (settings.SCREEN_WIDTH, settings.VYSKA_HORNIHO_PANELU))

        # Dynamické texty, které se mění, a proto se musí renderovat v každém snímku.

        score_text = self.font_robot_small.render(f"POCET_KAPEK: {self.score}", True, self.barva_textu)
        score_text_rect = score_text.get_rect(topleft=(10, 0))

        barel_text = self.font_robot_small.render(f"POCET_SUDU: {pocet_sudu}", True, self.barva_textu)
        barel_text_rect = barel_text.get_rect(topleft=(10, 25))

        rychlost_text = self.font_robot.render(f"RYCHLOST HRY: {self.rychlost}", True, self.barva_textu)
        rychlost_text_rect = rychlost_text.get_rect(center=(450, settings.VYSKA_HORNIHO_PANELU // 2))

        text_jmeno = self.font_robot.render(f"player: {settings.PLAYER_NAME}", True, self.barva_textu)
        text_jmeno_rect = text_jmeno.get_rect(center=((settings.SCREEN_WIDTH // 2) + 480, settings.VYSKA_HORNIHO_PANELU // 2))

        lives_text = self.font_robot.render(f"ZIVOTY: {self.zivoty}", True, self.barva_textu)
        lives_text_rect = lives_text.get_rect(topright=(settings.SCREEN_WIDTH - 10, 0))

        # Vykreslení všech textů na obrazovku.
        self.screen.blit(lives_text, lives_text_rect)
        self.screen.blit(barel_text, barel_text_rect)
        self.screen.blit(rychlost_text, rychlost_text_rect)
        self.screen.blit(self.nadpis_text, self.nadpis_text_rect)  # Používáme předrenderovaný nadpis
        self.screen.blit(score_text, score_text_rect)
        self.screen.blit(text_jmeno, text_jmeno_rect)

    def update_stav_is_angry(self):
        """
        Aktualizuje barvu pozadí a přehrává/zastavuje alarm na základě toho,
        zda je některý z pavouků v "angry" stavu.
        """
        self.any_spider_angry = False
        # Prochází všechny pavouky a kontroluje jejich stav.
        for jeden_pavouk in self.pavouci_group:
            if jeden_pavouk.is_angry:
                self.any_spider_angry = True
                break  # Stačí najít jednoho "angry" pavouka

        if self. any_spider_angry:
            self.main_color = settings.ANGRY_COLOR  # Změní barvu pozadí na "angry"
            if not self.alarm_hraje:
                self.kanal4.play(self.angry_sound, loops=-1)  # Spustí alarm ve smyčce
                self.alarm_hraje = True
        else:
            self.main_color = settings.SCREEN_COLOR  # Obnoví normální barvu pozadí
            if self.alarm_hraje:
                self.kanal4.stop()  # Zastaví alarm
                self.alarm_hraje = False

    def update_rychlosti(self):
        """
        Aktualizuje rychlost hráče a pavouků na základě počtu získaných sudů.
        Přehrává zvukový efekt při každé změně rychlosti.
        """

        velikost = len(self.hrac_obj.had_segmenty)  # Počet sudů určuje úroveň rychlosti

        # Podmínky pro zvýšení rychlosti a přehrání zvuku (pouze jednou pro každou úroveň).
        if velikost >= 8 and not self.rychlost_played_8:
            self.kanal3.play(self.rychlost_sound)
            self.rychlost_played_8 = True
            self.hrac_obj.rychlostni_koeficient = settings.RYCHLOST_MAX
            self.hrac_obj.mezera_mezi_sudy = 4
            self.rychlost = "MAX"  # Text pro zobrazení

        if velikost >= 5 and not self.rychlost_played_5:
            # Kontrola pořadí: tato podmínka se může splnit dříve než pro 8 sudů,
            # takže je důležité, aby neblokovala další úrovně.
            # Zde je pořadí důležité pro správnou aktivaci rychlostí.
            self.kanal3.play(self.rychlost_sound)
            self.rychlost_played_5 = True
            self.hrac_obj.rychlostni_koeficient = settings.RYCHLOST_3
            self.hrac_obj.mezera_mezi_sudy = 4
            self.rychlost = "3"

        if velikost >= 2 and not self.rychlost_played_2:
            self.kanal3.play(self.rychlost_sound)
            self.rychlost_played_2 = True
            self.hrac_obj.rychlostni_koeficient = settings.RYCHLOST_2
            self.hrac_obj.mezera_mezi_sudy = 5
            self.rychlost = "2"

        # Všichni pavouci dostávají stejný rychlostní koeficient jako hráč.
        for pavouk in self.pavouci_group:
            pavouk.rychlostni_koeficient = self.hrac_obj.rychlostni_koeficient

    def prida_odebere_pavouka(self):
        """
        Dynamicky přidává nové pavouky do hry na základě počtu získaných sudů hráčem.
        Při přidání pavouka se hráči aktivuje dočasná imunita.
        """

        # Podmínka pro Max pavouka.
        # Poznámka: `len(hrac_obj.had_segmenty) >= 0` je vždy True, takže pavouk Max se přidá vždy.
        if len(self.hrac_obj.had_segmenty) >= 0:
            if not self.max_added:
                self.pavouci_group.add(self.pavouk_max)
                # Nastaví pavoukovi stejnou rychlost jako má hráč.
                self.pavouk_max.rychlostni_koeficient = self.hrac_obj.rychlostni_koeficient
                self.hrac_obj.aktivovat_imunitu()  # Hráč získá imunitu po přidání pavouka
                self.max_added = True

        # Podmínka pro Tery pavouka.
        if len(self.hrac_obj.had_segmenty) >= 2:
            if not self.tery_added:
                self.pavouci_group.add(self.pavouk_tery)
                self.pavouk_tery.rychlostni_koeficient = self.hrac_obj.rychlostni_koeficient
                self.hrac_obj.aktivovat_imunitu()
                self.tery_added = True

        # Podmínka pro Niky pavouka.
        if len(self.hrac_obj.had_segmenty) >= 3:
            if not self.niky_added:
                self.pavouci_group.add(self.pavouk_niky)
                self.pavouk_niky.rychlostni_koeficient = self.hrac_obj.rychlostni_koeficient
                self.hrac_obj.aktivovat_imunitu()
                self.niky_added = True

        # Podmínka pro Eda pavouka.
        if len(self.hrac_obj.had_segmenty) >= 5:
            if not self.eda_added:
                self.pavouci_group.add(self.pavouk_eda)
                self.pavouk_eda.rychlostni_koeficient = self.hrac_obj.rychlostni_koeficient
                self.hrac_obj.aktivovat_imunitu()
                self.eda_added = True

        # Podmínka pro Hana pavouka.
        # Poznámka: Tato podmínka je stejná jako pro Eda pavouka (>= 5).
        # Zkontrolujte, zda je to záměr, nebo zda by zde měla být jiná hodnota (např. >= 7 nebo 8).
        if len(self.hrac_obj.had_segmenty) >= 5:
            if not self.hana_added:
                self.pavouci_group.add(self.pavouk_hana)
                self.pavouk_hana.rychlostni_koeficient = self.hrac_obj.rychlostni_koeficient
                self.hrac_obj.aktivovat_imunitu()
                self.hana_added = True

        # Místo pro další logiku, pokud hráč získá více sudů.
        if len(self.hrac_obj.had_segmenty) >= 12:
            pass

    @staticmethod
    def get_offset(sprite1: RectHolder, sprite2: RectHolder):
        """
        Vypočítá offset mezi dvěma spritovými objekty pro použití s maskovou kolizí.

        Args:
            sprite1 (pygame.sprite.Sprite): První sprite (obvykle hráč).
            sprite2 (pygame.sprite.Sprite): Druhý sprite (jídlo, pavouk, sud).

        Returns:
            tuple: Offset ve formátu (offset_x, offset_y).
        """
        offset_x = sprite2.rect.x - sprite1.rect.x
        offset_y = sprite2.rect.y - sprite1.rect.y
        return offset_x, offset_y

    def kontrola_kolize(self):
        """
        Kontroluje kolize mezi hráčem a jídlem, a mezi hráčem a pavouky.
        Zpracovává důsledky kolizí (sběr jídla, ztráta sudů/životů).
        """

        # Kontrola kolize s jídlem.
        for jedno_jidlo in self.jidla_group:
            offset_j = self.get_offset(self.hrac_obj, jedno_jidlo)
            if self.hrac_obj.mask.overlap(jedno_jidlo.mask, offset_j):
                self.kanal1.play(self.zvuk_kapky)  # Přehrání zvuku sebrání kapky
                jedno_jidlo.rect.topleft = jedno_jidlo.nahodna_pozice()  # Přemístění jídla
                self.score += 1
                self.kapky_od_posledniho_sudu += 1
                settings.SCORE =self.score
                # Pokud hráč sebral dostatek kapek, přidá se nový sud (segment hada).
                if self.kapky_od_posledniho_sudu >= self.pocet_kapek_na_sud:
                    # Nový sud se objeví na pozici hráče.
                    new_sud = Sud(self.hrac_obj.rect.centerx, self.hrac_obj.rect.centery, settings.BARREL_IMAGE)
                    self.sudy_group.add(new_sud)
                    self.hrac_obj.pridej_segment(new_sud)  # Přidání sudu k hráči (hadovi)
                    self.kapky_od_posledniho_sudu = 0  # Reset počítadla kapek

        # Kontrola kolize s pavouky.
        for pavouk_obj in self.pavouci_group:
            offset_p = self.get_offset(self.hrac_obj, pavouk_obj)
            if self.hrac_obj.mask.overlap(pavouk_obj.mask, offset_p):
                if not self.hrac_obj.imunita_aktivni:
                    self.kanal2.play(self.kousanec_sound)  # Přehrání zvuku kousnutí
                    aktualni_pocet_sudu = len(self.hrac_obj.had_segmenty)
                    if aktualni_pocet_sudu >= 1:
                        # Hráč ztratí sud (segment hada).
                        odstraneny_sud = self.hrac_obj.had_segmenty.pop()
                        self.sudy_group.remove(odstraneny_sud)
                        self.kapky_od_posledniho_sudu = 0  # Reset počítadla kapek
                    else:
                        # Hráč ztratí život, pokud už nemá žádné sudy.
                        self.zivoty -= 1
                        self.kapky_od_posledniho_sudu = 0

                    self.hrac_obj.aktivovat_imunitu()  # Hráč získá dočasnou imunitu
                    # Pavouk je po kolizi přesunut mimo obrazovku, aby se neustále nespouštěla kolize
                    # (pouze pokud hrac není imunní, když je imuní pavouk se nepřesune)
                    pavouk_obj.rect.x = -500
                    pavouk_obj.rect.y = -500
            if self.zivoty == 0:
                self.game_over()

    def pause(self):
        """
        Přepíná stav pozastavení hry. Pokud je hra pozastavena, zobrazí se pauza menu.
        Zpracovává volby z pauza menu (pokračování, restart, ukončení).
        """
        if not self.game_paused:
            # Hru pozastavíme a spustíme menu.
            pygame.mixer.music.pause()  # Zastaví hudbu
            pygame.mixer.Sound.stop(self.angry_sound)  # Zastaví "angry" alarm, pokud hraje
            self.game_paused = True
            result = self.pause_menu.show_menu()  # Zobrazí menu a čeká na volbu
            self.game_paused = False  # Po návratu z menu hru vždy rozjedeme (nebo ukončíme)
            if result == "quit":
                self.lets_continue = False  # Nastaví flag pro ukončení hlavní smyčky
            elif result == "restart":
                # Zde by se měla přidat logika pro restart hry (např. resetování všech herních proměnných
                # a pozic objektů, nebo volání metody pro restart).
                self.restart()
            elif result == "new_game":
                # Zde by se měla přidat logika pro restart hry (např. resetování všech herních proměnných
                # a pozic objektů, nebo volání metody pro restart).
                self.new_game()

            else:  # result == "continue" nebo jakákoli jiná možnost, která nekončí hru
                pygame.mixer.music.unpause()  # **Pokračuje v hudbě po návratu z menu**
                if self.alarm_hraje:  # Pokud hrál alarm před pauzou, měl by hrát i teď
                    self.kanal4.play(self.angry_sound, loops=-1)
                self.hrac_obj.direction = None

    def new_game(self):
        settings.GAME_OVER = False
        self.ulozit_score = True
        settings.PLAYER_NAME = ""
        self.score = 0
        self.hrac_obj.had_segmenty.clear()  # Vyprázdní segmenty hada (sudy)
        self.kresleni_horniho_panelu()
        self.zadani_jmena()
        if self.player_name_entered:
            self.restart()

    def restart(self):
        """
        Resetuje hru do počátečního stavu po restartu.
        Vynuluje skóre, životy, pozice objektů, vymaže sudy, resetuje pavouky a zvuky.
        """
        # Zastav a resetuj zvuky
        pygame.mixer.music.stop()
        if self.kanal4.get_busy():
            self.kanal4.stop()
        self.alarm_hraje = False  # Resetujte flag, že alarm nehraje
        pygame.mixer.music.play(-1)  # Znovu spustí hudbu na pozadí

        # Resetuj herní stavové proměnné
        self.zivoty = settings.ZIVOTY  # Reset životů!
        settings.GAME_OVER = False
        self.score = 0
        settings.SCORE = 0
        self.kapky_od_posledniho_sudu = 0
        self.rychlost = 1  # Nastaví rychlost zpět na výchozí zobrazení
        self.main_color = settings.SCREEN_COLOR  # Obnoví normální barvu pozadí

        # Resetuj flagy rychlosti
        self.rychlost_played_2 = False
        self.rychlost_played_5 = False
        self.rychlost_played_8 = False

        # Resetuj hráče
        # Nastavení směru na nulový vektor, aby se hráč hned nepohyboval
        self.hrac_obj.direction = None
        self.hrac_obj.rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)  # Střed herní plochy
        self.hrac_obj.aktivovat_imunitu()  # Získá imunitu na začátku nové hry
        self.hrac_obj.rychlostni_koeficient = settings.RYCHLOST_1  # Reset rychlosti hráče
        self.hrac_obj.had_segmenty.clear()  # Vyprázdní segmenty hada (sudy)
        self.sudy_group.empty()  # Odstraní všechny sudy ze skupiny spritů

        # Resetuj pavouky
        self.pavouci_group.empty()  # Odstraní všechny pavouky ze skupiny spritů
        self.prida_odebere_pavouka()  # Znovu přidá počáteční pavouky do hry
        # Resetuj flagy pro přidání pavouků
        self.max_added = False
        self.pavouk_max.rect.x = -500
        self.pavouk_max.rect.y = -500
        self.tery_added = False
        self.niky_added = False
        self.eda_added = False
        self.hana_added = False
        self.pavouk_max.is_angry = False
        self.pavouk_tery.is_angry = False
        self.pavouk_niky.is_angry = False
        self.pavouk_eda.is_angry = False
        self.pavouk_hana.is_angry = False

        # Resetuj jídlo
        for jedno_jidlo in self.jidla_group:
            jedno_jidlo.rect.topleft = jedno_jidlo.nahodna_pozice()  # Přemístění jídla

        # Zajišťuje, že se hra po restartu nepřeruší
        self.ulozit_score = True
        self.lets_continue = True

    def game_over(self):
# -------------------------------------------------------------------------------------------------------------------------------
        if self.ulozit_score:
            self.score_list.save_score(settings.PLAYER_NAME, settings.SCORE)
            self.ulozit_score = False
        settings.SCORE = 0
        settings.GAME_OVER = True
# --------------------------------------------------------------------------------------------------------------------------------
        self.draw_game_over()
        self.zivoty = 0
        self.kresleni_horniho_panelu()
        self.pause()  # Pozastaví/rozjede hru
    def draw_game_over(self):
            dialog_width = 500
            dialog_height = 200
            dialog_rect = pygame.Rect(0, 0, dialog_width, dialog_height)
            dialog_rect.center = (settings.SCREEN_WIDTH // 2, 300 + 3)

            # Vyplnění pozadí dialogu (podobně jako u tlačítek)
            pygame.draw.rect(self.screen, settings.POZADI_MENU, dialog_rect, border_radius=20)
            # Volitelné: ohraničení dialogu
            pygame.draw.rect(self.screen, settings.BORDER, dialog_rect, 3,
                             border_radius=20)  # Bílý rámeček, tloušťka 3px

            text_game_over = self.font_robot_big_1.render("GAME OVER", True, settings.BARVA_TEXTU_MENU)
            text_game_over_rect = text_game_over.get_rect(center=((settings.SCREEN_WIDTH // 2), 300))
            self.screen.blit(text_game_over, text_game_over_rect)



    def stisknute_klavesy(self):
        """
        Zpracovává události stisku kláves a ukončení okna.
        Řídí pauzu hry, přepínání fullscreenu a pohyb hráče.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.lets_continue = False  # Nastaví flag pro ukončení hry
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause()  # Pozastaví/rozjede hru
                if event.key == pygame.K_F11:
                    self.fullscreen()  # Přepne režim celé obrazovky
                # Pokud není hra pozastavena, zpracuj vstup pro hráče.
                if not self.game_paused:
                    self.hrac_obj.stisknute_klavesy_player(event)

    @staticmethod
    def get_relative_positions(group, current_width, current_height):
        """
        Získá relativní pozice všech spritů v dané skupině vzhledem k aktuálním rozměrům obrazovky.

        Args:
            group (pygame.sprite.Group): Skupina spritů, pro které se mají získat pozice.
            current_width (int): Aktuální šířka obrazovky.
            current_height (int): Aktuální výška obrazovky.

        Returns:
            list: Seznam tuplic, kde každá tuplice obsahuje (objekt, relativní_x, relativní_y).
        """
        relative_positions = []
        for obj in group:
            if hasattr(obj, 'rect') and obj.rect:
                # Ukládá referenci na objekt a jeho relativní pozice (procenta šířky/výšky).
                relative_positions.append((obj, obj.rect.centerx / current_width, obj.rect.centery / current_height))
        return relative_positions

    @staticmethod
    def apply_relative_positions(relative_positions_data, new_width, new_height):
        """
        Aplikuje dříve získané relativní pozice na sprity v nové velikosti obrazovky.

        Args:
            relative_positions_data (list): Seznam tuplic s objekty a jejich relativními pozicemi.
            new_width (int): Nová šířka obrazovky.
            new_height (int): Nová výška obrazovky.
        """
        for obj, rel_x, rel_y in relative_positions_data:
            if hasattr(obj, 'rect') and obj.rect:
                # Přepočítá absolutní pozici na základě nových rozměrů.
                obj.rect.centerx = int(rel_x * new_width)
                obj.rect.centery = int(rel_y * new_height)

    def fullscreen(self):
        """
        Přepíná režim zobrazení mezi oknem a celou obrazovkou.
        Zachovává relativní pozice všech herních objektů a aktualizuje nastavení.
        """
        original_screen_width = self.screen.get_width()
        original_screen_height = self.screen.get_height()

        # Přepneme stav fullscreenu hned na začátku.
        self.is_fullscreen = not self.is_fullscreen

        # Získejte relativní pozice všech herních skupin PŘED změnou rozlišení.
        player_relative_positions = self.get_relative_positions(self.hrac_group, original_screen_width,
                                                                original_screen_height)
        jidla_relative_positions = self.get_relative_positions(self.jidla_group, original_screen_width,
                                                               original_screen_height)
        pavouci_relative_positions = self.get_relative_positions(self.pavouci_group, original_screen_width,
                                                                 original_screen_height)
        sudy_relative_positions = self.get_relative_positions(self.sudy_group, original_screen_width,
                                                                 original_screen_height)

        if self.is_fullscreen:
            # Nastaví režim celé obrazovky na rozlišení monitoru.
            self.screen = pygame.display.set_mode((settings.MONITOR_WIDTH, settings.MONITOR_HEIGHT), pygame.FULLSCREEN)
            # Aktualizuje GLOBÁLNÍ nastavení rozměrů obrazovky.
            settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT = self.screen.get_size()

        else:
            # Přepne zpět do okenního režimu na původní rozlišení.
            self.screen = pygame.display.set_mode((settings.ORIGINAL_SCREEN_WIDTH, settings.ORIGINAL_SCREEN_HEIGHT))
            # Aktualizuje GLOBÁLNÍ nastavení rozměrů obrazovky.
            settings.SCREEN_WIDTH = settings.ORIGINAL_SCREEN_WIDTH
            settings.SCREEN_HEIGHT = settings.ORIGINAL_SCREEN_HEIGHT

        # Zde se znovu škáluje pozadí, protože se změnilo rozlišení obrazovky.
        self.scaled_pozadi_image = pygame.transform.scale(
            self.original_pozadi_image,
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT - settings.VYSKA_HORNIHO_PANELU)
        )

        # Aplikujte relativní pozice na základě nových rozměrů obrazovky.
        self.apply_relative_positions(player_relative_positions, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.apply_relative_positions(jidla_relative_positions, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.apply_relative_positions(pavouci_relative_positions, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.apply_relative_positions(sudy_relative_positions, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

        # Aktualizujte pozice textů, které závisí na rozměrech obrazovky.
        # Konkrétně nadpis na horním panelu a pozice tlačítek
        self.nadpis_text_rect.center = (settings.SCREEN_WIDTH // 2, settings.VYSKA_HORNIHO_PANELU // 2)
        self.pause_menu.update_screen_size(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

    def kresleni(self):
        """
        Vykreslí všechny herní objekty a UI prvky na obrazovku.
        """
        self.screen.fill(self.main_color)  # Vyplní celou obrazovku hlavní barvou (změní se při "angry" stavu)
        self.kresleni_pozadi()  # Vykreslí pozadí herní plochy
        self.jidla_group.draw(self.screen)  # Vykreslí všechny objekty jídla
        self.sudy_group.draw(self.screen)  # Vykreslí všechny objekty sudů
        self.pavouci_group.draw(self.screen)  # Vykreslí všechny pavouky
        self.hrac_group.draw(self.screen)  # Vykreslí hráče
        # Vykreslí horní panel s aktuálními herními informacemi
        self.kresleni_horniho_panelu()
        pygame.display.update()  # Aktualizuje celou obrazovku

    def update(self):
        """
        Aktualizuje stav všech herních objektů a logiky v každém snímku.
        Zahrnuje přidávání pavouků, kontrolu kolizí a aktualizaci rychlosti.
        """
        self.prida_odebere_pavouka()
        self.kontrola_kolize()
        self.update_stav_is_angry()
        self.update_rychlosti()

    def run(self):
        """
        Hlavní herní smyčka. Zpracovává události, aktualizuje herní stav a vykresluje.
        Pokračuje, dokud se proměnná `self.lets_continue` nestane False.
        """
        self.kresleni()
        # self.zadani_jmena()
        self.new_game()
        while self.lets_continue:
            self.stisknute_klavesy()  # Zpracování uživatelského vstupu
            if not self.game_paused:
                self.update()  # Aktualizace herní logiky
                self.hrac_group.update()  # Aktualizace hráče
                self.pavouci_group.update() # Aktualizace pavouků
            self.kresleni()  # Vykreslení všech herních prvků
            pygame.time.Clock().tick(settings.FPS)  # Omezuje rychlost hry na definované FPS
