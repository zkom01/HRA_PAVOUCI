class Score:
    def __init__(self, filename="score.txt"):
        self.filename = filename

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
        #
        # # Výpis top 10
        # for i, (jmeno, score) in enumerate(skore_list[:10], start=1):
        #     print(f"{i}. Jméno: {jmeno} Score: {score}")

        return skore_list[:11]
