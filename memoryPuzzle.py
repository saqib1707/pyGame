import pygame,sys,random
from pygame.locals import *

black=(0,0,0)
white=(255,255,255)
blue=(0,0,255)
green=(0,255,0)
red=(255,0,0)
cyan=(0,255,255)
grey=(128,128,128)
navyBlue=( 60, 60, 100)

donut='donut'
square='square'
diamond='diamond'
lines='line'
oval='oval'

backgroundColor=navyBlue
boxColor=white
highlightColor=blue

windowHeight=480
windowWidth=640
boxSize=40
gapSize=10
boardHeight=7
boardWidth=10

assert (boardWidth*boardHeight)%2==0,"Board should have even number of boxes"

x_margin=int((windowWidth-(boardWidth*(boxSize+gapSize)))/2)
y_margin=int((windowHeight-(boardHeight*(boxSize+gapSize)))/2)

All_Colors=(black,blue,green,red,cyan,grey,navyBlue)
All_Shapes=(donut,square,oval,diamond,lines)

def main():
	pygame.init()
	global display_turf
	display_turf=pygame.display.set_mode((windowWidth,windowHeight))
	pygame.display.set_caption('Memory Puzzle')
	display_turf.fill(black)
	mainBoard=getRandomizedBoard()

	revealedBoxes=generateRevealedBoxesData(False)
	startGameAnimation(mainBoard)


def getRandomizedBoard():
	icons=[]
	for color in All_Colors:
		for shape in All_Shapes:
			icons.append((color,shape))
	random.shuffle(icons)
	numIconsNeeded=int((boardWidth*boardHeight)/2)

	icons=icons[:numIconsNeeded]*2
	random.shuffle(icons)
	board=[]
	for x in range(boardWidth):
		column=[]
		for y in range(boardHeight):
			column.append(icons[0])
			del icons[0]
		board.append(column)
	#print board
	return board

def generateRevealedBoxesData(boolean):
	revealedBoxes=[]
	for i in range(boardWidth):
		revealedBoxes.append([boolean]*boardHeight)
	#print revealedBoxes
	return revealedBoxes

def leftTopCoordsOfBox(box_x,box_y):
	return (x_margin+box_x*(boxSize+gapSize),y_margin+box_y*(boxSize+gapSize))

def getShapeAndColor(board,box_x,box_y):
	return (board[box_x][box_y][0],board[box_x][box_y][1])

def drawIcon(shape,color):
	if shape=='donut':
		pygame.draw.circle(display_turf,)


def drawBoard(board,revealed):
	for box_x in range(boardWidth):
		for box_y in range(boardHeight):
			if not revealed[x][y]:
				left,top=leftTopCoordsOfBox(box_x,box_y)
				pygame.draw.rect(display_turf,box_color,(left,top,boxSize,boxSize))
			else:
				shape,color=getShapeAndColor(board,box_x,box_y)
				drawIcon(shape,color)

def startGameAnimation(board):
	coveredBoxes=generateRevealedBoxesData(False)
	boxes=[]
	for x in range(boardWidth):
		for y in range(boardHeight):
			boxes.append((x,y))
	random.shuffle(boxes)
	print coveredBoxes
	boxGroups=splitsIntoGroup(8,boxes)

	drawBoard(board,coveredBoxes)

def splitsIntoGroup(groupsize,box):
	result=[]
	for x in range(0,len(box),groupsize):
		result.append(box[x:x+groupsize])
	#print result
	return result

def 
if __name__=='__main__':
	main()