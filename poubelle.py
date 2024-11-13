import random


tabaa = [0,  1,  2,  3,  4,  5,  6,  7,
       8,  9,  10, 11, 12, 13, 14, 15,
       16, 17, 18, 19, 20, 21, 22, 23,
       24, 25, 26, 27, 28, 29, 30, 31,
       32, 33, 34, 35, 36, 37, 38, 39,
       40, 41, 42, 43, 44, 45, 46, 47,
       48, 49, 50, 51, 52, 53, 54, 55,
       56, 57, 58, 59, 60, 61, 62, 63]

matriceTabOne = [
[64, 63, 62, 61, 60, 59, 58, 57],
[49, 50, 51, 52, 53, 54, 55, 56],
[48, 47, 46, 45, 44, 43, 42, 41],
[33, 34, 35, 36, 37, 38, 39, 40],
[32, 31, 30, 29, 28, 27, 26, 25],
[17, 18, 19, 20, 21, 22, 23, 24],
[16, 15, 14, 13, 12, 11, 10,  9],
[ 1,  2,  3,  4,  5,  6,  7,  8],]

matriceTab = [
    [63, 62, 61, 60, 59, 58, 57, 56],
    [48, 49, 50, 51, 52, 53, 54, 55],
    [47, 46, 45, 44, 43, 42, 41, 40],
    [32, 33, 34, 35, 36, 37, 38, 39],
    [31, 30, 29, 28, 27, 26, 25, 24],
    [16, 17, 18, 19, 20, 21, 22, 23],
    [15, 14, 13, 12, 11, 10,  9,  8],
    [ 0,  1,  2,  3,  4,  5,  6,  7]]


# formule : 
# le numéro de la case est égal à : (y+1)*8-(x+1)

x = random.randint(0,7)
y = random.randint(0,7)

# if y%2 == 0 or y == 0:
#     res=(y*8+x)
# else:
#     res=(y*8+7-x)

def coordsCalc(x,y):
    if y%2 == 0 or y == 0:
        res=(y*8+x)
    else:
        res=(y*8+7-x)
    return res

def calcRow(rowId):
    listCL=[]
    for i in range(0,8):
        listCL.append(coordsCalc(rowId,0))
    return listCL

def calcCol(colId):
    listCL=[]
    for i in range(0,8):
        listCL.append(coordsCalc(colId,i))
    return listCL

print(calcCol(1))

# i = 0
# p=15
# m=1

# count = -1

# tabJ = []
# tabK = []

# firstTry = True

# verif = True
# for j in range (0,8):
#     tabK = []

#     for k in range (0,8):
#         if firstTry == True:
#             firstTry = False
#             count = j
#         elif verif == True:
#             count += m
#             verif = False
#         elif verif == False:
#             count += p
#             verif = True

#         tabK.append(count)
#     firstTry = True
#     tabJ.append(tabK)
#     print(m,p)
#     p-=2
#     m+=2
#     count=-1
#     print(tabK)