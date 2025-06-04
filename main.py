# main.py
import utime
import machine
import random

from led_matrix import LedMatrix
from joystick import Joystick
from snake import Snake, Food

class BotSnake:
    """
    Serpent contrôlé par l’IA en mode Hard.
    Comporte même taille que Snake, mais se déplace aléatoirement (non très fort).
    - grid_size : taille (8)
    - body, direction, grow_flag définis comme Snake
    """

    def __init__(self, grid_size=8):
        self.grid_size = grid_size
        mid = grid_size // 2
        # Corps initial au centre (4 segments verticaux vers le bas)
        self.body = [(mid, mid - 1), (mid, mid), (mid, mid + 1)]
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.grow_flag = False

    def set_direction(self, new_dir):
        opposites = {'UP':'DOWN', 'DOWN':'UP', 'LEFT':'RIGHT', 'RIGHT':'LEFT'}
        if opposites.get(new_dir) != self.direction:
            self.direction = new_dir

    def move(self):
        """
        Avance le serpent IA.  
        - Choisit aléatoirement un changement de direction
          qui n’est pas l’opposé, avec probabilité faible.
        - Retourne False si collision interne, True sinon.
        """
        # 20% de changer de direction aléatoirement
        if random.random() < 0.2:
            new_dir = random.choice(['UP','DOWN','LEFT','RIGHT'])
            self.set_direction(new_dir)

        head_x, head_y = self.body[0]
        if self.direction == 'UP':
            head_y -= 1
        elif self.direction == 'DOWN':
            head_y += 1
        elif self.direction == 'LEFT':
            head_x -= 1
        elif self.direction == 'RIGHT':
            head_x += 1

        head_x %= self.grid_size
        head_y %= self.grid_size
        new_head = (head_x, head_y)

        if new_head in self.body:
            return False

        self.body.insert(0, new_head)
        if self.grow_flag:
            self.grow_flag = False
        else:
            self.body.pop()
        return True

    def eat_poison(self):
        """
        Quand le bot mange une pomme toxique, on ne le fait pas grandir,
        mais on peut respawner la pomme toxique.
        """
        pass  # pas de croissance

    def head_pos(self):
        return self.body[0]


class SnakeGame:
    """
    Jeu du Snake 8×8 avec difficulté “Hard” :
      - Joystick analogique (GPIO0, GPIO4, GPIO11)
      - Potentiomètre pour vitesse (GPIO1)
      - Slide switch Hard/Normal (GPIO12)
      - Serpent IA (mode Hard) n’apparaît que si le joueur mange une pomme toxique
      - Pomme toxique toujours présente, respawns réguliers
      - DATA WS2812B → GPIO5
    """

    def __init__(self):
        # --- BROCHES ---
        PIN_LED_MATRIX = 5   # WS2812B DATA sur GPIO5
        PIN_POT        = 1   # Potentiomètre sur GPIO1 (ADC1_CH1)
        PIN_SWITCH     = 12  # Slide switch Hard/Normal (digital)
        # Joystick VRx=GPIO0, VRy=GPIO4, SW=GPIO11 (déjà codés dans Joystick)

        # Initialisation matrice
        self.matrix = LedMatrix(pin_data=PIN_LED_MATRIX)

        # Initialisation potentiomètre (ADC)
        self.adc_pot = machine.ADC(machine.Pin(PIN_POT))
        self.adc_pot.atten(machine.ADC.ATTN_11DB)

        # Initialisation slide switch
        self.switch = machine.Pin(PIN_SWITCH, machine.Pin.IN, machine.Pin.PULL_DOWN)

        # Initialisation joystick (calibration auto)
        self.joystick = Joystick(threshold=300, samples=10)

        # Initialisation serpent joueur et nourriture normale + toxique
        self.snake = Snake(grid_size=8)
        self.food  = Food(grid_size=8)       # Pomme normale (rouge)
        self.poison = Food(grid_size=8)      # Pomme toxique (bleu)
        # Veiller à ce qu’elles n’apparaissent pas sur le corps joueur
        if self.food.position in self.snake.body:
            self.food.respawn(self.snake.body)
        if self.poison.position in self.snake.body or self.poison.position == self.food.position:
            self.poison.respawn(self.snake.body + [self.food.position])

        self.bot = None   # Aucun bot au départ
        self.score = 0
        self.game_over = False

    def _show_menu(self):
        """
        Menu avant partie (clignotement + console).
        """
        print("=== SNAKE 8×8 ===")
        print("Appuyez sur SW pour démarrer (Switch Hard =", 
              "ON" if self.switch.value() else "OFF", ")")
        for _ in range(3):
            # Allumer matrice en vert faible
            for x in range(8):
                for y in range(8):
                    self.matrix.set_pixel(x, y, (0, 5, 0))
            self.matrix.show()
            utime.sleep_ms(200)
            self.matrix.clear()
            self.matrix.show()
            utime.sleep_ms(200)

        while self.joystick.is_button_pressed():
            utime.sleep_ms(50)
        while not self.joystick.is_button_pressed():
            utime.sleep_ms(50)
        self.matrix.clear()
        self.matrix.show()
        while self.joystick.is_button_pressed():
            utime.sleep_ms(50)
        print("Début de la partie !  Mode Hard =", "Oui" if self.switch.value() else "Non")

    def _update_direction(self):
        """
        Lit joystick pour diriger joueur, ne bloque pas.
        """
        direction = self.joystick.get_direction()
        if direction != 'NEUTRAL':
            self.snake.set_direction(direction)

    def _check_eat(self):
        """
        Gestion des pommes :
         - Si joueur mange NORMAL → incrémente score, respawn normale
         - Si joueur mange POISON → spawn bot si mode Hard & aucun bot,
                              respawn poison
        - Si bot existe et mange POISON → respawn poison,
                                        pas de croissance
        """
        # Joueur mange pomme normale ?
        if self.snake.head_pos() == self.food.position:
            self.snake.eat()
            self.score += 1
            self.food.respawn(self.snake.body + ([] if not self.bot else self.bot.body))
        # Joueur mange pomme toxique ?
        if self.snake.head_pos() == self.poison.position:
            # Respawn poison hors du corps joueur + bot
            occupied = self.snake.body + ([] if not self.bot else self.bot.body)
            self.poison.respawn(occupied)
            # Mode Hard actif et pas encore de bot → spawn bot
            if self.switch.value() == 1 and self.bot is None:
                self.bot = BotSnake(grid_size=8)
                print(">>> Bot Snake apparu !")
        # Bot mange poison ?
        if self.bot and self.bot.head_pos() == self.poison.position:
            # Respawn poison hors du corps joueur et bot
            occupied = self.snake.body + self.bot.body
            self.poison.respawn(occupied)
            # Pas de croissance ni score pour le bot

    def _update_bot(self):
        """
        Si bot existe, on le fait bouger.
        - Collision interne du bot → il meurt
        - Collision bot→joueur (bot.head sur snake.body) → game over
        """
        if not self.bot:
            return
        alive = self.bot.move()
        if not alive:
            print(">>> Bot Snake s'est auto-collidé et est mort.")
            self.bot = None
            return

        # Si bot head chute sur corps du joueur → game over pour le joueur
        if self.bot.head_pos() in self.snake.body:
            print(">>> Bot a tué le joueur !")
            self.game_over = True

    def _check_bot_collision(self):
        """
        Si joueur head chute sur le corps du bot (autre que sa tête), bot meurt.
        """
        if not self.bot:
            return
        if self.snake.head_pos() in self.bot.body[1:]:
            print(">>> Joueur a tué le bot !")
            self.bot = None

    def _draw(self):
        """
        Efface la matrice, dessine :
         - Pomme normale (rouge faible)
         - Pomme toxique (bleu faible)
         - Serpent joueur (vert faible)
         - Bot (si existe, en jaune faible)
        """
        self.matrix.clear()
        # Pomme normale
        if self.food.position is not None:
            self.matrix.draw_food(self.food.position, color=(5, 0, 0))
        # Pomme toxique (bleu très faible)
        if self.poison.position is not None:
            x, y = self.poison.position
            self.matrix.set_pixel(x, y, (0, 0, 5))
        # Serpent joueur
        self.matrix.draw_snake(self.snake.body, color=(0, 5, 0))
        # Bot (jaune très faible)
        if self.bot:
            for (x, y) in self.bot.body:
                self.matrix.set_pixel(x, y, (5, 5, 0))
        self.matrix.show()

    def _display_score_on_matrix(self):
        """
        À la fin, affiche le score figé sur la matrice 8×8.
        On centre horizontalement le nombre (max 4 chiffres).
        """
        # Cartes 5×7 pour chiffres
        digits = {
            '0': [0x3E, 0x45, 0x49, 0x51, 0x3E],  # 0
            '1': [0x00, 0x21, 0x7F, 0x01, 0x00],  # 1
            '2': [0x21, 0x43, 0x45, 0x49, 0x31],  # 2
            '3': [0x42, 0x41, 0x51, 0x69, 0x46],  # 3
            '4': [0x0C, 0x14, 0x24, 0x7F, 0x04],  # 4
            '5': [0x72, 0x51, 0x51, 0x51, 0x4E],  # 5
            '6': [0x3E, 0x49, 0x49, 0x49, 0x26],  # 6
            '7': [0x40, 0x47, 0x48, 0x50, 0x60],  # 7
            '8': [0x36, 0x49, 0x49, 0x49, 0x36],  # 8
            '9': [0x30, 0x49, 0x49, 0x4A, 0x3C],  # 9
        }


        s = str(self.score)
        # On limite à 4 chiffres max
        if len(s) > 4:
            s = s[-4:]
        patterns = [digits[c] for c in s]

        # Calculer décalage pour centrer : largeur totale = len(s)*6 - 1 (5 colonnes + 1 espace)
        total_width = len(s) * 6 - 1
        offset_x = (8 - total_width) // 2  # centrer

        # Afficher chaque chiffre à sa place, sans défilement
        self.matrix.clear()
        for i, patt in enumerate(patterns):
            base_x = offset_x + i * 6
            for col_idx in range(5):
                col = patt[col_idx]
                for row in range(7):
                    if (col >> (6 - row)) & 0x01:
                        self.matrix.set_pixel(base_x + col_idx, row + 1, (0, 5, 0))
        self.matrix.show()
        # Laisser le score visible longtemps
        utime.sleep_ms(5000)
        self.matrix.clear()
        self.matrix.show()

    def run(self):
        """
        Boucle principale du jeu :
         1) afficher menu
         2) boucle jusqu'à game_over :
            - lire joystick → dir joueur
            - déplacer joueur
            - mettre à jour bot (si existe)
            - vérifier collisions (joueur ↔ bot)
            - gérer pommes (normale + toxique)
            - dessiner tout
            - lire SW → fin
            - lire pot → délai → sleep_ms
         3) animation Game Over
         4) afficher score figé
        """
        self._show_menu()

        while not self.game_over:
            # 2.1) déplacer joueur
            self._update_direction()
            alive = self.snake.move()
            if not alive:
                self.game_over = True
                break

            # 2.2) mettre à jour bot
            if self.switch.value() and self.bot:
                self._update_bot()

            # 2.3) collisions réciproques
            if self.bot:
                self._check_bot_collision()
                if self.game_over:
                    break

            # 2.4) pommes
            self._check_eat()

            # 2.5) dessiner
            self._draw()

            # 2.6) fin si SW
            if self.joystick.is_button_pressed():
                self.game_over = True
                break

            # 2.7) délai ajusté
            raw = self.adc_pot.read_u16() >> 4
            delay_ms = 50 + (350 * (4095 - raw) // 4095)
            utime.sleep_ms(delay_ms)

        # 3) Animation Game Over (rouge très faible)
        for _ in range(3):
            self.matrix.clear()
            self.matrix.show()
            utime.sleep_ms(200)
            for x in range(8):
                for y in range(8):
                    self.matrix.set_pixel(x, y, (3, 0, 0))
            self.matrix.show()
            utime.sleep_ms(200)
        self.matrix.clear()
        self.matrix.show()

        # 4) Afficher score figé
        self._display_score_on_matrix()

if __name__ == "__main__":
    while True:
        game = SnakeGame()
        game.run()
        print("Partie terminée ! Appuyez sur SW pour rejouer.")
        # Attendre relâchement puis nouvel appui SW
        while game.joystick.is_button_pressed():
            utime.sleep_ms(50)
        while not game.joystick.is_button_pressed():
            utime.sleep_ms(50)
        while game.joystick.is_button_pressed():
            utime.sleep_ms(50)
        # Nouvelle partie

