import pygame
import settings

class Score:
    def __init__(self, screen, filename="score.txt"):
        self.filename = filename
        self.screen = screen
        self.font_large = pygame.font.Font(settings.FONT_ROBOT_PATH, 50)


    def load_scores(self):
        skore_list = []
        try:
            with open(self.filename) as f:
                for radek in f:
                    radek = radek.strip()
                    if not radek:
                        continue
                    parts = radek.split(",")
                    if len(parts) != 2:
                        continue
                    jmeno = parts[0].strip()
                    try:
                        score = int(parts[1].strip())
                    except ValueError:
                        continue
                    skore_list.append((jmeno, score))
        except FileNotFoundError:
            # Soubor neexistuje, vrátí prázdný list
            pass
        return skore_list

    def save_score(self, player_name, player_score):
        skore_list = self.load_scores()
        skore_list.append((player_name, player_score))
        skore_list.sort(key=lambda x: x[1], reverse=True)

        with open(self.filename, "w") as f:
            for jmeno, score in skore_list[:11]:
                f.write(f"{jmeno},{score}\n")

        return skore_list[:11]

    def draw(self):
        score_dialog_width = 500
        score_dialog_height = 600
        score_dialog_rect = pygame.Rect(0, 0, score_dialog_width, score_dialog_height)
        score_dialog_rect.center = (400, 500)

        # Vyplnění pozadí dialogu (podobně jako u tlačítek)
        pygame.draw.rect(self.screen, settings.POZADI_MENU, score_dialog_rect, border_radius=20)
        # Volitelné: ohraničení dialogu
        pygame.draw.rect(self.screen, settings.BORDER, score_dialog_rect, 3,
                         border_radius=20)  # Bílý rámeček, tloušťka 3px

        nadpis = self.font_large.render("SCORE TOP10", True, settings.BARVA_TEXTU_MENU)
        text_game_over_rect = nadpis.get_rect(center=(400, 240))
        self.screen.blit(nadpis, text_game_over_rect)
        pygame.draw.line(self.screen, settings.BORDER, (170, 270),(620, 270))

        # Výpis top 10
        next_line = 0
        height = 300
        for i, (jmeno, score) in enumerate(self.load_scores()[:10], start=1):
            one_line = self.font_large.render(f"{jmeno} _____ {score}", True, settings.BARVA_TEXTU_MENU)

            height += next_line
            one_line_rect = one_line.get_rect(center=(400, height))
            self.screen.blit(one_line, one_line_rect)
            next_line = 50
