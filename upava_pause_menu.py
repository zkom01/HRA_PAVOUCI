# Děkuji, že jsi mi poskytl kód pro PauseMenu. Problém spočívá ve způsobu, jakým se spouští dialogové okno s potvrzením. 
# Po kliknutí na tlačítko "NE" v potvrzovacím dialogu se sice skryje, ale v pozadí zůstává vykresleno původní menu, které se už nepřekreslí, protože se nedostane do smyčky show_menu.

# Problém
# Když uživatel klikne na "Restart" nebo "Ukončit", zobrazí se potvrzovací dialog. Pokud ale v něm klikne na "NE", metoda _confirm_action provede následující:
# Nastaví self.confirm_dialog_active = False
# Poté zavolá self.game_instance.kresleni() a self.score_list.draw()
# Toto vykreslení proběhne mimo hlavní smyčku v show_menu. Smyčka while self.paused: se pak na začátku další iterace pokusí znovu vykreslit menu, ale to původní překreslení (z _confirm_action) už není vidět, protože se překryje.
# Hlavní problém je v tom, že se v _confirm_action spouští vykreslování, které by mělo být pouze v show_menu smyčce. To vede k nekonzistentnímu stavu.

# Řešení
# Nejlepší řešení je odstranit řádky pro vykreslení z metody _confirm_action. Všechno vykreslování by mělo být centralizováno v hlavní smyčce while self.paused: v metodě show_menu.
# Když uživatel klikne na "NE", stačí pouze nastavit self.confirm_dialog_active = False. Hlavní smyčka v show_menu se o zbytek postará. Na začátku dalšího průchodu smyčkou uvidí, že self.confirm_dialog_active je False a správně vykreslí hlavní menu.

# Navrhované úpravy
# Odstraň z _confirm_action zbytečné volání vykreslování:
# Najdi metodu _confirm_action(self) ve třídě PauseMenu.
# V bloku else (pro "NE") smaž následující řádky:

self.game_instance.kresleni()
if settings.SCORE == 0 and settings.GAME_OVER:
    self.game_instance.draw_game_over()
self.score_list.draw()
# Ověř si v show_menu, že se správně vykreslí "GAME OVER" dialog:
# Tento kód už tam je, takže je to spíše kontrola. Když se menu zobrazuje, je potřeba správně vykreslit pozadí, a pokud je hra ve stavu "GAME OVER", pak i ten dialog.
# Doporučuji umístit logiku pro vykreslení herní obrazovky (včetně dialogu "GAME OVER") před vykreslením tlačítek menu.


def show_menu(self) -> str:
    # ... (původní kód)

    while self.paused:
        # 1. Znovu vykresli herní obrazovku
        self.game_instance.kresleni()

        # 2. Pokud je hra u konce, vykresli game over dialog
        if settings.GAME_OVER:
            self.game_instance.draw_game_over()

        # 3. Vykresli menu nad herní scénu
        # ... (původní kód pro vykreslování hlavního a potvrzovacího menu)
# Tato úprava zajistí, že se celý obsah obrazovky správně překreslí v každém snímku, což odstraní zmíněné chyby.


# ---- když kliknu na ukončit a potom na ANO, někdy se hra neukončí ale zobrazí se znovu menu před potvrzovacím dialogem. 
# musím znovu kliknout na ukončit a znovu na ano.

# Tenhle problém je opravdu matoucí! Děje se to proto, že potvrzovací dialog není správně ukončen a občas se vrací do hlavní smyčky menu místo toho, aby rovnou poslal signál pro ukončení hry.

# Analýza chyby
# Podívejme se na kód v metodě _confirm_action(self):
def _confirm_action(self):
    self.confirm_dialog_active = False
    if self.confirm == "ANO":
        if self.current_action_pending == "restart":
            self.restart_requested = True
            self.paused = False
        elif self.current_action_pending == "ukončit":
            self.quit_requested = True
            self.paused = False
        elif self.current_action_pending == "new_game":
            self.new_game_requested = True
            self.paused = False
    else: # Když klikneš na "NE"
        self.current_action_pending = None
        self.game_instance.kresleni()
        if settings.SCORE == 0 and settings.GAME_OVER:
            self.game_instance.draw_game_over()
        self.score_list.draw()
        
# Když klikneš na Ukončit a pak na ANO, nastaví se self.quit_requested = True a self.paused = False. To by mělo ukončit smyčku while self.paused: v metodě show_menu a vrátit hodnotu "quit".
# Problém je, že se to občas neprovede hned. Pygame potřebuje zpracovat všechny události, včetně kliknutí myší, a pokud se smyčka show_menu zrovna nachází uprostřed zpracování událostí, nemusí self.paused = False zareagovat okamžitě a smyčka while se provede ještě jednou. To způsobí, že se menu znovu vykreslí a ty musíš kliknout znovu.
# Jak to opravit
# Nejlepší řešení je nechat logiku pro ukončení hry zpracovat až po opuštění smyčky menu. Místo okamžitého nastavení self.paused = False a self.quit_requested = True přenecháme rozhodnutí na konci metody show_menu.
# Jednoduše upravíme metodu _confirm_action(self) tak, aby jen nastavila, co se má stát, a hlavní smyčka se postará o provedení.
# 1. Uprav metodu _confirm_action
# Změň kód tak, aby se logika ukončení prováděla až za smyčkou. Odstraň self.paused = False z obou podmínek, kde se nastavuje restart_requested a quit_requested. 
###############################################################################################
def _confirm_action(self):
    self.confirm_dialog_active = False
    if self.confirm == "ANO":
        if self.current_action_pending == "restart":
            self.restart_requested = True
        elif self.current_action_pending == "ukončit":
            self.quit_requested = True
        elif self.current_action_pending == "new_game":
            self.new_game_requested = True
        
        # Když uživatel potvrdí ANO, chceme opustit menu, takže nastavíme paused na False.
        self.paused = False 
    else: # Když klikneš na "NE"
        self.current_action_pending = None
        
# Vysvětlení: Teď se self.paused = False nastaví vždy, když se klikne na ANO. Tím se zajistí, že se smyčka while self.paused: okamžitě ukončí, ať už je akce restart, ukončení, nebo nová hra.
# 2. Uprav metodu show_menu
# V této metodě zajisti, že se na začátku smyčky while vždy vykreslí herní pozadí, nad kterým bude menu. To zabrání „blikání“ nebo zobrazení nekonzistentního obsahu.

def show_menu(self) -> str:
    self.paused = True
    self.quit_requested = False
    self.restart_requested = False
    self.new_game_requested = False
    self.confirm_dialog_active = False
    self.current_action_pending = None
    self.update_screen_size(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
    self.score_list.draw()

    clock = pygame.time.Clock()

    while self.paused:
        # Vždy vykresli herní pozadí pod menu
        self.game_instance.kresleni()

        # Vykreslení menu
        if not self.confirm_dialog_active:
            for button in self.buttons:
                button.draw(self.screen)
        else:
            # Vykreslení potvrzovacího dialogu
            # ... (zde ponech kód pro vykreslení dialogu a tlačítek)

        # Zpracování událostí
        for event in pygame.event.get():
            # ... (zde ponech zpracování událostí)

            if not self.confirm_dialog_active:
                for button in self.buttons:
                    button.handle_event(event)
            else:
                for button in self.confirm_buttons:
                    button.handle_event(event)

        pygame.display.flip()
        clock.tick(settings.FPS)

    # Návratová hodnota, která určí další akci
    if self.quit_requested:
        return "quit"
    elif self.restart_requested:
        return "restart"
    elif self.new_game_requested:
        return "new_game"
    else:
        return "resume"
Tím, že přesuneš self.paused = False do správného bloku a zajistíš konzistentní vykreslování, se problém vyřeší. Hra bude reagovat spolehlivě a menu se bude chovat přesně tak, jak očekáváš.
