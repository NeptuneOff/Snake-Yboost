import machine
import neopixel
import time
import random
from math import sqrt


pin = machine.Pin(13) 
num_leds = 64
ledsLen = 64


np = neopixel.NeoPixel(pin, num_leds)



num_leds=64



goPrint = [
    [1,6],[2,6],[5,6],[6,6],
    [0,5],[4,5],[7,5],
    [0,4],[2,4],[4,4],[7,4],
    [0,3],[2,3],[4,3],[7,3],
    [1,2],[2,2],[5,2],[6,2]]





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

def turnOffAll():
    for i in range(0,64):
        np[i]=(0,0,0)
    np.write()

def scorePrint(score):
    turnOffAll()


for e in goPrint:
    np[coordsCalc(e[0],e[1])] = (10,10,10)
    np.write()
time.sleep(3)
turnOffAll()


class apple:
    def __init__(self):
        self.color = (10,0,0)
        self.x = 0
        self.y = 0
        
        
    def generate (self):
        self.x = random.randint(0,7)
        self.y = random.randint(0,7)
        
pomme = apple()
pomme.generate()



butUp = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
butDown = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
butLeft = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)
butRight = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)
butSTOP = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)

npx = 0
npy = 3
npCo = coordsCalc(npx,npy)
np[npCo] = (0,0,10)
np.write()
direction = "up"

dontPop = False

snakeMoving=True

con = [[0,3],[0,2],[0,1]]
cod = [[0,4],[0,3],[0,2]]

for element in con:
    np[coordsCalc(element[0],element[1])] = (0,0,10)
    np.write()

pomme.generate()
pommeCo = coordsCalc(pomme.x,pomme.y)
while np[pommeCo] == (0,0,10):
    pomme.generate()
    pommeCo = coordsCalc(pomme.x,pomme.y)
np[pommeCo]=(0,10,0)
np.write()

appleEatAmout = 0

while snakeMoving == True:
    if not butUp.value() and direction != "down":
        direction = "up"
    if not butDown.value() and direction != "up":
        direction = "down"
    if not butRight.value() and direction != "left":
        direction = "right"
    if not butLeft.value() and direction != "right":
        direction = "left"

    if direction == "up" and npy < 7:
        npy += 1
    elif direction == "up":
        npy = 0

    if direction == "down" and npy > 0:
        npy -= 1
    elif direction == "down":
        npy = 7

    if direction == "right" and npx < 7:
        npx += 1
    elif direction == "right":
        npx = 0

    if direction == "left" and npx > 0:
        npx -= 1
    elif direction == "left":
        npx = 7

    con.insert(0,[npx,npy])
    np[coordsCalc(con[len(con)-1][0],con[len(con)-1][1])] = (0,0,0)
    


    npCo=coordsCalc(npx,npy)

    if np[npCo] == (0,0,10):
        snakeMoving = False
    
    elif np[npCo] == (0,10,0):
        dontPop = True

    if snakeMoving != False :
        np[npCo] = (0,0,10)  

    if dontPop == True:
        dontPop = False
        pomme.generate()
        pommeCo = coordsCalc(pomme.x,pomme.y)
        while np[pommeCo] == (0,0,10):
            pomme.generate()
            pommeCo = coordsCalc(pomme.x,pomme.y)
        np[pommeCo]=(0,10,0)

        appleEatAmout +=1
        
    else:
        con.pop()
    if snakeMoving == False:
        for k in range (0,3):
            for i in range(0,64):
                np[i] = (2,0,0)
            np.write()
            time.sleep(0.1)

            for j in range(0,64):
                np[j] = (0,0,0)
            np.write()
            time.sleep(0.1)
        scorePrint(appleEatAmout)

    np.write()     




    if not butSTOP.value():
        snakeMoving = False
        np[npCo] = (0,0,0)
        np.write()
        print("ARRET")

    time.sleep(0.3)


for j in range(0,64):
    np[j] = (0,0,0)
np.write() 