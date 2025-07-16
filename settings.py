from screeninfo import get_monitors

# základní nastavení pravydel hry
ZIVOTY = 3
POCET_KAPEK_NA_SUD = 2
SCORE = 0
RYCHLOST_1 = 1.0
RYCHLOST_2 = 1.2
RYCHLOST_3 = 1.4
RYCHLOST_MAX = 1.5
MEZERA_MEZI_SUDY = 5
DOBA_IMUNITY = 2000 # 2000 = 2s

# Získání rozměrů primárního monitoru
monitors = get_monitors()
MONITOR_WIDTH = monitors[0].width
MONITOR_HEIGHT = monitors[0].height

# --- Nastavení obrazovky ---
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700
ORIGINAL_SCREEN_WIDTH = SCREEN_WIDTH
ORIGINAL_SCREEN_HEIGHT = SCREEN_HEIGHT
SCREEN_COLOR = (0, 0, 0)
IKONA_IMAGE_PATH = "media/img/robot.png"

# --- Nastavení herních parametrů ---
VYSKA_HORNIHO_PANELU = 64
FPS = 60

# --- Barvy ---
BARVA_TEXTU = (50, 103, 6)
WHITE = (255, 255, 255)

# --- Cesty k souborům ---
FONT_ROBOT_PATH = "media/fonts/Super Rocky by All Super Font.ttf"
MUSIC_PATH = "media/sounds/Desert_Nomad.ogg"
ZVUK_KAPKY_PATH = "media/sounds/olej_sound.ogg"
KOUSANEC_SOUND_PATH = "media/sounds/kousanec.ogg"
RYCHLOST_SOUND_PATH = "media/sounds/rychlost.ogg"
ANGRY_SOUND_PATH = "media/sounds/angry.ogg"
POZADI_IMAGE_PATH = "media/img/pozadi.png"

# Třídy pro obrázky herních objektů (necháme je zde pro snadný přístup)
# Alternativně by mohly být tyto cesty přímo v konstruktorech tříd, pokud nejsou sdílené.
PLAYER_IMAGE = "robot.png"
FOOD_IMAGE = "olej.png"
BARREL_IMAGE = "sud_90.png"
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