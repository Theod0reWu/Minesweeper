# -*- coding: utf-8 -*-
"""
Created on Wed May 26 11:06:23 2021

@author: wut6
"""

from minesweeper import Minesweeper

mode = ""
while (True):
    mode = input("Enter Difficulty (easy, medium, hard): ")
    if (mode == "easy" or mode == "medium" or mode == "hard"):
        break

h,w,b = 0,0,0
if (mode == "easy"):
    h,w,b = 10,10,10
elif (mode == "medium"):
    h,w,b = 16,16,40
else:
    h,w,b = 16,30,99

m = Minesweeper(h,w,b)

while (not m.lost and not m.won):
    m.printGui(True)
    print("Enter the command flag, unflag, clear or quit (f/u/c/q) then the row and column")
    s = input("Enter: ").split()
    if (len(s) < 3 and s[0] != 'q'):
        continue
    if (s[0] == 'f'):
        for i in range(1,len(s)-1,2):
           m.flag(int(s[i]),int(s[i+1]))
    elif(s[0] == 'c'):
        for i in range(1,len(s)-1,2):
           m.uncover(int(s[i]),int(s[i+1]))
    elif (s[0] == 'u'):
        for i in range(1,len(s)-1,2):
           m.unflag(int(s[i]),int(s[i+1]))
    elif (s[0] == 'q'):
        break
    else:
        print("unknown command")

print("\n========")
if (m.lost):
    print("You Lost")
elif(m.won):
    print("You Won")
print("========")
m.printGui(True)