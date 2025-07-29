import pygame

class NameInput:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player_name = ""
        self.game_state = "get_player_name"
        self.cursor_visible = True
        self.cursor_timer = 0
        self.done = False

        # Barvy
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (70, 70, 70)
        self.LIGHT_GRAY = (100, 100, 100)
        self.BORDER_COLOR = (200, 200, 200)
        self.TEXT_COLOR = (255, 255, 255)

        # Fonty
        self.font_large = pygame.font.SysFont(None, 74)
        self.font_medium = pygame.font.SysFont(None, 50)

        # Input box
        self.input_box = pygame.Rect(screen.get_width() // 2 - 200, 300, 400, 50)

    def run(self):
        while not self.done:
            self.clock.tick(60)
            self.handle_events()
            self.update_cursor()
            self.draw()
        return self.player_name

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.game_state == "get_player_name":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.player_name:
                        self.game_state = "display_name"
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        if event.unicode.isprintable():
                            self.player_name += event.unicode
                    self.cursor_visible = True
                    self.cursor_timer = pygame.time.get_ticks()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == "display_name":
                        self.done = True

    def update_cursor(self):
        dt = pygame.time.get_ticks() - self.cursor_timer
        if dt > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = pygame.time.get_ticks()

    def draw(self):
        self.screen.fill(self.BLACK)
        if self.game_state == "get_player_name":
            prompt = self.font_large.render("Zadejte jméno:", True, self.WHITE)
            self.screen.blit(prompt, (self.screen.get_width() // 2 - prompt.get_width() // 2, 230))

            pygame.draw.rect(self.screen, self.GRAY, self.input_box, border_radius=30)
            pygame.draw.rect(self.screen, self.BORDER_COLOR, self.input_box, 2, border_radius=30)

            text_surface = self.font_medium.render(self.player_name, True, self.TEXT_COLOR)
            self.screen.blit(text_surface, (self.input_box.x + 20, self.input_box.y + 10))

            if self.cursor_visible:
                cursor_x = self.input_box.x + 20 + text_surface.get_width()
                cursor_y = self.input_box.y + 7
                pygame.draw.line(self.screen, self.WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + self.font_medium.get_height()), 2)

        elif self.game_state == "display_name":
            text = self.font_large.render(f"Zadané jméno: {self.player_name}", True, self.WHITE)
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))

            pokracuj = self.font_medium.render("Klikni myší pro pokračování", True, self.WHITE)
            self.screen.blit(pokracuj, (self.screen.get_width() // 2 - pokracuj.get_width() // 2, self.screen.get_height() // 2 + 60))

        pygame.display.flip()
