# 🕷️ Pavouci Komárkovi

Pygame hra inspirovaná klasickým konceptem "Snake", rozšířená o dynamické nepřátele, adaptivní obtížnost a stavový AI systém pavouků.

Projekt demonstruje praktické využití OOP v Pythonu a práci s herními mechanikami v reálném čase.

---

## 🚀 Technologický framing (Co projekt ukazuje)

- **Herní logika**: Implementace plynulého pohybu a kolizního systému v Pygame.
- **AI Nepřátel**: Využití stavových automatů (klidný vs. agresivní mód) pro chování pavouků.
- **Dynamická obtížnost**: Adaptivní zrychlování hry a přidávání nepřátel v závislosti na postupu hráče.
- **Data Persistence**: Ukládání a správa historických výsledků (Top 10) pomocí formátu JSON.

---

## 🎮 Herní princip

Hráč ovládá robota, který sbírá kapky oleje a postupně za sebou vytváří „ocas“ ze sudů.

**Cílem hry je:**
- Přežít co nejdéle a sbírat kapky oleje.
- Vyhýbat se pavoukům, kteří reagují na vaši blízkost.
- Tvořit co nejdelší řetězec sudů pro vyšší skóre.

**S rostoucím skóre:**
- Se zvyšuje rychlost pohybu.
- Na mapě se objevuje více pavouků.
- Hra vyžaduje vyšší postřeh a strategické plánování pohybu.

---

## 🕹️ Ovládání

| Klávesa | Funkce |
| :--- | :--- |
| **WASD / Šipky** | Pohyb hráče |
| **Mezerník** | Pauza / Menu |
| **F11** | Fullscreen |

---

## 🕷️ Systém umělé inteligence

Pavouci nejsou jen statické překážky, ale využívají dva základní stavy:

1. **Klidný stav**: Náhodný pohyb v prostoru mapy.
2. **Agresivní stav**: Pokud se hráč přiblíží na určitou vzdálenost, pavouk začne hráče aktivně pronásledovat.

**Vlastnosti systému:**
- Vizuální změna stavu a zvuková odezva při detekci hráče.
- Krátká imunita hráče po zásahu, aby nedocházelo k okamžitému ukončení hry.

---

## 🏆 Systém skóre a ukládání

Aplikace obsahuje plně funkční systém pro správu výsledků:
- Před začátkem hry uživatel zadá své jméno.
- Výsledky se ukládají do souboru `score.json`.
- Hra automaticky vyhodnocuje a zobrazuje tabulku **Top 10 nejlepších hráčů**.

---

## 🧰 Použité technologie

- **Python 3.10+**
- **Pygame** (grafika, zvuk, vstupy)
- **screeninfo** (automatické přizpůsobení rozlišení monitoru)
- **JSON** (ukládání dat a nastavení)

---

## 🗂️ Struktura projektu
```
spider/
├── main.py           # Vstupní bod – inicializace a spuštění hry
├── game.py           # Hlavní herní logika, smyčka, kolize, zvuky
├── player.py         # Hráč (robot) – pohyb, had segmentů, imunita
├── spider.py         # Pavouk – pohyb, pronásledování, naštvaný stav
├── barrel.py         # Sud – segment hada hráče
├── food.py           # Jídlo (kapka oleje) – náhodná pozice
├── button.py         # UI tlačítko – hover, callback
├── pause_menu.py     # Menu pauzy – pokračovat, restart, nová hra, konec
├── name_input.py     # Zadávání jména hráče před hrou
├── score_json.py     # Správa skóre (ukládání/načítání JSON, vykreslení Top 10)
├── score.py          # Starší verze správy skóre (TXT) – nepoužívá se
├── settings.py       # Globální konstanty – rozměry, barvy, rychlosti, cesty k médiím
├── score.json        # Soubor s uloženými skóre (generuje se automaticky)
├── .gitignore
└── media/
    ├── fonts/        # Herní font (Super Rocky)
    ├── ico/          # Ikona okna
    ├── img/          # Obrázky hráče, pavouků, sudů, jídla, pozadí
    └── sounds/       # Hudba a zvukové efekty
```
