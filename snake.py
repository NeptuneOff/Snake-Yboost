# snake.py
import random

class Snake:
    """
    Représente le serpent :
    - grid_size : taille de la grille (8)
    - body : liste de tuples (x, y), de la tête jusqu’à la queue
    - direction : 'UP','DOWN','LEFT','RIGHT'
    """

    def __init__(self, grid_size=8):
        self.grid_size = grid_size
        mid = grid_size // 2
        # Corps initial de longueur 3, vers la droite
        self.body = [(mid, mid), (mid - 1, mid), (mid - 2, mid)]
        self.direction = 'RIGHT'
        self.grow_flag = False

    def set_direction(self, new_dir):
        """
        Change la direction si ce n'est pas l'opposé.
        """
        opposites = {'UP':'DOWN', 'DOWN':'UP', 'LEFT':'RIGHT', 'RIGHT':'LEFT'}
        if opposites.get(new_dir) != self.direction:
            self.direction = new_dir

    def move(self):
        """
        Avance le serpent.  
        - Applique wrap-around.  
        - Retourne False si collision self-collision, True sinon.
        """
        head_x, head_y = self.body[0]
        if self.direction == 'UP':
            head_y -= 1
        elif self.direction == 'DOWN':
            head_y += 1
        elif self.direction == 'LEFT':
            head_x -= 1
        elif self.direction == 'RIGHT':
            head_x += 1

        # Wrap-around
        head_x %= self.grid_size
        head_y %= self.grid_size

        new_head = (head_x, head_y)

        # Collision avec le corps
        if new_head in self.body:
            return False

        self.body.insert(0, new_head)
        if self.grow_flag:
            self.grow_flag = False
        else:
            self.body.pop()
        return True

    def eat(self):
        """
        Signale que le serpent doit grandir au prochain move().
        """
        self.grow_flag = True

    def head_pos(self):
        return self.body[0]


class Food:
    """
    Gère la nourriture :
    - grid_size : taille de la grille (8)
    - position : tuple (x,y)
    """

    def __init__(self, grid_size=8):
        self.grid_size = grid_size
        self.position = None
        self.respawn([])

    def _generate_position(self, occupied):
        free_cells = [(x, y)
                      for x in range(self.grid_size)
                      for y in range(self.grid_size)
                      if (x, y) not in occupied]
        if not free_cells:
            return None
        return random.choice(free_cells)

    def respawn(self, occupied):
        """
        Crée une nouvelle position hors des cellules occupées.
        """
        self.position = self._generate_position(occupied)

