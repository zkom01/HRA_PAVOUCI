"""
Hlavní modul pro spuštění hry "EDOVA_HRA".

Inicializuje Pygame, nastavuje okno hry, načítá herní zdroje a vytváří instance
všech hlavních herních objektů a skupin. Následně spouští hlavní herní smyčku
a provádí profilování výkonu pro ladící účely.
"""

import pygame
import settings
from game import Game
from player import Player
from spider import Pavouk
from food import Jidlo
from barrel import Sud

# --- Inicializace Pygame ---
# Inicializuje všechny moduly Pygame potřebné pro běh hry.
pygame.init()

# --- Nastavení herního okna ---
# Nastavuje rozměry okna na základě hodnot definovaných v modulu 'settings'.
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
# Nastavuje titulek okna hry.
pygame.display.set_caption("EDOVA_HRA")
# Načítá obrázek pro ikonu okna.
ikona_image = pygame.image.load(settings.IKONA_IMAGE_PATH)
# Nastavuje ikonu okna.
pygame.display.set_icon(ikona_image)

# --- Vytvoření herních objektů a skupin spritů ---
# Vytváří instance pavouků s jejich počátečními pozicemi, obrázky a rychlostmi.
# Každý pavouk má normální a "naštvaný" obrázek.
pavouk_max = Pavouk(-500, -500, settings.PAVOUK_MAX_IMAGE, settings.PAVOUK_MAX_ANGRY_IMAGE, settings.SPIDER_RYCHLOST)
pavouk_tery = Pavouk(-500, settings.SCREEN_HEIGHT + 500, settings.PAVOUK_TERY_IMAGE, settings.PAVOUK_TERY_ANGRY_IMAGE, settings.SPIDER_RYCHLOST)
pavouk_niky = Pavouk(settings.SCREEN_WIDTH + 500, -500, settings.PAVOUK_NIKY_IMAGE, settings.PAVOUK_NIKY_ANGRY_IMAGE, settings.SPIDER_RYCHLOST)
pavouk_eda = Pavouk(settings.SCREEN_WIDTH + 500, settings.SCREEN_HEIGHT + 500, settings.PAVOUK_EDA_IMAGE, settings.PAVOUK_EDA_ANGRY_IMAGE, settings.SPIDER_RYCHLOST)
pavouk_hana = Pavouk(settings.SCREEN_WIDTH + 500, settings.SCREEN_HEIGHT + 500, settings.PAVOUK_HANA_IMAGE, settings.PAVOUK_HANA_ANGRY_IMAGE, settings.SPIDER_RYCHLOST)
# Skupina spritů pro všechny pavouky. Inicializována prázdná, pavouci se přidávají v Game třídě.
pavouk_group = pygame.sprite.Group()

# Vytváří instanci hráče na středu obrazovky.
player = Player(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2, settings.PLAYER_IMAGE, settings.PLAYER_RYCHLOST)
# Skupina spritů pro hráče. Obsahuje pouze jednoho hráče.
player_group = pygame.sprite.Group()
player_group.add(player)

# Vytváří instance jídla.
jidlo = Jidlo(settings.FOOD_IMAGE)
jidlo1 = Jidlo(settings.FOOD_IMAGE)
# Skupina spritů pro jídlo.
jidlo_group = pygame.sprite.Group()
jidlo_group.add(jidlo, jidlo1)

# Vytváří instanci sudu.
# Počáteční pozice mimo obrazovku, bude se objevovat dynamicky.
sud = Sud(-500, -500, settings.BARREL_IMAGE)
# Skupina spritů pro sudy.
sud_group = pygame.sprite.Group()
sud_group.add(sud) # Poznámka: Pokud tento sud nemá být trvale přítomen, ale objevovat se dynamicky,
                   # je vhodné ho zde nepřidávat do skupiny, nebo ho přidat až při jeho generování.

# Vytváří hlavní instanci hry, předává jí všechny potřebné herní objekty a skupiny.
hra = Game(player_group, jidlo_group, pavouk_group, sud_group,
           pavouk_max, pavouk_tery, pavouk_niky, pavouk_eda, pavouk_hana, screen)

# --- Spuštění hry a profilování ---
# Nastaví hru na celoobrazovkový režim, pokud je v nastavení povoleno.
hra.fullscreen()

# # Importy pro ladění a profilování výkonu.
# import cProfile
# import pstats
#
# # Inicializace a spuštění profilování kódu.
# profiler = cProfile.Profile()
# profiler.enable()

# Spustí hlavní herní smyčku.
hra.run()

# # Ukončení profilování a výpis statistik.
# profiler.disable()
# # Seřadí statistiky podle kumulativního času (celkový čas strávený ve funkci a jejích podfunkcích).
# stats = pstats.Stats(profiler).sort_stats('cumtime')
# # Vypíše top 20 nejpomalejších funkcí do standardního výstupu.
# stats.print_stats(20)
#
# # Uloží statistiky profilování do souboru 'profil.txt'.
# with open("profil.txt", "w") as f:
#     stats = pstats.Stats(profiler, stream=f).sort_stats('cumtime')
#     stats.print_stats(20)

# --- Ukončení Pygame ---
# Odinicializuje Pygame a uvolní všechny zdroje.
pygame.quit()
