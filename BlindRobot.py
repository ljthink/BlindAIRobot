import numpy as np
import copy
import math


file = open('Map.txt', 'r')
mainl = file.read().split()
dimensions = int(math.sqrt(len(mainl)))

mL = []
for row in range(dimensions):
    inner_list = []
    for col in range(dimensions):
        inner_list.append(0)
    mL.append(inner_list)


for temp in range(len(mainl)):
    mL[int(temp/dimensions)][temp % dimensions] = mainl[temp]
    if 'A' == mainl[temp]:
        pA = temp
    elif 'B' == mainl[temp]:
        pB = temp
    elif 'G' == mainl[temp]:
        pG = temp


def DepthFirst(start, last, mL, L):
    s = (int(start/len(mL)), start%len(mL))
    l = (int(last/len(mL)), last%len(mL))
    update = [(s, [s])]
    check = []
    while update:
        (node, main) = update.pop()
        for n in L[node[1] + node[0]*len(mL)]:
            row = int(n/len(mL))
            column = n%len(mL)
            if (row, column) == l:
                return main + [l]
            else:
                if (row,column) not in check:
                    check.append((row, column))
                    update.append(((row,column), main + [(row,column)]))


def make(dir,x,mainl, dimensions):
    i = int(x/dimensions)
    j = x%dimensions
    if 'UP' == dir and i != 0:
        if mainl[i-1][j] != '0':
            i = i-1
    if 'RIGHT' == dir and j != dimensions-1:
        if mainl[i][j+1] != '0':
            j = j+1
    if 'DOWN' == dir and i != dimensions-1:
        if mainl[i+1][j] != '0':
            i = i+1
    if 'LEFT' == dir and j != 0:
        if mainl[i][j-1] != '0':
            j = j-1
    return j + i*dimensions

def Apathsearch(mL, start, stop, m):
    check = {}
    update = {}
    temp2 = len(mL)
    s = (int(start/temp2),start%temp2)
    stopCoord = (int(stop/temp2), stop%temp2)

    update[(s[0], s[1])] = (s, 0, 0, None)
    while update:
        l = None
        lK = None
        for K, count in update.items():
            if l is None or count[1] < l[1]:
                l = count
                lK = K
            del update[lK]
            cur = l
            break
        #cur = less(update)
        if cur[0] == stopCoord:
            temp = []
            while cur[3] != None:
                temp.insert(0,cur[0])
                cur = cur[3]
            temp.insert(0, cur[0])
            return temp[::-1]
        check[(cur[0][0], cur[0][1])] = cur

        for x in m[cur[0][1] + cur[0][0]*temp2]:
            row = int(x/temp2)
            column = x%temp2
            if (row,column) in list(check.keys()):
                continue
            dest = cur[2] + 1
            update2 = dest + sum(abs(a-b) for a,b in zip((row,column),stopCoord))
            last = check[(cur[0][0], cur[0][1])]

            try:
                nNode = update[(row,column)]
                if nNode[2] > dest:
                    update[(row,column)][1] = update2
                    update[(row,column)][2] = dest
                    update[(row,column)][3] = last
            except KeyError:
                update[(row,column)] = ((row, column), update2, dest, last)

def checkDirs(main, nMain, dimensions):

    i,j = main
    k = j + i*dimensions
    nIndex = nMain[k]


    neighbors = [[int(i/dimensions), i%dimensions] for i in nMain[k]]
    if sorted([[i+1,j], [i, j+1]]) == sorted(neighbors):
        return True
    if sorted([[i-1,j], [i, j+1]]) == sorted(neighbors):
        return True
    if sorted([[i+1,j], [i, j-1]]) == sorted(neighbors):
        return True
    if sorted([[i-1,j], [i, j-1]]) == sorted(neighbors):
        return True

    return False


tempM = {}
a = len(mL)**2
b = len(mL)
temp = 0

for x in range(a):
    if x == a-1:
        tempM[x] = [x-1, x-b]
    elif x == (a-b):
        tempM[x] = [x-b, x+1]
    elif x == 0:
        tempM[x] = [x+1, x+b]
    elif x ==  b-1:
        tempM[x] = [x+b, x+1]
    elif x % b ==  b-1:
        tempM[x] = [x-b, x+b, x-1]
    elif int(x/b) == 0:
        tempM[x] = [x-1, x+1, x+b]
    elif int(x/b) ==  b-1:
        tempM[x] = [x-1, x+1, x-b]
    elif x % b == 0:
        tempM[x] = [x+b, x-b, x+1]
    else:
        tempM[x] = [x+1, x-1, x+b, x-b]

m = copy.deepcopy(tempM)
for key,val in m.items():
    for elem in val:
        r = int(elem/b)
        c = elem%b
        if mL[r][c] == '0':
            tempM[key].remove(elem)


m = copy.deepcopy(tempM)



avai = []
temp = 0

for i in range(len(mL)):
    for j in range(len(mL[0])):
        if mL[i][j] == '1' and checkDirs([i, j], m, len(mL)):
            avai.append(j + i*len(mL))

near = None
nearP = None
for z in avai:

    if DepthFirst(pB, z, mL, m) != None and DepthFirst(pA, z, mL, m) != None:
        main = Apathsearch(mL, pB, z, m)

        if near is None:
            near = z
            nearP = main
        elif len(nearP) > len(main):
            nearP = main
            near = corner
nearP.reverse()





def finalP(temp, x, y, mL):
    tempL = []
    for corner,num in enumerate(temp):
        if corner != 0:
            dir = ""
            a,c = temp[corner-1]
            b,d = num

            if a-b == -1:
                dir = 'DOWN'

            elif a-b == 1:
                dir = 'UP'

            elif c-d == 1:
                dir = 'LEFT'

            else:
                dir = 'RIGHT'
        else:
            continue
        tempL.append(dir)

    tempA = x
    tempB = y
    for d in tempL:
        tempA = make(d, tempA, mL, len(mL))
        tempB = make(d, tempB, mL, len(mL))

    return tempA, tempB, tempL
main = []
updB = pB
updA = pA

updA, updB, directionsList = finalP(nearP, updA, updB, mL)
main.extend(directionsList)

i = 0
while i < len(mL):
    if updA == updB:
        break

    elif i%2 == 1:
        pathCorner = Apathsearch(grid, updA, updB, matrix)
    elif i%2 == 0:
        pathCorner = Apathsearch(mL, updB, updA, m)
    pathCorner.reverse()


    updA, updB, directionsList = finalP(pathCorner, updA, updB, mL)

    main.extend(directionsList)
    i += 1

Answer = Apathsearch(mL, updB, pG, m)

Answer.reverse()
temp1, temp2, directionsList = finalP(Answer, updA, updB, mL)
main.extend(directionsList)
print(f'Final Sequence: {main}')
