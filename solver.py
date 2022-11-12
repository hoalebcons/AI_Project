# AI Assignment 1 - Bloxorz

import time
import copy
import sys
import queue as Q

def readMap(fileMap):
    with open(fileMap) as f:
        MAP_ROW, MAP_COL, xStart, yStart = [int(x) for x in next(f).split()] # read first line
        sourceMap = []
        countMapLine = 1
        for line in f: # read map
            countMapLine += 1
            sourceMap.append([int(x) for x in line.split()])
            if countMapLine > MAP_ROW: break

        # read managedBoard
        manaBoa = []
        for line in f: 
            manaBoa.append([int(x) for x in line.split()])

    print("\nYOUR MAP LOOK LIKE THIS:")
    for item in sourceMap:
        print(item)
    print("Start at (",xStart, ",", yStart,")")
    print("Manage Board:")
    for item in manaBoa:
        print(item)
    print("======================================")
    return MAP_ROW, MAP_COL, xStart, yStart, sourceMap, manaBoa

def deltatime(start_time):
    result = time.time() - start_time
    print("Time: ", result)

class Block:

    def __init__(self, x, y, rot, parent, board, dir="", x1=None, y1=None):
        self.x      = x
        self.y      = y
        self.rot    = rot  
        self.parent = parent
        self.board  = copy.deepcopy(board)
        self.dir    = dir
        self.x1     = x1
        self.y1     = y1

    def move_up(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.dir)
        
        newBlock.dir = "U"

        if self.rot == "STANDING":
            newBlock.y -= 2 
            newBlock.rot = "LAYING_Y"

        elif newBlock.rot == "LAYING_X":
            newBlock.y -= 1
        
        elif newBlock.rot == "LAYING_Y":
            newBlock.y -= 1
            newBlock.rot = "STANDING"
        
        return newBlock 

    def move_down(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.dir)

        newBlock.dir = "D"
        
        if newBlock.rot == "STANDING":
            newBlock.y += 1
            newBlock.rot = "LAYING_Y"

        elif newBlock.rot == "LAYING_X":
            newBlock.y += 1

        elif newBlock.rot == "LAYING_Y":
            newBlock.y += 2
            newBlock.rot = "STANDING"
        return newBlock 

    def move_right(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.dir)

        newBlock.dir = "R"
    
        if newBlock.rot == "STANDING":
            newBlock.x += 1
            newBlock.rot = "LAYING_X"

        elif newBlock.rot == "LAYING_X":
            newBlock.x += 2
            newBlock.rot = "STANDING"

        elif newBlock.rot == "LAYING_Y":
             newBlock.x += 1
        return newBlock

    def move_left(self):
        newBlock = Block(self.x, self.y, self.rot, self, self.board, self.dir)

        newBlock.dir = "L"
        
        if newBlock.rot == "STANDING":
            newBlock.rot = "LAYING_X"
            newBlock.x -= 2

        elif newBlock.rot == "LAYING_X":
            newBlock.x -= 1
            newBlock.rot = "STANDING"

        elif newBlock.rot == "LAYING_Y":
            newBlock.x -= 1

        return newBlock 

    def disPlayPath(self):
        if self.rot != "SPLIT":
            print(self.dir)
    
    def disPlayPosition(self):
        if self.rot != "SPLIT":
            print(self.rot, self.x, self.y)
        else:
            print(self.rot, self.x, self.y, self.x1, self.y1)
    
    def disPlayBoard(self):
        
        # local definition
        x   = self.x
        y   = self.y
        x1  = self.x1
        y1  = self.y1
        rot = self.rot
        board = self.board

        if rot != "SPLIT":
            for i in range(len(board)): # for ROW
                print("",end='  ')
                for j in range(len(board[i])): # for COL in a ROW

                    if (i==y and j==x and rot=="STANDING") or \
                            ((i==y and j==x) or (i==y and j==x+1) and rot=="LAYING_X") or \
                            ((i==y and j==x) or (i==y+1 and j==x) and rot=="LAYING_Y"):

                        print("x",end=' ')

                    elif(board[i][j]==0):
                        print(" ",end=' ')
                    else:
                        print(board[i][j], end=' ')
                print("")
        else: # CASE SPLIT
                print("")
            
    
# Case 3: X Toggle
def isNumberThree(block,x,y):
    board = block.board

    for item in ManaBoa:

        if (x,y) ==  (item[0], item[1]):

            # TOGGLEEEE

            numToggle = item[2]   # num toggle
            index = 2   # index to check more element

            for i in range(numToggle):    # traverse toggle array
                bX = item[2*i+3]
                bY = item[2*i+4]
                if board[bX][bY] == 0:
                    board[bX][bY] = 1
                else:
                    board[bX][bY] = 0
        
            index = index + 1 + 2 * numToggle

            # CLOSEEEE

            # check if "item" has more element
            if index < len(item):   # case has more

                # read num close
                numClose = item[index]

                # traverse list close if num > 0
                for i in range(numClose):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=0

                index = index + 1 + 2 * numClose
            

            # OPEENNNN

            # check if "item" has more element
            if index < len(item):   # case also has more item
                # get num open
                numOpen = item[index]

                # traverse list open if num > 0
                for i in range(numOpen):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=1



# Case 4: Circle - Close Switch
def isNumberFour(block,x,y):
    board = block.board
    
    #print("(x-y) = (", x,"-", y,")")

    for item in ManaBoa:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 0

# Case 5: Circle Toggle
def isNumberFive(block,x,y):
    board = block.board

    for item in ManaBoa:
        if (x,y) ==  (item[0], item[1]):


            numToggle = item[2]     # numtoggle
            index = 2   # index to check more element

            for i in range(numToggle):
                bX = item[2*i+3]
                bY = item[2*i+4]
                if board[bX][bY] == 0:
                    board[bX][bY] = 1
                else:
                    board[bX][bY] = 0
            
            index = index + 1 + 2 * numToggle

            # CLOSEEEE

            # check if "item" has more element
            if index < len(item):   # case has more

                # read num close
                numClose = item[index]
                    
                # traverse list close if num > 0
                for i in range(numClose):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=0

                index = index + 1 + 2 * numClose
            

            # OPEENNNN

            # check if "item" has more element
            if index < len(item):   # case also has more item
                # get num open
                numOpen = item[index]

                # traverse list open if num > 0
                for i in range(numOpen):
                    bX = item[index+2*i+1]
                    bY = item[index+2*i+2]
                    board[bX][bY]=1


# Case 6: Circle - Open Switch
def isNumberSix(block,x,y):
    board = block.board

    for item in ManaBoa:
        if (x,y) ==  (item[0], item[1]):
            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 1

# Case 7: Split

# Case 8: X - Open Switch
def isNumberEight(block,x,y):
    board = block.board

    for item in ManaBoa:
        if (x,y) ==  (item[0], item[1]):

            num = item[2]
            for i in range(num):
                bX = item[2*i+3]
                bY = item[2*i+4]
                board[bX][bY] = 1


def isFloor(block):
    x = block.x
    y = block.y
    rot = block.rot
    board = block.board
    
    
    if x >= 0 and y >= 0 and \
            y < MAP_ROW and x < MAP_COL and \
            board[y][x] != 0:

        if rot == "STANDING":
            return True
        elif rot == "LAYING_Y":
            if y+1 < MAP_ROW and board[y+1][x] != 0 :
                return True
        elif rot == "LAYING_X":
            if x+1 < MAP_COL and board[y][x+1] != 0 :
                return True
        else: # case SPLIT
            x1 = block.x1
            y1 = block.y1

            if x1 >= 0 and y1 >= 0 and \
                y1 < MAP_ROW and x1 < MAP_COL and \
                board[y1][x1] != 0:
                    return True

    else:
        return False


# isValidBLock - Case Solution
def isValidBlock(block):
    
    if isFloor(block):
        
        # local definition
        x     = block.x
        y     = block.y
        x1    = block.x1
        y1    = block.y1
        rot   = block.rot
        board = block.board
        
        
        # Case 2: Red_Floor
        if rot == "STANDING" and board[y][x] == 2:
            return False 

        # Case 3: X Toggle 
        if rot == "STANDING" and board[y][x] == 3:
            isNumberThree(block,x,y)
        
        # Case 4: Circle - Close switch
        if board[y][x] == 4:
            isNumberFour(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 4:
            isNumberFour(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 4:
            isNumberFour(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 4:
            isNumberFour(block,x1,y1)


        # Case 5: Circle Toggle
        if board[y][x] == 5:
            isNumberFive(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 5:
            isNumberFive(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 5:
            isNumberFive(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 5:
            isNumberFive(block,x1,y1)

        # Case 6: Circle - Open Switch
        if board[y][x] == 6:
            isNumberSix(block,x,y)
        if rot == "LAYING_X" and board[y][x+1] == 6:
            isNumberSix(block,x+1,y)
        if rot == "LAYING_Y" and board[y+1][x] == 6:
            isNumberSix(block,x,y+1)
        if rot == "SPLIT" and board[y1][x1] == 6:
            isNumberSix(block,x1,y1)

        # Case 7: Split 

        # Case 8: X - Open Switch
        if rot == "STANDING" and board[y][x] == 8:
            isNumberEight(block,x,y)
            
        return True
    else:
        return False

def isGoal(block):
    x = block.x
    y = block.y
    rot = block.rot
    board = block.board

    if rot == "STANDING" and  \
        board[y][x] == 9:
        return True
    else:
        return False


def isVisited(block):
    if block.rot != "SPLIT":

        for item in passState:
            if item.x == block.x     and item.y == block.y and \
                item.rot == block.rot and item.board == block.board:
                return True

    else: # case SPLIT
                return True

    return False

def move(Stack, block, flag):

    if isValidBlock(block):
        if isVisited(block):
            return False
        
        Stack.append(block)
        passState.append(block)
        return True 

    return False   

def printSuccessRoad(block):
    
    successRoad = [block]
    temp = block.parent
    
    while temp != None:
        
        if temp.rot != "SPLIT":
            newBlock = Block(temp.x, temp.y, \
                    temp.rot, temp.parent, temp.board, temp.dir)
        else: # case SPLIT
            newBlock = Block(temp.x, temp.y, \
                    temp.rot, temp.parent, temp.board, temp.x1, temp.y1)

        successRoad = [newBlock] + successRoad
        
        temp = temp.parent
    
    step = 0
    path = ""
    for item in successRoad:
        step += 1
        print("\nStep:", step, end=' >>> ')
        item.disPlayPath()
        path += item.dir
        item.disPlayPosition()
        print("=============================")
        item.disPlayBoard()

    print("=============================")
    print("THIS IS SUCCESS ROAD: ",path)
    print("CONSUME",step,"STEP")
    
# solve DFS
def DFS(block):

    board = block.board
    Stack = []
    Stack.append(block)
    passState.append(block)
    
    virtualStep = 0

    while Stack:

        current = Stack.pop()

        if isGoal(current):
            printSuccessRoad(current)
            print("CONSUME", virtualStep, "VIRTUAL STEP")
            return True
        else:
            if current.rot != "SPLIT":
                virtualStep += 4

                move(Stack,current.move_up(), "Up")
                move(Stack,current.move_right(), "Right")
                move(Stack,current.move_down(), "Down")
                move(Stack,current.move_left(), "Left")
            else: #Split
                virtualStep += 8

    return False

# solve BFS
def BFS(block):

    board = block.board
    Queue = []
    Queue.append(block)
    passState.append(block)

    virtualStep = 0

    while Queue:
        current = Queue.pop(0)

        if isGoal(current):
            printSuccessRoad(current)
            print("CONSUME", virtualStep, "VIRTUAL STEP")
            return True

        if current.rot != "SPLIT":
            virtualStep += 4

            move(Queue,current.move_up(), "up")
            move(Queue,current.move_right(), "right")
            move(Queue,current.move_down(), "down")
            move(Queue,current.move_left(), "left")
        else: #Split
            virtualStep += 8
    return False



# START PROGRAM HERE
passState = []

MAP_ROW, MAP_COL, xStart, yStart, sourceMap, ManaBoa \
                        = readMap('map/map'+sys.argv[1:][0]+'.txt')

block = Block(xStart, yStart, "STANDING", None, sourceMap)

Start_Time = time.time()

if sys.argv[1:][1] == "DFS":
    print("Solve DFS")  
    DFS(block)

elif sys.argv[1:][1] == "BFS":
    print("Solve BFS")
    BFS(block)

else:
    print("Wrong algorithms argument!")

deltatime(Start_Time)