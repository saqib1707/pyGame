import pygame,sys,random
from pygame.locals import *

black=(0,0,0)
white=(255,255,255)
blue=(0,0,255)
green=(0,255,0)
red=(255,0,0)
cyan=(0,255,255)
gray=(128,128,128)
navyBlue=( 60, 60, 100)
yellow=(255,255,0)
purple=(255,0,255)
orange=(255,128,0)

donut='donut'
square='square'
diamond='diamond'
lines='lines'
oval='oval'

backgroundColor=navyBlue
lightBgColor=gray
boxColor=white
highlightColor=blue

windowWidth=640
windowHeight=480
boxSize=40
gapSize=10
boardWidth=10
boardHeight=7

groupSize=8

assert (boardWidth*boardHeight)%2==0,"Board should have even number of boxes"

x_margin=int((windowWidth-(boardWidth*(boxSize+gapSize)))/2)     # comes out to be 70 for above cases
y_margin=int((windowHeight-(boardHeight*(boxSize+gapSize)))/2)   # comes out to be 65 for above cases

All_Colors=(purple,blue,green,red,cyan,yellow,orange)
All_Shapes=(donut,square,oval,diamond,lines)

def main():
	pygame.init()
	fpsClock=pygame.time.Clock()                                         # initializing the clock
	global display_surface
	display_surface=pygame.display.set_mode((windowWidth,windowHeight))     #  will return a surface object on which everything will
																			#  be laid upon
	pygame.display.set_caption('Memory Puzzle')
	display_surface.fill(backgroundColor)
	mainBoard=getRandomizedBoard()                              # will return a 10x7 board with each place containing a tuple of 
																# (color,shape)
	revealedBoxes=generateRevealedBoxesData(False)    # will return a 10 x 7 list revealing the state( T or F )of individual boxes 
														# whether it is revealed or covered.In the beginning it is False by default
	startGameAnimation(mainBoard) 
	mouse_x=0
	mouse_y=0            
	while True:
		display_surface.fill(backgroundColor)
		isMouseClicked=False
		firstSelected=None

		drawBoard(mainBoard,revealedBoxes)
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			elif event.type==MOUSEMOTION:
				mouse_x,mouse_y=event.pos
			elif event.type==MOUSEBUTTONUP:
				mouse_x,mouse_y=event.pos
				isMouseClicked=True
		box_x,box_y=getBoxNumber(mouse_x,mouse_y)
		if box_x!=None and box_y!=None:
			if not revealedBoxes[box_x][box_y]:
				drawHighlightColor(mainBoard,box_x,box_y)
			if not revealedBoxes[box_x][box_y] and isMouseClicked==True:
				revealBoxAnimation(mainBoard,[(box_x,box_y)])
				if firstSelected==None:
					firstSelected=(box_x,box_y)
				else:
					getShape1,getColor1=getShapeAndColor(mainBoard,firstSelected[0],firstSelected[1])
					getShape2,getColor2=getShapeAndColor(mainBoard,box_x,box_y)
					if getShape1==getShape2 and getColor1==getColor2:
						revealedBoxes[box_x][box_y]=True
						revealedBoxes[firstSelected[0],firstSelected[1]]=True
						if hasGameWon(revealedBoxes):
							gameWonAnimation(mainBoard)
							pygame.time.wait(3000)
							# if game won then start a new game
							mainBoard=getRandomizedBoard()
							revealedBoxes=generateRevealedBoxesData(False)
							drawBoard(mainBoard,revealedBoxes)
							pygame.time.wait(1000)
							pygame.display.update()
							startGameAnimation(mainBoard)
					elif getshape1!=getShape2 or getColor1!=getColor2:
						pygame.time.wait(1000)
						coverBoxesAnimation(mainBoard,[(firstSelected[0],firstSelected[1]),(box_x,box_y)])
						revealedBoxes[box_x][box_y]=False
						revealedBoxes[firstSelected[0]][firstSelected[1]]=False
		pygame.display.update()

def hasGameWon(revealedBoxes):
	flag=True
	for box_x in range(boardWidth):
		for box_y in range(boardHeight):

			if revealedBoxes[box_x][box_y]==False:
				return False
	return True

def gameWonAnimation(board):
	display_surface.fill(navyBlue)
	pygame.display.update()
	pygame.time.wait(2000)

def getBoxNumber(mouse_x,mouse_y):
	for box_x in range(boardWidth):
		for box_y in range(boardHeight):
			left,top=leftTopCoordsOfBox(mouse_x,mouse_y)
			boxRect=pygame.Rect(left,top,boxSize,boxSize)
			if boxRect.collidepoint(mouse_x,mouse_y):
				return box_x,box_y
	return None,None
				
def drawHighlightColor(board,box_x,box_y):
	left,top=leftTopCoordsOfBox(board,box_x,box_y)
	pygame.draw.rect(display_surface,highlightColor,(left-5,top-5,boxSize+10,boxSize+10),5)
	pygame.display.update()

def getRandomizedBoard():
	icons=[]
	for color in All_Colors:
		for shape in All_Shapes:
			icons.append((shape,color))
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
	return board

def generateRevealedBoxesData(boolean):
	revealedBoxes=[]
	for i in range(boardWidth):
		revealedBoxes.append([boolean]*boardHeight)
	return revealedBoxes

def leftTopCoordsOfBox(box_x,box_y):
	return int(x_margin+(box_x * (boxSize+gapSize))),int(y_margin+(box_y * (boxSize+gapSize)))

def getShapeAndColor(board,box_x,box_y):
	return board[box_x][box_y][0],board[box_x][box_y][1]

def drawIcon(shape,color,box_x,box_y):
	left,top=leftTopCoordsOfBox(box_x,box_y)
	x_center=left+boxSize/2
	y_center=top+boxSize/2

	if shape=='donut':
		pygame.draw.circle(display_surface,color,(x_center,y_center),boxSize/2,5)

	elif shape=='diamond':
		pygame.draw.polygon(display_surface,color,((x_center,top),(left+boxSize,y_center),(x_center,top+boxSize),(left,y_center)))

	elif shape=='square':
		pygame.draw.rect(display_surface,color,(left+boxSize/4,top+boxSize/4,boxSize/2,boxSize/2))

	elif shape=='lines':
		for i in range(0, boxSize, 4):
			pygame.draw.line(display_surface, color, (left, top + i), (left +i, top))
			pygame.draw.line(display_surface, color, (left + i, top + boxSize- 1), (left + boxSize - 1, top + i))

	elif shape=='oval':
		pygame.draw.ellipse(display_surface,color,(left,top+boxSize/4,boxSize,boxSize/2))

def drawBoxCover(board,boxesToReveal,coverage):      # has the effect of opening and closing of boxes.
	for box in boxesToReveal:
		left,top=leftTopCoordsOfBox(box[0],box[1])
		pygame.draw.rect(display_surface,backgroundColor,(left,top,boxSize,boxSize))  
		shape,color=getShapeAndColor(board,box[0],box[1])
		drawIcon(shape,color,box[0],box[1])
		if coverage>0:
			pygame.draw.rect(display_surface,boxColor,(left,top,coverage,boxSize))
	pygame.display.update()

def coverBoxesAnimation(board,boxesToCover):
	for coverage in range(0,boxSize+groupSize,8):
		drawBoxCover(board,boxesToCover,coverage)


def revealBoxesAnimation(board,boxesToReveal):
	for coverage in range(boxSize,-groupSize-1,-groupSize):
		drawBoxCover(board,boxesToReveal,coverage)


def drawBoard(board,revealed):                       # this function draws the board in its present state.
	for box_x in range(boardWidth):
		for box_y in range(boardHeight):
			if not revealed[box_x][box_y]:
				left,top=leftTopCoordsOfBox(box_x,box_y)         # left ,top are starting pixel coordinates of a particular box.
				pygame.draw.rect(display_surface,boxColor,(left,top,boxSize,boxSize))   # draw a white cover of boxSize x boxSize
			else:
				shape,color=getShapeAndColor(board,box_x,box_y)     # will take shape and color if it is not revealed and draw icon
				drawIcon(shape,color,box_x,box_y)

def splitsIntoGroupOf(groupsize,boxes):
	result=[]
	for x in range(0,len(boxes),groupsize):
		result.append(boxes[x:x+groupsize])
	return result

def startGameAnimation(board):
	coveredBoxes=generateRevealedBoxesData(False)
	boxes=[]
	for x in range(boardWidth):
		for y in range(boardHeight):   
			boxes.append((x,y))                      # boxes[] appends boardWidth x boardheight number of tuples like [(5,4),(2,6)] 
	random.shuffle(boxes)
	groupsize=8
	boxGroups=splitsIntoGroupOf(groupsize,boxes)    # will return a list[] containing tuples of (x,y) in groups of 8 but last will
													# be a group of 6 since it is 10 x 7 matrix

	drawBoard(board,coveredBoxes)			# covered boxes is a list of 10 x 7 matrix containing False.
	for boxGroup in boxGroups:
		revealBoxesAnimation(board,boxGroup)
		coverBoxesAnimation(board,boxGroup)

if __name__=='__main__':
	main()