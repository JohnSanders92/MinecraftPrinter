import keyboard 
import time 
from tkinter import filedialog
from tkinter import Tk
from tkinter import *

def writeBlock(x, y, z):
    keyboard.send("enter")
    time.sleep(.1)
    keyboard.write("/setblock "+str(x)+" "+str(z)+" "+str(y)+" gold_block")
    time.sleep(.1)
    keyboard.send("enter")
    time.sleep(.1)

commandLimit = 65500
numberOfFiles = 0
def writeBlockToFile(x, y ,z):
    global saveFileLocation
    global buildFile
    global airFile

    buildFile.write("setblock "+str(x)+" "+str(z)+" "+str(y)+" "+blockType+"\n")
    airFile.write("setblock "+str(x)+" "+str(z)+" "+str(y)+" "+blockType+"\n")
    global commandLimit
    commandLimit = commandLimit - 1
    if(commandLimit == 0):
        buildFile.close()
        airFile.close()
        commandLimit = 65500
        global numberOfFiles
        numberOfFiles = numberOfFiles+1
        buildFile = open(saveFileLocation+str(numberOfFiles)+".mcfunction","w")
        airFile = open(saveFileLocation+"Air"+str(numberOfFiles)+".mcfunction","w")

def findPoint(m, x, b):
    y = m*x + b
    return y

Tk().withdraw()
file = filedialog.askopenfilename()
time.sleep(5)
x1 = None #x1
y1 = None #y1
z1 = 4
x2 = None #x2
y2 = None #y2
E = None
saveFileLocation = filedialog.asksaveasfilename()
buildFile = open(saveFileLocation+str(numberOfFiles)+".mcfunction","w")
airFile = open(saveFileLocation+"Air"+str(numberOfFiles)+".mcfunction","w")
blockType = input("Enter BlockType")
gcode = open(file, "r")
for line in gcode:
    parse = line.split()
    if (len(parse) > 2) and (parse[0][:2] == "G0" or parse[0][:2] == "G1") and (parse[1][:1] == "X" or parse[2][:1] == "X"):
        for code in parse:
            if code[:1] == "X":
                if(x1 == None):
                    x1 = code[1:]
                    x1 = int(round(float(x1),0))
                else:
                    x2 = code[1:]
                    x2 = int(round(float(x2),0))
            if code[:1] == "Y":
                if(y1 == None):
                    y1 = code[1:]
                    y1 = int(round(float(y1),0))
                else:
                    y2 = code[1:]
                    y2 = int(round(float(y2),0))
            if code[:1] == "Z":
                z1 = code[1:]
                z1 = int(round(float(z1),0)+4)
            if code[:1] == "E":
                E = code[1:]

        if(E is not None):
            writeBlockToFile(x1,y1,z1)
            if(x2 is not None):
                if(x1 != x2):
                    slope = (y2-y1)/(x2-x1)
                    b = y1-slope*x1
                    while x1 != x2:
                        if(x1 < x2):
                            y1 = int(round(findPoint(slope, x1, b),0))
                            writeBlockToFile(x1,y1,z1)
                            x1 = x1+1
                        else:
                            y1 = int(round(findPoint(slope, x1, b),0))
                            writeBlockToFile(x1,y1,z1)
                            x1 = x1-1
                    writeBlock(x1,y1,z1)
                else:
                    while y1 != y2:
                        if(y1 < y2):
                            writeBlockToFile(x1,y1,z1)
                            y1 = y1+1
                        else:
                            writeBlockToFile(x1,y1,z1)
                            y1 = y1-1
                    writeBlock(x1,y1,z1)
        x1 = x2
        y1 = y2 
        E = None
buildFile.close()
airFile.close()
