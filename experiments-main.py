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
    

def ledPrintTest(x,y):
    if y%2 == 0 or y == 0:
        res=(y*8+x)
    else:
        res=(y*8+7-x)
    np[res] = (5,5,5)
    np.write()
    time.sleep(5)
    np[res] = (0,0,0)
    np.write()
    
def coordsCalc(x,y):
    print("coordsCalc")
    if y%2 == 0 or y == 0:
        res=(y*8+x)
    else:
        res=(y*8+7-x)
    return res

def calcRow(rowId):
    print("calcRow")
    listCL=[]
    for i in range(0,8):
        listCL.append(coordsCalc(i,rowId))
    return listCL

def calcCol(colId):
    print("calcCol")
    listCL=[]
    for i in range(0,8):
        listCL.append(coordsCalc(colId,i))
    return listCL


def colAndLinePrint():
    print("colAndLinePrint")
    for i in range(0,8):
        columnList = calcCol(i)
        for j in columnList:
            np[j] = (5,5,5)
            np.write()
        time.sleep(0.1)
        for j in columnList:
            np[j] = (0,0,0)
            np.write()
            
    for i in range(0,8):
        rowList = calcRow(i)
        for j in rowList:
            np[j] = (5,5,5)
            np.write()
        time.sleep(0.1)
        for j in rowList:
            np[j] = (0,0,0)
            np.write()

colAndLinePrint()

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
        
