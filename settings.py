"""
Modul settings.py obsahuje globální konstanty a konfigurační parametry pro hru.
Definuje herní pravidla, rozměry obrazovky, rychlosti objektů, barvy,
cesty k souborům s médii a další důležitá nastavení.
"""

from screeninfo import get_monitors

# --- Základní herní pravidla ---
# Počáteční počet životů hráče.
ZIVOTY = 3
# Počet sebraných kapek jídla potřebných k získání jednoho sudu (segmentu "hada").
POCET_KAPEK_NA_SUD = 2
# Počáteční skóre hráče.
SCORE = 0

# --- Rychlosti herních objektů ---
# Základní rychlost pohybu pavouků (v pixelech za snímek).
SPIDER_RYCHLOST = 6
# Základní rychlost pohybu hráče (v pixelech za snímek).
PLAYER_RYCHLOST = 10

# Koeficienty pro modifikaci rychlosti hráče a pavouků.
# Používají se k postupnému zvyšování obtížnosti nebo k aktivaci speciálních stavů.
RYCHLOST_1 = 1.0  # Výchozí rychlost (100%)
RYCHLOST_2 = 1.2  # Zvýšená rychlost (120%)
RYCHLOST_3 = 1.4  # Další zvýšení rychlosti (140%)
RYCHLOST_MAX = 1.5 # Maximální rychlostní koeficient (150%)

# Vzdálenost v pixelech mezi segmenty (sudy) hada.
MEZERA_MEZI_SUDY = 5
# Doba trvání imunity hráče po zásahu (v milisekundách). 2000 ms = 2 sekundy.
DOBA_IMUNITY = 2000 
# Vzdálenost v pixelech, pod kterou se pavouk stane "naštvaným" a začne pronásledovat hráče.
ANGRY_VZDALENOST = 400
# Násobitel rychlosti pavouka, když je "naštvaný". (Přidáno pro lepší konfiguraci a oddělení od SPIDER_RYCHLOST)
ANGRY_SPEED_MULTIPLIER = 1.5 # Příklad: 1.5x původní rychlost


# --- Nastavení obrazovky ---
# Získání rozměrů primárního monitoru pro potenciální fullscreen režim.
try:
    monitors = get_monitors()
    MONITOR_WIDTH = monitors[0].width
    MONITOR_HEIGHT = monitors[0].height
except IndexError:
    # Fallback pro případ, kdy není detekován žádný monitor (např. v CI/CD prostředí)
    MONITOR_WIDTH = 1920
    MONITOR_HEIGHT = 1080
    print("Upozornění: Nelze detekovat monitor. Používám výchozí rozlišení 1920x1080.")


# Výchozí šířka herního okna.
SCREEN_WIDTH = 1400
# Výchozí výška herního okna.
SCREEN_HEIGHT = 700
# Původní (výchozí) šířka herního okna, pro případné přepočty při změně velikosti.
ORIGINAL_SCREEN_WIDTH = SCREEN_WIDTH
# Původní (výchozí) výška herního okna, pro případné přepočty při změně velikosti.
ORIGINAL_SCREEN_HEIGHT = SCREEN_HEIGHT

# Výška horního informačního panelu (např. pro skóre, životy).
VYSKA_HORNIHO_PANELU = 64
# Maximální počet snímků za sekundu (Frame Rate) pro hru.
FPS = 60

# --- Barvy (RGB formát) ---
SCREEN_COLOR = (0, 0, 0)          # Černá barva pozadí obrazovky
BARVA_TEXTU = (50, 103, 6)        # Specifická zelená barva pro texty
WHITE = (255, 255, 255)           # Čistě bílá barva
ANGRY_COLOR = (128, 0, 0)         # Tmavě červená barva, např. pro indikaci "naštvaného" stavu
BARVA_HOVER = (58, 88, 255)       # Světle modrá barva pro efekt najetí myši na tlačítka

# --- Cesty k souborům s médii ---
# Cesta k souboru s ikonou okna hry.
IKONA_IMAGE_PATH = "media/img/robot.png"
# Cesta k souboru s vlastním písmem.
FONT_ROBOT_PATH = "media/fonts/Super Rocky by All Super Font.ttf"
# Cesta k souboru s hudbou na pozadí.
MUSIC_PATH = "media/sounds/Desert_Nomad.ogg"
# Cesta k souboru se zvukem sebrání kapky jídla.
ZVUK_KAPKY_PATH = "media/sounds/olej_sound.ogg"
# Cesta k souboru se zvukem kousnutí/zásahu pavoukem.
KOUSANEC_SOUND_PATH = "media/sounds/kousanec.ogg"
# Cesta k souboru se zvukem aktivace rychlostního bonusu.
RYCHLOST_SOUND_PATH = "media/sounds/rychlost.ogg"
# Cesta k souboru se zvukem, když se pavouk "naštve".
ANGRY_SOUND_PATH = "media/sounds/angry.ogg"
# Cesta k souboru s obrázkem pozadí hry.
POZADI_IMAGE_PATH = "media/img/pozadi.png"

# --- Názvy souborů obrázků pro herní objekty ---
# Tyto konstanty uchovávají pouze názvy souborů, bez cesty,
# protože cesta "media/img/" je přidávána přímo ve třídách, které je používají.
PLAYER_IMAGE = "robot.png"
FOOD_IMAGE = "olej.png"
BARREL_IMAGE = "sud_90.png"

# Obrázky pro různé typy pavouků a jejich "naštvané" varianty.
PAVOUK_MAX_IMAGE = "pavoukMax_165.png"
PAVOUK_MAX_ANGRY_IMAGE = "pavoukMaxAngry_165.png"
PAVOUK_TERY_IMAGE = "pavoukTery_165.png"
PAVOUK_TERY_ANGRY_IMAGE = "pavoukTeryAngry_165.png"
PAVOUK_NIKY_IMAGE = "pavoukNiky_165.png"
PAVOUK_NIKY_ANGRY_IMAGE = "pavoukNikyAngry_165.png"
PAVOUK_EDA_IMAGE = "pavoukEda_185.png"
PAVOUK_EDA_ANGRY_IMAGE = "pavoukEdaAngry_185.png"
PAVOUK_HANA_IMAGE = "pavoukHana_185.png"
PAVOUK_HANA_ANGRY_IMAGE = "pavoukHanaAngry_185.png"
