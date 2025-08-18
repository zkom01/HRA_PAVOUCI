import pygame
import settings
import json
import os

class ScoreJson:
    """
    Spravuje skóre, včetně ukládání, načítání a zobrazení nejlepších výsledků
    ve formátu JSON.

    Tato třída obsluhuje soubor 'score.json', do kterého ukládá dosažená skóre
    ve strukturované podobě. Umožňuje načítat a zobrazovat seznam 10 nejvyšších skóre.

    Atributy:
        screen (pygame.Surface): Povrch obrazovky, na který se bude vykreslovat.
        filename (str): Název souboru se skóre, standardně 'score.json'.
        font_large (pygame.font.Font): Písmo použité pro vykreslování textu.
    """
    def __init__(self, screen, filename="score.json"):
        self.filename = filename
        self.screen = screen
        self.font_large = pygame.font.Font(settings.FONT_ROBOT_PATH, 50)

    def load_scores(self):
        """
        Načte a vrátí seřazený seznam skóre ze souboru JSON.

        Pokud soubor neexistuje nebo je poškozený, vrátí prázdný seznam.
        Data ze souboru JSON jsou převedena na seznam dvojic (jméno, skóre)
        a seřazena sestupně podle skóre.

        Vrací:
            list[tuple[str, int]]: Seřazený seznam dvojic (jméno, skóre).
        """
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, encoding="utf-8") as f:
                data = json.load(f)  # Načte JSON jako Python list/dict
        except (json.JSONDecodeError, FileNotFoundError):
            return []

        # data bude list slovníků [{"name": "Eda", "score": 100}, ...]
        skore_list = [(item["name"], int(item["score"])) for item in data]
        skore_list.sort(key=lambda x: x[1], reverse=True)

        return skore_list

    def save_score(self, player_name, player_score):
        """
        Přidá nové skóre do seznamu, seřadí jej a uloží 10 nejlepších do souboru JSON.

        Tato metoda načte stávající skóre, přidá nové, seřadí je a omezí
        seznam na 10 nejlepších výsledků, které pak uloží zpět do souboru
        'score.json'. Zajišťuje správné formátování JSON a podporu diakritiky.

        Parametry:
            player_name (str): Jméno hráče.
            player_score (int): Dosažené skóre.

        Vrací:
            list[tuple[str, int]]: Seřazený seznam 10 nejlepších skóre.
        """
        skore_list = self.load_scores()
        skore_list.append((player_name, player_score))
        skore_list.sort(key=lambda x: x[1], reverse=True)

        # Uloží jen top 10
        top10 = []  # prázdný seznam pro uložení prvních 10 záznamů
        for jmeno, score in skore_list[:10]:  # vezme prvních 10 dvojic (jmeno, score)
            zaznam = {  # vytvoří slovník s klíči "name" a "score"
                "name": jmeno,
                "score": score
            }
            top10.append(zaznam)  # přidá slovník do seznamu top10

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(top10, f, ensure_ascii=False, indent=2)
            # ensure_ascii=False → diakritika zůstane čitelná
            # indent=4 → hezky formátovaný soubor

        return skore_list[:10]

    def draw(self):
        """
        Vykreslí dialogové okno s tabulkou 10 nejlepších skóre.

        Dialog obsahuje titul "SCORE TOP10", ohraničení a pozadí.
        Načtená skóre jsou seřazena a vykreslena jako seznam jmen a
        číselných hodnot na obrazovku.
        """
        score_dialog_width = 500
        score_dialog_height = 600
        score_dialog_rect = pygame.Rect(0, 0, score_dialog_width, score_dialog_height)
        score_dialog_rect.center = (400, 500)

        pygame.draw.rect(self.screen, settings.POZADI_MENU, score_dialog_rect, border_radius=20)
        pygame.draw.rect(self.screen, settings.BORDER, score_dialog_rect, 3, border_radius=20)

        nadpis = self.font_large.render("SCORE TOP10", True, settings.BARVA_TEXTU_MENU)
        text_game_over_rect = nadpis.get_rect(center=(400, 240))
        self.screen.blit(nadpis, text_game_over_rect)
        pygame.draw.line(self.screen, settings.BORDER, (170, 270), (630, 270))

        next_line = 0
        height = 270
        for i, (jmeno, score) in enumerate(self.load_scores()):
            score_str = str(score)
            one_line_jmeno = self.font_large.render(jmeno, True, settings.BARVA_TEXTU_MENU)
            one_line_score = self.font_large.render(score_str, True, settings.BARVA_TEXTU_MENU)

            height += next_line
            one_line_jmeno_rect = one_line_jmeno.get_rect(topleft=(180, height))
            self.screen.blit(one_line_jmeno, one_line_jmeno_rect)
            one_line_score_rect = one_line_score.get_rect(topright=(620, height))
            self.screen.blit(one_line_score, one_line_score_rect)
            next_line = 50
