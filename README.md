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
API_ARES/
├── main.py         # Vstupní bod aplikace
├── game.py         # Hlavní herní smyčka a logika
├── player.py       # Třída hráče a správa sudů
├── spider.py       # Logika a AI nepřátel
├── barrel.py       # Mechanika připojených sudů
├── food.py         # Generování kapek oleje
├── button.py       # UI prvky (tlačítka)
├── pause_menu.py   # Logika menu a pauzy
├── score_json.py   # Modul pro práci s JSON daty
├── settings.py     # Globální konfigurace a konstanty
└── media/          # Obrázky, ikony a zvuky
```
