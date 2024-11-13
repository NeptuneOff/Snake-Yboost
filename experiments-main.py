import machine
import neopixel
import time
import random
from math import sqrt

# Configuration de la broche et du nombre de LEDs
pin = machine.Pin(5)  # GPIO 13 comme broche de données
num_leds = 64  # Nombre total de LEDs de la matrice (par exemple pour 8x8)
ledsLen = 64

# Initialisation de la matrice de LEDs
np = neopixel.NeoPixel(pin, num_leds)

# Éteindre toutes les LEDs au démarrage

num_leds=64

for i in range(num_leds):
    np[i] = (5, 5, 5)
    np.write()  # Envoie les données pour éteindre toutes les LEDs
    time.sleep(0.01)
    np[i] = (0, 0, 0)
    np.write()  # Envoie les données pour éteindre toutes les LEDs
    



class apple:
    def __init__(self):
        self.color = (255,0,0)
        self.x = 0
        self.y = 0
        
        
    def pop (self):
        self.x = random.randint(0,7)
        self.y = random.randint(0,7)
        
pomme = apple()
pomme.pop()
print(pomme.x)



class matrice:
    def __init__(self):
        self.size=sqrt(ledsLen)
        
