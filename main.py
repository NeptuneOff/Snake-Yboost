# main.py
import utime
import machine

from led_matrix import LedMatrix
from joystick import Joystick
from snake import Snake, Food

class SnakeGame:
    """
    Jeu du Snake sur une matrice 8×8, contrôlé par :
      - Joystick analogique (GPIO0, GPIO4, GPIO11)
      - Potentiomètre pour la vitesse (GPIO1)
      - Affichage du score sur la matrice après fin de partie
      - DATA WS2812B → GPIO5
    """

    def __init__(self):
        # --- BROCHES ---
        PIN_LED_MATRIX = 5    # WS2812B DATA sur GPIO5
        PIN_POT        = 1    # Potentiomètre sur GPIO1 (ADC1_CH1)

        # Initialisation de la matrice
        self.matrix = LedMatrix(pin_data=PIN_LED_MATRIX)

        # Initialisation du potentiomètre (ADC1_CH1 = GPIO1)
        self.adc_pot = machine.ADC(machine.Pin(PIN_POT))
        self.adc_pot.atten(machine.ADC.ATTN_11DB)  # plage 0–3.3V → 0–4095

        # Initialisation du joystick avec calibration automatique
        self.joystick = Joystick(threshold=300, samples=10)

        # Initialisation du serpent et de la nourriture
        self.snake = Snake(grid_size=8)
        self.food  = Food(grid_size=8)
        if self.food.position in self.snake.body:
            self.food.respawn(self.snake.body)

        self.score     = 0
        self.game_over = False

    def _show_menu(self):
        """
        Affiche un menu avant la partie :
         - Clignotement de la matrice
         - Attente de l'appui sur SW du joystick
        """
        print("=== SNAKE 8×8 ===")
        print("Appuyez sur SW pour démarrer")
        for _ in range(3):
            # Allumer tout en vert très faible
            for x in range(8):
                for y in range(8):
                    self.matrix.set_pixel(x, y, (0, 5, 0))
            self.matrix.show()
            utime.sleep_ms(200)
            self.matrix.clear()
            self.matrix.show()
            utime.sleep_ms(200)

        # Attendre que SW soit relâché puis appuyé
        while self.joystick.is_button_pressed():
            utime.sleep_ms(50)
        while not self.joystick.is_button_pressed():
            utime.sleep_ms(50)
        # Clear avant démarrage
        self.matrix.clear()
        self.matrix.show()
        # Attendre le relâchement pour démarrer
        while self.joystick.is_button_pressed():
            utime.sleep_ms(50)
        print("Début de la partie !")

    def _update_direction(self):
        """
        Lit le joystick pour changer la direction immédiatement.
        """
        direction = self.joystick.get_direction()
        if direction != 'NEUTRAL':
            self.snake.set_direction(direction)

    def _check_eat(self):
        """
        Si la tête du serpent touche la nourriture, grandir et respawn.
        """
        if self.snake.head_pos() == self.food.position:
            self.snake.eat()
            self.score += 1
            self.food.respawn(self.snake.body)

    def _draw(self):
        """
        Efface la matrice, dessine la nourriture et le serpent, puis met à jour.
        """
        self.matrix.clear()
        # Food en rouge très faible
        if self.food.position is not None:
            self.matrix.draw_food(self.food.position, color=(5, 0, 0))
        # Serpent en vert très faible
        self.matrix.draw_snake(self.snake.body, color=(0, 5, 0))
        self.matrix.show()

    def _display_score_on_matrix(self):
        """
        Après la fin de la partie, faire défiler le score sur la matrice 8×8,
        chiffre par chiffre, en utilisant des patterns 5×7 pour chaque chiffre.
        """
        # Cartes 5×7 pour les chiffres 0–9 (chaque valeur est une colonne 7 bits, MSB non utilisé)
        digits = {
            '0': [0x7E, 0x81, 0x81, 0x81, 0x7E],
            '1': [0x00, 0x82, 0xFF, 0x80, 0x00],
            '2': [0xE2, 0x91, 0x91, 0x91, 0x8E],
            '3': [0x42, 0x81, 0x89, 0x89, 0x76],
            '4': [0x18, 0x14, 0x12, 0xFF, 0x10],
            '5': [0x4F, 0x89, 0x89, 0x89, 0x71],
            '6': [0x7E, 0x89, 0x89, 0x89, 0x72],
            '7': [0x01, 0xE1, 0x11, 0x09, 0x07],
            '8': [0x76, 0x89, 0x89, 0x89, 0x76],
            '9': [0x4E, 0x91, 0x91, 0x91, 0x7E],
        }

        # Convertir score en chaîne puis en liste de patterns
        s = str(self.score)
        patterns = [digits[c] for c in s]

        # Construire le flux de colonnes : chaque chiffre → 5 colonnes + 1 colonne vide
        stream = []
        for patt in patterns:
            stream += patt[:]
            stream.append(0x00)  # espace entre chiffres

        # Ajouter 8 colonnes vides pour voir le dernier chiffre complètement
        stream += [0x00] * 8

        # Défilement : pour chaque position de fenêtre de largeur 8 colonnes
        for offset in range(len(stream) - 7):
            self.matrix.clear()
            window = stream[offset:offset + 8]
            for x in range(8):
                col = window[x]
                for y in range(7):
                    if (col >> (6 - y)) & 0x01:
                        # Allumer pixel (x, y+1) pour centrer verticalement
                        self.matrix.set_pixel(x, y + 1, (0, 5, 0))
            self.matrix.show()
            utime.sleep_ms(200)

        # Laisser le score figé 3 s, puis éteindre
        utime.sleep_ms(3000)
        self.matrix.clear()
        self.matrix.show()

    def run(self):
        """
        Boucle principale du jeu :
          1) afficher le menu
          2) lire joystick pour orientation
          3) move serpent (collision interne → fin)
          4) check_eat()
          5) draw matrice
          6) si SW appuyé → fin
          7) lire pot → calcul délai → utime.sleep_ms(délai)
        """
        self._show_menu()

        while not self.game_over:
            # 2) orientation du serpent
            self._update_direction()

            # 3) déplacement du serpent
            alive = self.snake.move()
            if not alive:
                self.game_over = True
                break

            # 4) vérification “manger”
            self._check_eat()

            # 5) dessin sur la matrice
            self._draw()

            # 6) si SW appuyé → fin de partie
            if self.joystick.is_button_pressed():
                self.game_over = True
                break

            # 7) ajuster délai via potentiomètre
            raw = self.adc_pot.read_u16() >> 4  # 0–4095
            delay_ms = 50 + (350 * (4095 - raw) // 4095)
            utime.sleep_ms(delay_ms)

        # Animation “Game Over” (rouge très faible)
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

        # Afficher le score sur la matrice
        self._display_score_on_matrix()

if __name__ == "__main__":
    while True:
        game = SnakeGame()
        game.run()
        print("Partie terminée ! Affichage du score…")
        print("Appuyez sur SW pour une nouvelle partie.")
        # Attendre relâchement puis nouvel appui SW
        while game.joystick.is_button_pressed():
            utime.sleep_ms(50)
        while not game.joystick.is_button_pressed():
            utime.sleep_ms(50)
        while game.joystick.is_button_pressed():
            utime.sleep_ms(50)
        # Redémarre automatiquement une nouvelle partie

