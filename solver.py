# -*- coding: utf-8 -*-
"""
Created on Wed May 26 17:34:44 2021

@author: wut6
"""

from minesweeper import Minesweeper
import time
import os

def animate(m, duration = .05):
    #print(chr(27) + "[2J")
    os.system('cls' if os.name == 'nt' else 'clear')
    m.printGui()
    time.sleep(duration)

def solve(m = Minesweeper(10,10,10), anim = False):
    
    uncoverNext = [[0,0]]
    while (len(uncoverNext) > 0 and not m.won and not m.lost):
        for coord in uncoverNext:
            if (anim):
               animate(m)
            m.uncover(coord[0], coord[1])
            
        cop = m.getBoardState()
        flagNext = obviousFlags(cop)
        for coord in flagNext:
            if (anim):
                animate(m)
            m.flag(coord[0], coord[1])
        
        cop = m.getBoardState()
        uncoverNext = obviousUncover(cop)
        
        if ( len(uncoverNext) == 0 and not m.won and not m.lost):
            uncoverNext = logicUncover(cop)
            
        if (anim):
            animate(m)

def logicUncover(board):
    uncoverNext = []
    
    unsolvedNums = []
    numsNeeds = []
    covered = {}
    #find the unsolved numbers
    for y in range(m.height):
        for x in range(m.width):
            if board[y][x] != Minesweeper.ground_symbol \
            and board[y][x] != " " \
            and board[y][x] != Minesweeper.flag_symbol:
                adj = getAdj(board, y, x)
                count = 0
                for coord in adj:
                    if (board[coord[0]][coord[1]] == Minesweeper.flag_symbol):
                        count += 1
                    elif (board[coord[0]][coord[1]] == Minesweeper.ground_symbol):
                        covered[(coord[0],coord[1])] = 0
                if (count < board[y][x]):
                    unsolvedNums.append([y,x])
                    numsNeeds.append(board[y][x] - count)
    
    #print(covered)
    #print(unsolvedNums)
    #print(numsNeeds)
    
    #use the numbers to calculate all the possible places a mine can go
    covered,worked = logicUncoverHelper(board, unsolvedNums, numsNeeds, covered)
    
    for key in covered.keys():
        if (covered[key] == 0):
            uncoverNext.append([key[0],key[1]])
    
    if len(uncoverNext) == 0:
        least = -1
        coord = []
        for key in covered:
            if (covered[key] < least or least == -1):
                coord = list(key)
                least = covered[key]
        uncoverNext.append(coord)
    #print (covered)
    
    return uncoverNext
    
def logicUncoverHelper(board, unsolvedNums, numsNeeds, covered, at = 0):
    for i in numsNeeds:
        if (i < 0):   
            return covered, False
    if (at < len(unsolvedNums) and numsNeeds[at] == 0):
        return logicUncoverHelper(board, unsolvedNums, numsNeeds, covered,at+1)
    if (len(unsolvedNums) > at):
        pos = unsolvedNums[at]
        
        need = numsNeeds[at]
        
        #
        possibleSpots = []
        adj = getAdj(board, pos[0], pos[1])
        for coord in adj:
            if (board[coord[0]][coord[1]] == Minesweeper.ground_symbol):
                possibleSpots.append(coord)
        
        permuations = permutate(possibleSpots[:], need)
        
        #print("num:", pos[0],",",pos[1])
        #print("perms:", permuations)
        
        for perm in permuations:
            cop = []
            for row in board:
                cop.append(row[:])
                
            numsNeedsCop = numsNeeds[:]
            
            #flag all the spots for a mine in this permutation
            for coord in perm:
                cop[coord[0]][coord[1]] = Minesweeper.flag_symbol
                covered[(coord[0],coord[1])] += 1
                
                x = 0
                for num in unsolvedNums:
                    if (isAdj(coord[0], coord[1], num[0], num[1])):
                        numsNeedsCop[x] -= 1
                    x+=1
                    
            covered,worked = logicUncoverHelper(cop, unsolvedNums, numsNeedsCop, covered,at+1)
                
            for coord in perm:
                if (not worked):
                    covered[(coord[0],coord[1])] -= 1   
    return covered, True

def permutate(lst, diff):
    if (0 >= diff or diff > len(lst)):
        return [[]]
    l = []
    while len(lst) >= diff:
        temp = lst[0]
        lst.pop(0)
        for e in permutate(lst[:],diff-1):
            l.append([temp]+e)
    return l
    

def isAdj(y1,x1, y2,x2):
    return abs(y1-y2) <= 1 and abs(x1-x2) <= 1

def obviousFlags(board):
    flags = []
    for y in range(m.height):
        for x in range(m.width):
            if board[y][x] != Minesweeper.ground_symbol \
            and board[y][x] != " " \
            and board[y][x] != Minesweeper.flag_symbol:
                #stuff
                flags.extend(getFlags(board,y,x))
    return flags

#counts the number of coverd/flagged squares and if it equals the count
#it returns the squares to flag
def getFlags(board, y, x):
    flags = []
    adj = getAdj(board,y,x)
    count = 0
    for coord in adj:
        if (board[coord[0]][coord[1]] == Minesweeper.ground_symbol):
            count += 1
            flags.append(coord)
        elif (board[coord[0]][coord[1]] == Minesweeper.flag_symbol):
            count += 1
    if (count == board[y][x]):
        return flags
    return []

#returns the next squares to uncover
def obviousUncover(board):
    uncoverNext = []
    
    for y in range(m.height):
        for x in range(m.width):
            if board[y][x] != Minesweeper.ground_symbol \
            and board[y][x] != " " \
            and board[y][x] != Minesweeper.flag_symbol:
                uncoverNext.extend(getUncovered(board, y, x))
    return uncoverNext

#get the squares to uncover at this pos
def getUncovered(board,y, x):
    temp = []
    adj = getAdj(board,y,x)
    count = 0
    for coord in adj:
        if (board[coord[0]][coord[1]] == Minesweeper.flag_symbol):
            count += 1
        elif (board[coord[0]][coord[1]] == Minesweeper.ground_symbol):
            temp.append(coord)
    if (count == board[y][x]):
        return temp
    return []       

def getAdj(board,y,x):
    adj = []
    width = len(board[0])
    height = len(board)
    if y > 0:
        # |
        adj.append([y - 1,x] )
        # \
        if (x > 0):
             adj.append([y-1,x-1])
    if x > 0:
        # -
        adj.append([y,x-1])
        # /
        if (y < height-1):
             adj.append([y+1,x-1])
    if y < height -1:
        # | 
        adj.append([y+1,x])
        # \
        if (x < width -1):
             adj.append([y+1,x+1])
    if x < width - 1:
        #-
        adj.append([y,x+1])
            
        if (y > 0):
             adj.append([y-1,x+1])
    return adj
    

m = Minesweeper(16,16,40)

solve(m, True)

#m.printGui(True)