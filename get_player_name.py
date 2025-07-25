import pygame
from button import Button  # Předpokládá se, že 'button.py' je ve stejném adresáři

# --- Inicializace Pygame ---
pygame.init()

game_state = "get_player_name"
player_name = ""
screen = pygame.display.set_mode((1400, 700))
pygame.display.set_caption("Zadej jméno")  # Nastavení titulku okna
lets_continue = True

# --- Barvy ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)  # Pro normální stav inputu
LIGHT_GRAY = (100, 100, 100)  # Pro aktivní stav inputu
BORDER_COLOR = (200, 200, 200)  # Barva okraje inputu a tlačítek
TEXT_COLOR = (255, 255, 255)  # Barva textu

# --- Fonty ---
font_large = pygame.font.SysFont(None, 74)  # Pro nadpis/instrukce
font_medium = pygame.font.SysFont(None, 50)  # Pro zadané jméno / input pole

# --- Vzhled input pole ---
INPUT_NORMAL_COLOR = GRAY
INPUT_ACTIVE_COLOR = LIGHT_GRAY
INPUT_BORDER_COLOR = BORDER_COLOR
INPUT_TEXT_COLOR = TEXT_COLOR

# --- Nastavení pro blikající kurzor ---
CURSOR_BLINK_INTERVAL = 300  # Milisekundy (500ms = 0.5 sekundy)
cursor_visible = True
cursor_timer = 0


# --- Funkce pro přechod do hlavní hry ---
def start_main_game():
    global game_state
    game_state = "main_game"
    print(f"Jméno {player_name} potvrzeno, spouštím hlavní hru.")  # Pro kontrolu v konzoli


# --- Funkce pro potvrzení jména (callback pro tlačítko "Potvrdit") ---
def confirm_player_name():
    global game_state
    if player_name:  # Potvrdit pouze pokud jméno není prázdné
        game_state = "display_name"


# --- Tlačítko pro potvrzení jména ---
# Bude vedle input pole
confirm_button = Button("OK",
                        screen.get_width() // 2 + 220,  # X pozice: napravo od inputu
                        300,  # Stejná Y pozice jako input pole
                        80, 50,  # Šířka a výška
                        confirm_player_name)  # Callback funkce

# --- Tlačítko pro pokračování (po zobrazení jména) ---
continue_button = Button("Pokračovat",
                         screen.get_width() // 2 - 100,  # X pozice - vycentrování
                         screen.get_height() // 2 + 100,  # Y pozice pod zobrazeným jménem
                         200, 50,  # Šířka a výška
                         start_main_game)  # Callback funkce

# --- Hlavní smyčka ---
while lets_continue:
    # Získání uplynulého času pro blikání kurzoru
    dt = pygame.time.get_ticks() - cursor_timer
    if dt > CURSOR_BLINK_INTERVAL:
        cursor_visible = not cursor_visible
        cursor_timer = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

        # Zpracování událostí pro vstup jména
        if game_state == "get_player_name":
            # Tlačítko Potvrdit zpracovává události
            confirm_button.handle_event(event)

            if event.type == pygame.KEYDOWN:
                # Už Enter nebude potvrzovat jméno, pouze backspace a tisknutelné znaky
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if event.unicode.isprintable():
                        player_name += event.unicode
                # Reset kurzoru při každé změně textu
                cursor_timer = pygame.time.get_ticks()
                cursor_visible = True

        # Zpracování událostí pro tlačítko "Pokračovat"
        elif game_state == "display_name":
            continue_button.handle_event(event)

    # --- Vykreslování ---
    if game_state == "get_player_name":
        screen.fill(BLACK)

        # Nadpis "Zadejte své jméno:"
        prompt_text = font_large.render("Zadejte jméno:", True, WHITE)
        screen.blit(prompt_text, (screen.get_width() // 2 - prompt_text.get_width() // 2, 230))

        # Vstupní pole
        input_box = pygame.Rect(screen.get_width() // 2 - 200, 300, 400, 50)

        # Vykreslení pozadí a okraje input pole
        pygame.draw.rect(screen, INPUT_NORMAL_COLOR, input_box, border_radius=30)
        pygame.draw.rect(screen, INPUT_BORDER_COLOR, input_box, 2, border_radius=30)

        # Text uvnitř input pole
        input_text_surface = font_medium.render(player_name, True, INPUT_TEXT_COLOR)
        screen.blit(input_text_surface, (input_box.x + 20, input_box.y + 10))

        # Vykreslení blikajícího kurzoru
        if cursor_visible:
            # Vypočítáme pozici kurzoru na konci textu
            cursor_x = input_box.x + 20 + input_text_surface.get_width()
            cursor_y = input_box.y + 7
            cursor_height = font_medium.get_height()
            pygame.draw.line(screen, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

        # Vykreslení tlačítka "Potvrdit"
        confirm_button.draw(screen)

        pygame.display.flip()

    elif game_state == "display_name":
        screen.fill(BLACK)

        # Vykreslení zadaného jména
        display_text = font_large.render(f"Zadané jméno: {player_name}", True, WHITE)
        screen.blit(display_text, (screen.get_width() // 2 - display_text.get_width() // 2,
                                   screen.get_height() // 2 - display_text.get_height() // 2))

        # Vykreslení tlačítka "Pokračovat"
        continue_button.draw(screen)

        pygame.display.flip()

    elif game_state == "main_game":
        screen.fill((50, 50, 150))  # Modré pozadí pro hlavní hru
        main_game_text = font_large.render(f"Vítejte ve hře, {player_name}!", True, WHITE)
        screen.blit(main_game_text, (screen.get_width() // 2 - main_game_text.get_width() // 2,
                                     screen.get_height() // 2 - main_game_text.get_height() // 2))
        pygame.display.flip()

# --- Ukončení Pygame ---
pygame.quit()