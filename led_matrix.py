# led_matrix.py
import machine
import neopixel

class LedMatrix:
    """
    Gestion d'une matrice WS2812B 8x8 en zigzag.
    - pin_data : numéro de la broche GPIO connectée à la ligne Data de la matrice.
    - width : largeur (8)
    - height : hauteur (8)
    """

    def __init__(self, pin_data, width=8, height=8):
        self.width = width
        self.height = height
        self.n_pixels = width * height
        self.pin = machine.Pin(pin_data, machine.Pin.OUT)
        # Initialisation de NeoPixel (WS2812)
        self.np = neopixel.NeoPixel(self.pin, self.n_pixels)

    def clear(self):
        """Éteint tous les pixels."""
        for i in range(self.n_pixels):
            self.np[i] = (0, 0, 0)
        self.np.write()

    def _coord_to_index(self, x, y):
        """
        Convertit (x,y) en index linéaire selon le motif zigzag.
        """
        if y < 0 or y >= self.height or x < 0 or x >= self.width:
            return None
        if (y % 2) == 0:
            # Ligne “pair” (y=0,2,4,…) : sens gauche→droite
            idx = y * self.width + x
        else:
            # Ligne “impair” : sens droite→gauche
            idx = y * self.width + (self.width - 1 - x)
        return idx

    def set_pixel(self, x, y, color):
        """
        Définit le pixel (x,y) à la couleur (r,g,b).
        - color : tuple (R, G, B) avec valeurs 0–255.
        """
        idx = self._coord_to_index(x, y)
        if idx is not None:
            self.np[idx] = color

    def show(self):
        """Envoie les données à la matrice."""
        self.np.write()

    def draw_snake(self, snake_body, color=(0, 255, 0)):
        """
        Dessine le serpent sur la matrice.
        - snake_body : liste de tuples (x, y).
        - color : couleur du serpent.
        """
        for (x, y) in snake_body:
            self.set_pixel(x, y, color)

    def draw_food(self, food_pos, color=(255, 0, 0)):
        """
        Dessine la nourriture.
        - food_pos : tuple (x, y).
        - color : couleur de la bouffe.
        """
        x, y = food_pos
        self.set_pixel(x, y, color)

