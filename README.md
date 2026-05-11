# 🕷️ Pavouci Komárkovi

Pygame hra inspirovaná klasickým hadem (Snake). Hráč ovládá robota, sbírá kapky oleje, a vyhýbá se pavoukolidem. Čím více kapek sebere, tím delší „had" sudů táhne za sebou – a tím více pavouků mu jde po krku.

---

## 🎮 Jak se hraje

| Klávesa | Akce |
|---|---|
| `←` / `A` | pohyb doleva |
| `→` / `D` | pohyb doprava |
| `↑` / `W` | pohyb nahoru |
| `↓` / `S` | pohyb dolů |
| `Mezerník` | pauza / menu |
| `F11` | přepnutí celé obrazovky |

**Cíl:** Sbírat kapky oleje a přežít co nejdéle. Za každé 3 kapky se k robotovi přidá jeden sud. Pavouci tě začnou pronásledovat, jakmile se přiblížíš – čím více sudů máš, tím více pavouků je ve hře.

**Životy:** Začínáš se 3 životy. Zásah pavouka odebere jeden sud, nebo život, pokud žádný sud nemáš.

**Imunita:** Po každém zásahu jsi na 2 sekundy imunní (robot bliká).

**Rychlost:** Hra se postupně zrychluje podle počtu sebraných kapek:
- 20 kapek → rychlost 2
- 50 kapek → rychlost 3
- 80 kapek → rychlost MAX

---

## 🕷️ Pavouci

Ve hře je 5 pavouků, kteří se postupně přidávají jak sbíráš sudy:

| Pavouk | Přidá se při |
|---|---|
| Max | hned na začátku |
| Tery | 2 sudy |
| Niky | 3 sudy |
| Eda | 4 sudy |
| Hana | 4 sudy |

Každý pavouk má **klidný** a **naštvaný** stav. Když se přiblížíš na méně než 400 px, pavouk se „naštve", změní vzhled a začne tě pronásledovat. Pokud je naštvaný alespoň jeden pavouk, pozadí hry zčervená a spustí se alarm.

---

## 🏆 Skóre

Po konci hry se tvoje skóre uloží do `score.json`. Zobrazuje se **Top 10** nejlepších výsledků. Jméno hráče (max. 7 znaků) se zadává před každou hrou.

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

---

## ⚙️ Instalace a spuštění

### Požadavky

- Python 3.10+
- pygame
- screeninfo

### Instalace závislostí

```bash
pip install pygame screeninfo
```

### Spuštění

```bash
python main.py
```

---

## 🛠️ Konfigurace

Veškerá nastavení hry jsou v souboru `settings.py`:

| Konstanta | Výchozí hodnota | Popis |
|---|---|---|
| `ZIVOTY` | `3` | Počet životů hráče |
| `POCET_KAPEK_NA_SUD` | `3` | Kapky potřebné k získání sudu |
| `PLAYER_RYCHLOST` | `10` | Základní rychlost robota |
| `SPIDER_RYCHLOST` | `6` | Základní rychlost pavouka |
| `ANGRY_VZDALENOST` | `400` | Vzdálenost (px), při které se pavouk naštve |
| `DOBA_IMUNITY` | `2000` | Délka imunity po zásahu (ms) |
| `SCREEN_WIDTH` | `1400` | Šířka okna |
| `SCREEN_HEIGHT` | `700` | Výška okna |
| `FPS` | `60` | Maximální počet snímků za sekundu |

---

## 🧩 Architektura

```
main.py
  └── inicializuje pygame, vytváří objekty
       └── Game.run()  ← hlavní smyčka
            ├── stisknute_klavesy()   – vstup od hráče
            ├── update()              – herní logika
            │    ├── prida_odebere_pavouka()
            │    ├── kontrola_kolize()
            │    ├── update_stav_is_angry()
            │    └── update_rychlosti()
            ├── hrac_group.update()   – pohyb hráče
            ├── pavouci_group.update()– pohyb pavouků
            └── kresleni()            – vykreslení
```

Komunikace mezi objekty probíhá přes `pygame.sprite.Group` a přímé reference. Globální stav hry (skóre, jméno hráče, game over) je uložen v `settings.py` jako modul-level proměnné.
