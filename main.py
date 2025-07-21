import pygame

import settings
from game import Game
from player import Player
from spider import Pavouk
from food import Jidlo
from barrel import Sud

# --- Inicializace hry ---
pygame.init()

# --- Nastavení obrazovky ---
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("EDOVA_HRA")
ikona_image = pygame.image.load(settings.IKONA_IMAGE_PATH)
pygame.display.set_icon(ikona_image)


# --- Vytvoření herních objektů a skupin ---
pavouk_max = Pavouk(-500, -500, settings.PAVOUK_MAX_IMAGE, settings.PAVOUK_MAX_ANGRY_IMAGE, settings.SPIDER_RYCHLOST)
pavouk_tery = Pavouk(-500, settings.SCREEN_HEIGHT + 500, settings.PAVOUK_TERY_IMAGE, settings.PAVOUK_TERY_ANGRY_IMAGE, settings.SPIDER_RYCHLOST)
pavouk_niky = Pavouk(settings.SCREEN_WIDTH + 500, -500, settings.PAVOUK_NIKY_IMAGE, settings.PAVOUK_NIKY_ANGRY_IMAGE, settings.SPIDER_RYCHLOST)
pavouk_eda = Pavouk(settings.SCREEN_WIDTH + 500, settings.SCREEN_HEIGHT + 500, settings.PAVOUK_EDA_IMAGE, settings.PAVOUK_EDA_ANGRY_IMAGE, settings.SPIDER_RYCHLOST)
pavouk_hana = Pavouk(settings.SCREEN_WIDTH + 500, settings.SCREEN_HEIGHT + 500, settings.PAVOUK_HANA_IMAGE, settings.PAVOUK_HANA_ANGRY_IMAGE, settings.SPIDER_RYCHLOST)
pavouk_group = pygame.sprite.Group()

player = Player(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2, settings.PLAYER_IMAGE, settings.PLAYER_RYCHLOST)
player_group = pygame.sprite.Group()
player_group.add(player)

jidlo = Jidlo(settings.FOOD_IMAGE)
jidlo1 = Jidlo(settings.FOOD_IMAGE)
jidlo_group = pygame.sprite.Group()
jidlo_group.add(jidlo, jidlo1)

sud = Sud(-500, -500, settings.BARREL_IMAGE)
sud_group = pygame.sprite.Group()
sud_group.add(sud) # Bude odstraněno, pokud tento sud nemá být počáteční

hra = Game(player_group, jidlo_group, pavouk_group, sud_group, pavouk_max, pavouk_tery, pavouk_niky, pavouk_eda, pavouk_hana, screen)

# --- Spuštění hry ---
hra.fullscreen()

# --- Profilování ---
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

hra.run()

profiler.disable()

# Výpis do konzole
stats = pstats.Stats(profiler).sort_stats('cumtime')
stats.print_stats(20) # Zobrazí top 20 nejpomalejších funkcí v konzoli

# Výpis do souboru
with open("profil_log.txt", "w") as f:
    stats = pstats.Stats(profiler, stream=f).sort_stats('cumtime')
    stats.print_stats(20)  # Zapíše do souboru

# --- Ukončení hry ---
pygame.quit()
