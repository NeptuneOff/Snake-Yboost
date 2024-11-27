import machine
import neopixel
import time
import random
from math import sqrt


# Configuration de la broche et du nombre de LEDs
pin = machine.Pin(13)  # GPIO 13 comme broche de données
num_leds = 64  # Nombre total de LEDs de la matrice (par exemple pour 8x8)
ledsLen = 64

# Initialisation de la matrice de LEDs
np = neopixel.NeoPixel(pin, num_leds)

# Éteindre toutes les LEDs au démarrage

num_leds=64

for i in range(num_leds):
    np[i] = (0, 10, 10)
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
    if y%2 == 0 or y == 0:
        res=(y*8+x)
    else:
        res=(y*8+7-x)
    return res

def calcRow(rowId):
    listCL=[]
    for i in range(0,8):
        listCL.append(coordsCalc(i,rowId))
    return listCL

def calcCol(colId):
    listCL=[]
    for i in range(0,8):
        listCL.append(coordsCalc(colId,i))
    return listCL


def colAndLinePrint():
    for i in range(0,8):
        columnList = calcCol(i)
        for j in columnList:
            np[j] = (10,0,0)
            np.write()
        time.sleep(0.1)
        for j in columnList:
            np[j] = (0,0,0)
            np.write()
            
    for i in range(0,8):
        rowList = calcRow(i)
        for j in rowList:
            np[j] = (10,0,0)
            np.write()
        time.sleep(0.1)
        for j in rowList:
            np[j] = (0,0,0)
            np.write()

#colAndLinePrint()

class apple:
    def __init__(self):
        self.color = (10,0,0)
        self.x = 0
        self.y = 0
        
        
    def pop (self):
        self.x = random.randint(0,7)
        self.y = random.randint(0,7)
        
pomme = apple()
pomme.pop()

npx = pomme.x
npy = pomme.y
npCo = coordsCalc(npx,npy)
print(npCo,npx,npy)
np[npCo] = (10,0,0)
np.write()


butUp = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
butDown = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
butLeft = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)
butRight = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)
butSTOP = machine.Pin(23, machine.Pin.IN, machine.Pin.PULL_UP)


npx = pomme.x
npy = pomme.y
npCo = coordsCalc(npx,npy)
print(npCo,npx,npy)
np[npCo] = (10,0,0)
np.write()

buttonMove = True



while buttonMove == True :
    if not butUp.value():
        np[npCo] = (0,0,0)
        if npy < 7:
            npy +=1
        npCo=coordsCalc(npx,npy)
        np[npCo] = (10,0,0)
        np.write()
        
    if not butDown.value():
        np[npCo] = (0,0,0)
        if npy > 0:
            npy-=1
        npCo=coordsCalc(npx,npy)
        np[npCo] = (10,0,0)
        np.write()
        
        
    if not butSTOP.value():
        buttonMove = False
    time.sleep(0.1)
