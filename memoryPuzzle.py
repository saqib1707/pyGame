import pygame,sys,random
from Tkinter import *
from pygame.locals import *
import time

black=(0,0,0)
white=(255,255,255)
blue=(0,0,255)
green=(0,255,0)
red=(255,0,0)
cyan=(0,255,255)
mixed_cyan=(60,255,255)
gray=(230,230,230)
navyBlue=( 60, 60, 100)
lightNavyBlue=(130,130,200)
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
highlightColor=yellow

windowWidth=640
windowHeight=480
boxSize=40
gapSize=10
boardWidth=4
boardHeight=3

groupSize=4
delay=500         # in miliseconds

assert (boardWidth*boardHeight)%2==0,"Board should have even number of boxes"

x_margin=int((windowWidth-(boardWidth*boxSize+gapSize*(boardWidth-1)))/2)     # comes out to be 70 for above cases
y_margin=int((windowHeight-(boardHeight*boxSize+gapSize*(boardHeight-1)))/2)   # comes out to be 65 for above cases

All_Colors=[purple,blue,green,red,cyan,yellow,orange]                         # it doesn't matters if u use a list or tuple here.
All_Shapes=[donut,square,oval,diamond,lines]

fpsClock=pygame.time.Clock()				# initializing the clock

def main():

	mouse_x=0
	mouse_y=0 
	pygame.init() 
	global basic_font,start_time,final_time
	basic_font=pygame.font.Font('freesansbold.ttf', 20)	                           
	global display_surface,start_rect,start_surface,exit_rect,exit_surface
	display_surface=pygame.display.set_mode((windowWidth,windowHeight))     #  will return a surface object on which everything will
                  															#  be laid upon
	start_surface,start_rect=makeText('New Game',gray,lightNavyBlue,500,10)
	exit_surface,exit_rect=makeText('Exit Game',gray,lightNavyBlue,500,40)

	pygame.display.set_caption('Memory Puzzle')
	display_surface.fill(backgroundColor)
	mainBoard=getRandomizedBoard()                             # will return a 10x7 board with each place containing a tuple of 
																# (color,shape)
	revealedBoxes=generateRevealedBoxesData(False)    # will return a 7x10 list revealing the state( T or F )of individual boxes 
	while True:
														# whether it is revealed or covered.In the beginning it is False by default
		pygame.draw.circle(display_surface,red,(30,30),10)

		display_surface.blit(start_surface,start_rect)
		display_surface.blit(exit_surface,exit_rect)

		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

			elif event.type==MOUSEBUTTONUP:
				mouse_x,mouse_y=event.pos

				if start_rect.collidepoint(event.pos):          # on clicking the new Game button.
					pygame.time.delay(500)

					startGameAnimation(mainBoard) 

					start_time=time.time() 									# after all the initial revealing happens ,jst start counting 
																			# the time

					pygame.draw.circle(display_surface,green,(30,30),10)       # signal that game has started.
					pygame.display.update()
					 
					firstSelected=None

					while True:

						display_surface.fill(backgroundColor)
						isMouseClicked=False
						drawBoard(mainBoard,revealedBoxes,green)
						# time calculation and showing
						cur_time=time.time()
						time_surf=basic_font.render('Time:'+ str(int(cur_time-start_time)),True,gray,lightNavyBlue)
						time_rect=time_surf.get_rect()
						time_rect.topleft=(500,80)
						display_surface.blit(time_surf,time_rect)
						pygame.display.update()

						for event in pygame.event.get():
							if event.type==QUIT:
								pygame.quit()
								sys.exit()

							elif event.type==MOUSEMOTION:
								mouse_x,mouse_y=event.pos

							elif event.type==MOUSEBUTTONUP:
								if exit_rect.collidepoint(event.pos):
									pygame.quit()
									sys.exit()
								elif start_rect.collidepoint(event.pos):
									mainBoard=getRandomizedBoard()
									revealedBoxes=generateRevealedBoxesData(False)
									display_surface.fill(backgroundColor)
									#drawBoard(mainBoard,revealedBoxes,red)
									pygame.time.delay(500)
									startGameAnimation(mainBoard)
									pygame.draw.circle(display_surface,green,(30,30),10)
									pygame.display.update()
								mouse_x,mouse_y=event.pos
								isMouseClicked=True

						box_x,box_y=getBoxNumber(mouse_x,mouse_y)
						if box_x!=None and box_y!=None:
							#if not revealedBoxes[box_x][box_y]:
								#drawHighlightColor(mainBoard,box_x,box_y)
								#pygame.display.update()
							if not revealedBoxes[box_x][box_y] and isMouseClicked==True:
								revealBoxesAnimation(mainBoard,[(box_x,box_y)])
								revealedBoxes[box_x][box_y]=True
								if firstSelected==None:
									firstSelected=(box_x,box_y)
								else:
									getShape1,getColor1=getShapeAndColor(mainBoard,firstSelected[0],firstSelected[1])
									getShape2,getColor2=getShapeAndColor(mainBoard,box_x,box_y)
					
									if getShape1!=getShape2 or getColor1!=getColor2:
										pygame.time.delay(500)
										coverBoxesAnimation(mainBoard,[(firstSelected[0],firstSelected[1]),(box_x,box_y)])
										revealedBoxes[box_x][box_y]=False
										revealedBoxes[firstSelected[0]][firstSelected[1]]=False
									elif hasGameWon(revealedBoxes):
										#final_time=cur_time
										gameWonAnimation(mainBoard,cur_time)
										mainBoard=getRandomizedBoard()
										revealedBoxes=generateRevealedBoxesData(False)
										display_surface.fill(backgroundColor)
										pygame.draw.circle(display_surface,red,(30,30),10)
										pygame.display.update()
										gameWon=True
										break
			
									firstSelected=None
				elif exit_rect.collidepoint(event.pos):
					pygame.quit()
					sys.exit()
			
			elif event.type==MOUSEMOTION:
				mouse_x,mouse_y=event.pos
				if insideCircle(mouse_x,mouse_y):
					pygame.draw.circle(display_surface,white,(30,30),10)

		pygame.display.update()
		

def makeText(text, color, bgcolor, top, left):				# for making text like new game and exit game
	# create the Surface and Rect objects for some text.
	textSurf = basic_font.render(text, True, color, bgcolor)
	textRect = textSurf.get_rect()
	textRect.topleft = (top, left)
	return (textSurf, textRect)
		
def insideCircle(x,y):
	if (pow((x-30),2)+pow((y-30),2)-100)<=0:
		return True
	else:
		return False


def hasGameWon(revealedBoxes):				# checks whether game has ended or not #
	flag=True
	for box_x in range(boardWidth):
		for box_y in range(boardHeight):

			if revealedBoxes[box_x][box_y]==False:
				return False
	return True

def get_Name():

	playerName=name_entry.get()
	with open('TimeRecord.txt','a') as appendFile:
		appendFile.write('%s : %s secs on %s\n'%(playerName,timeToComplete,time.ctime()))
	#for widget in frame.winfo_children():
		#widget.destroy()
	frame.destroy()

def gameWonAnimation(board,final_time):			# after game completion , background changes appears.
	
	display_surface.fill(cyan)
	global timeToComplete
	timeToComplete=str(int(final_time-start_time))

	finalTime_surf,finalTime_rect=makeText('Time Taken : '+timeToComplete+' secs',gray,lightNavyBlue,200,200)
	display_surface.blit(finalTime_surf,finalTime_rect)
	pygame.display.update()
	pygame.time.delay(3000)

	global frame
	frame=Tk()
	frame.title('LeaderBoard Name')
	frame.geometry('200x100+350+150')
	frame.config(bg='#ABADAC')
	frame.resizable(width = False,height = False)

	global name_entry
	name_entry=Entry(frame,width=40)
	name_entry.place(x=20,y=30)
	Button(frame,text='Proceed',command=get_Name).place(x=70,y=60)
	frame.mainloop()
	

def getBoxNumber(mouse_x,mouse_y):			# given the pixel values of the starting of a box , returns the box numbers.
	for box_x in range(boardWidth):
		for box_y in range(boardHeight):
			left,top=leftTopCoordsOfBox(box_x,box_y)
			boxRect=pygame.Rect(left,top,boxSize,boxSize)
			if boxRect.collidepoint(mouse_x,mouse_y):
				return box_x,box_y
	return None,None
				
def drawHighlightColor(board,box_x,box_y):       	# highlights the boxes if cursor hovers over it
	left,top=leftTopCoordsOfBox(box_x,box_y)
	pygame.draw.rect(display_surface,highlightColor,(left-5,top-5,boxSize+10,boxSize+10),5)

def getRandomizedBoard():		 # creates a row x col list having random tuples of (shape,color)
	icons=[]
	for color in All_Colors:
		for shape in All_Shapes:
			icons.append((shape,color))
	random.shuffle(icons)
	numIconsNeeded=int((boardWidth*boardHeight)/2)

	icons=icons[0:numIconsNeeded]*2
	random.shuffle(icons)                                  # for more randomization
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

def leftTopCoordsOfBox(box_x,box_y):				# given box numbers , returns the pixel values of the topleft corner 
	return int(x_margin+(box_x * (boxSize+gapSize))),int(y_margin+(box_y * (boxSize+gapSize)))

def getShapeAndColor(board,box_x,box_y):
	return board[box_x][box_y][0],board[box_x][box_y][1]

def drawIcon(shape,color,box_x,box_y):			# function name clarifies
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
	for box in boxesToReveal:                        # here boxToReveal ~ one of the group(8) of boxes.
		left,top=leftTopCoordsOfBox(box[0],box[1])
		pygame.draw.rect(display_surface,backgroundColor,(left,top,boxSize,boxSize))  # when opening and closing the background should 
		shape,color=getShapeAndColor(board,box[0],box[1])                             # be backgroundColor
		drawIcon(shape,color,box[0],box[1])
		if coverage>0:
			pygame.draw.rect(display_surface,boxColor,(left,top,coverage,boxSize))
		
	pygame.display.update()            
	pygame.time.delay(delay/10)                 # After revealing 8 boxes partially or fully it will wait.

def coverBoxesAnimation(board,boxesToCover):		# covers the box from both sides
	for coverage in range(0,boxSize+groupSize,8):
		drawBoxCover(board,boxesToCover,coverage)


def revealBoxesAnimation(board,boxesToReveal):		# opens the boxes from the middle
	for coverage in range(boxSize,-groupSize-1,-groupSize):
		drawBoxCover(board,boxesToReveal,coverage)


def drawBoard(board,revealed,colorOfCircle):                       # this function draws the board in its present state.
	for box_x in range(boardWidth):
		for box_y in range(boardHeight):
			if not revealed[box_x][box_y]:
				left,top=leftTopCoordsOfBox(box_x,box_y)         # left ,top are starting pixel coordinates of a particular box.
				pygame.draw.rect(display_surface,boxColor,(left,top,boxSize,boxSize))   # draw a white cover of boxSize x boxSize
			else:
				shape,color=getShapeAndColor(board,box_x,box_y)     # will take shape and color if it is not revealed and draw icon
				drawIcon(shape,color,box_x,box_y)
	pygame.draw.circle(display_surface,colorOfCircle,(30,30),10)
	display_surface.blit(start_surface,start_rect)
	display_surface.blit(exit_surface,exit_rect)

def splitsIntoGroupOf(groupsize,boxes):				# creates group of random boxes to show during startGameAnimation
	result=[]
	for x in range(0,len(boxes),groupsize):
		result.append(boxes[x:x+groupsize])
	return result


def startGameAnimation(board):

	coveredBoxes=generateRevealedBoxesData(False)            # 7x10
	boxes=[]
	for x in range(boardWidth):
		for y in range(boardHeight):   
			boxes.append((x,y))                      # boxes[] appends boardWidth x boardheight number of tuples like [(5,4),(2,6)] 
	random.shuffle(boxes)
	boxGroups=splitsIntoGroupOf(groupSize,boxes)    # will return a list[] containing tuples of (x,y) in groups of 8 but last will
													# be a group of 6 since it is 10 x 7 matrix

	drawBoard(board,coveredBoxes,red)			# covered boxes is a list of 10 x 7 matrix containing False.
	for boxGroup in boxGroups:
		revealBoxesAnimation(board,boxGroup)
		pygame.time.delay(delay*2)
		coverBoxesAnimation(board,boxGroup)
		pygame.time.delay(delay)


if __name__=='__main__':
	main()