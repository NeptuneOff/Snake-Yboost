import tkinter as tk

# Configuration de la taille de la grille
LARGEUR_CASE = 50  # Taille des cases
TAILLE_GRILLE = 8  # Taille de la grille 8x8

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Grille 8x8 avec une case mobile")

# Création du canvas
canvas = tk.Canvas(fenetre, width=TAILLE_GRILLE * LARGEUR_CASE, height=TAILLE_GRILLE * LARGEUR_CASE)
canvas.pack()

# Remplissage du canvas avec la grille de cases blanches avec bordures noires
for ligne in range(TAILLE_GRILLE):
    for colonne in range(TAILLE_GRILLE):
        x1 = colonne * LARGEUR_CASE
        y1 = ligne * LARGEUR_CASE
        x2 = x1 + LARGEUR_CASE
        y2 = y1 + LARGEUR_CASE
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

# Position initiale de la case verte
pos_x, pos_y = 0, 0  # Départ en haut à gauche (0,0)

# Création de la case verte
case_verte = canvas.create_rectangle(pos_x, pos_y, pos_x + LARGEUR_CASE, pos_y + LARGEUR_CASE, fill="green")

# Fonction pour déplacer la case verte avec les flèches du clavier
def deplacer_case(event):
    global pos_x, pos_y
    if event.keysym == "Up" and pos_y > 0:
        pos_y -= LARGEUR_CASE
    elif event.keysym == "Down" and pos_y < (TAILLE_GRILLE - 1) * LARGEUR_CASE:
        pos_y += LARGEUR_CASE
    elif event.keysym == "Left" and pos_x > 0:
        pos_x -= LARGEUR_CASE
    elif event.keysym == "Right" and pos_x < (TAILLE_GRILLE - 1) * LARGEUR_CASE:
        pos_x += LARGEUR_CASE
    # Mise à jour de la position de la case verte
    canvas.coords(case_verte, pos_x, pos_y, pos_x + LARGEUR_CASE, pos_y + LARGEUR_CASE)

# Liaison des touches de flèche au déplacement
fenetre.bind("<Up>", deplacer_case)
fenetre.bind("<Down>", deplacer_case)
fenetre.bind("<Left>", deplacer_case)
fenetre.bind("<Right>", deplacer_case)


# Lancement de la boucle principale
fenetre.mainloop()
