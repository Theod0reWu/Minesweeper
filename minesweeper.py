# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:14:14 2021
    Minesweeper game. To use simply create an object of type Minesweeper.
    specifying the height, width, number of bombs and an optional seed.
    (e.g. Minesweeper(h,w,b,seed) )
    
    To uncover a square call the function .uncover(row, column). If you
    input an invalid set of coordinates or if you have already lost/won. 
    This will do nothing.
    
    To see if you won/lost look at .won and .lost 
    
    To get the state of the board, use the function .getBoardState() will 
    return a copy of the current state of the board as a list of lists.
    - the covered squares are marked as Minesweeper.ground_symbol
    - the flags are marked as Minesweeper.flag_symbol
    - the numbers of the adjacent bombs are shown, with 0 being a space (' ')
    e.g.
         1 1 1 1 1 1  
         2 # # # # 1  
       1 3 # # 2 1 1 
       1 # # # 1
    
     A call to .printBoard() will print the true state of the board
     e.g.
         1 1 1 1 1 1  
         2 @ 1 1 @ 1  
       1 3 @ 3 2 1 1 
       1 @ 3 @ 1
     
     A call to .printGui() will print the board as a player would see
    
@author: wut6
"""
import random
import time

class Minesweeper:
    flag_symbol = 'P'
    bomb_symbol = '@'
    ground_symbol = '#'
    
    stop_color = '\x1b[0m'
    bg_color = '\33[47m' #colors from 40 - 47
    
    #colors from 30 - 37
    flag_color = '\33[33m'
    bomb_color = '\33[30m'
    ground_color = '\33[38m'
    
    def __init__(self, height, width, bombs, seed = 0):
        self.height = height
        self.width = width
        self.bombs = bombs
        
        self.addedBombs = False
        self.lost = False
        self.won = False
        self.uncovered = 0
        
        self.seed = seed
        if (seed == 0):
            self.seed = time.time()
        random.seed(self.seed)
        
        self.board = []
        self.gui = []
        for y in range (0, height):
            new = [0 for i in range(width)]
            other = [Minesweeper.ground_symbol for i in range(width)]
            self.board.append(new)
            self.gui.append(other)
        
     # \ | /
     # - 9 -
     # / | \
    def addBomb(self, y, x):
        self.board[y][x] = 9
        if y > 0:
            # |
            if (self.board[y - 1][x] != 9):
                self.board[y - 1][x] += 1
            # \
            if (x > 0 and self.board[y-1][x-1] != 9):
                self.board[y-1][x-1] += 1
        if x > 0:
            # -
            if (self.board[y][x-1] != 9):
                self.board[y][x-1] += 1
            # /
            if (y < self.height-1 and self.board[y+1][x-1] != 9):
                self.board[y+1][x-1] += 1
        if y < self.height -1:
            # | 
            if (self.board[y+1][x] != 9):
                self.board[y+1][x] += 1
            # \
            if (x < self.width -1 and self.board[y+1][x+1] != 9):
                self.board[y+1][x+1] += 1
        if x < self.width - 1:
            #-
            if (self.board[y][x+1] != 9):
                self.board[y][x+1] += 1
                
            if (y > 0 and self.board[y-1][x+1] != 9):
                self.board[y-1][x+1] += 1

    def uncover(self, ay, ax):
        if (ay < 0 or ay >= self.height 
            or ax < 0 or ax >= self.width 
            or self.gui[ay][ax] != Minesweeper.ground_symbol
            or self.lost):
            return
        if (not self.addedBombs):
            i = 0
            while (i < self.bombs):
                y = random.randint(0, self.height-1)
                x = random.randint(0, self.width-1)
                if (y != ay and x != ax) and self.board[y][x] != 9:
                    self.addBomb(y, x)
                    i+=1
            self.addedBombs = True
        if (self.board[ay][ax] == 0):
            self.gui[ay][ax] = " "
            
            self.uncover(ay+1, ax-1)
            self.uncover(ay+1, ax)
            self.uncover(ay+1, ax+1)
            
            self.uncover(ay, ax-1)
            self.uncover(ay, ax+1)
            
            self.uncover(ay-1, ax-1)
            self.uncover(ay-1, ax)
            self.uncover(ay-1, ax+1)
            
        elif (self.board[ay][ax] == 9):
            self.lost = True
            self.gui[ay][ax] = Minesweeper.bomb_symbol
        else:
            self.gui[ay][ax] = self.board[ay][ax]
        self.uncovered += 1
        if (self.uncovered == self.height * self.width - self.bombs):
            self.won = True
    
    def getSeed(self):
        return self.seed
    
    def flag(self, ay, ax):
        if (ay < 0 or ay >= self.height 
            or ax < 0 or ax >= self.width 
            or self.gui[ay][ax] != Minesweeper.ground_symbol
            or self.lost):
            return
        self.gui[ay][ax] = Minesweeper.flag_symbol
        
    def unflag(self, ay, ax):
        if (ay < 0 or ay >= self.height 
            or ax < 0 or ax >= self.width 
            or self.gui[ay][ax] != Minesweeper.flag_symbol
            or self.lost):
            return
        self.gui[ay][ax] = Minesweeper.ground_symbol
        
    #printing the nums only works for boards less than three digits on either side
    def printGui(self, nums = False):
        if (nums):
            s = "  |"
            if (self.width > 10):
                for i in range(self.width):
                    s += ' ' + str(i// 10)
                print(s)
                s = "  |"
            for i in range(self.width):
                s += ' ' + str(i%10)
            print(s)
        
        print("".join(["-" for i in range(3+2*(1+len(self.gui[0])))]) )
        y = 0
        for i in self.gui:
            s = ''
            if (nums):
                s = str(y)
                y+=1
                if (y <= 10):
                    s += ' '
            
            s += "|"+Minesweeper.bg_color + " " + Minesweeper.stop_color
            for e in i:
                if (e != Minesweeper.bomb_symbol):
                    s += Minesweeper.bg_color
                else:
                    s += '\33[43m'
                
                if (e == 1):
                    s += '\33[34m'
                elif (e == 2):
                    s += '\33[32m'
                elif (e == 3): #or e == Minesweeper.flag_symbol
                    s += '\33[33m'
                elif (e == 4):
                    s += '\33[36m'
                elif (e == 5 or e == Minesweeper.flag_symbol):
                    s += '\33[31m'
                elif (e == 6):
                    s += '\33[36m'
                elif (e == 7 or e == Minesweeper.bomb_symbol):
                    s += '\33[30m'
                elif (e == 8):
                    s += '\33[35m'
                
                if (e == Minesweeper.flag_symbol):
                    s += '\33[4m'
                s+=str(e)
                s += Minesweeper.stop_color + Minesweeper.bg_color + " " + Minesweeper.stop_color
            s+="|"
            print(s)
        print("".join(["-" for i in range(3+2*(1+len(self.gui[0])))]) )
        
    def getBoardState(self):
        copy = []
        for i in self.gui:
            copy.append(i[:])
        return copy
                    
    def printBoard(self): #debug print
        for i in self.board:
            s = ''
            for e in i:
                if e == 9:
                    s += Minesweeper.bomb_symbol
                else:
                    s += str(e)
                s += ' '
            print(s)
  