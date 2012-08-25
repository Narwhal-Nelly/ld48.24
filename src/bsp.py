#!/usr/bin/python
import curses
import random

class box:
	x = 0
	y = 0
	width = 0
	height = 0
	def __init__(self,x=0,y=0,w=1,h=1):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
	def splitH(self,xsplit):
		if self.width > xsplit:
			boxA = box(
				self.x,
				self.y,
				xsplit,
				self.height)
			boxB = box(
				self.x+xsplit,
				self.y,
				self.width-xsplit,
				self.height)
			return (boxA,boxB)
		return (None,None) 
	def splitV(self,ysplit):
		if self.height > ysplit:
			boxA = box(
				self.x,
				self.y,
				self.width,
				ysplit)
			boxB = box(
				self.x,
				self.y+ysplit,
				self.width,
				self.height-ysplit)
			return (boxA,boxB)
		return (None,None)
	def draw(self):
		x = self.x
		y = self.y
		w = self.width
		h = self.height
		# lines:
		scr.hline(y,x+1,curses.ACS_HLINE,w-2)
		scr.vline(y+1,x,curses.ACS_VLINE,h-2)
		scr.vline(y+1,x+w-1,curses.ACS_VLINE,h-2)
		scr.hline(y+h-1,x+1,curses.ACS_HLINE,w-2)
		# corners
		scr.addch(y,x,curses.ACS_ULCORNER)
		scr.addch(y,x+w-1,curses.ACS_URCORNER)
		scr.addch(y+h-1,x,curses.ACS_LLCORNER)
		scr.addch(y+h-1,x+w-1,curses.ACS_LRCORNER)
	def __str__(self):
		x = self.x
		y = self.y
		width = self.width
		height = self.height
		return "box["+`x`+','+`y`+','+`int(x+width)`+','+`int(y+height)`+"]"

def split(box,minSize, depth = 5):
	# make sure we didn't go too deep
	if depth is 0:
		return [ box ] # list of just this box
	# let's assume we _need_ to split this
	vertical = 1
	horizontal = 2
	direction = random.randint(1,2) # vertical or horizontal?
	#
	#
	if direction is vertical:
		if box.height < minSize * 2:
			direction = horizontal
	if direction is horizontal:
		if box.width < minSize * 2:
			if box.height < minSize * 2:
				return [ box ] # return a list containing just this box
			direction = vertical
	#
	# Now that size has been verified, perform split:
	if direction is vertical:
		subBoxes = box.splitV(random.randint(minSize,box.height-minSize))
	else: # horizontal
		subBoxes = box.splitH(random.randint(minSize,box.width-minSize))
	#
	if len(subBoxes) is 2:
		return split(subBoxes[0], minSize, depth - 1) + split(subBoxes[1], minSize, depth - 1)


if __name__ == '__main__':
	scr = curses.initscr()
	curses.curs_set(0)
	curses.meta(True)
	maxYX = scr.getmaxyx()
	minYX = scr.getbegyx()
	
	#maxYX = (20,20)
	#minYX = (0,0)
	
	width = maxYX[1] - minYX[1]-5
	height = maxYX[0] - minYX[0]-5
	boxes = [ box(3,3,width,height) ]
	print "DIM ",width,height
	boxes = split(boxes[0],4,3)
	for b in boxes:
		b.draw()
		print "box: ",`b.x`,`b.y`,`b.width`,`b.height`
	scr.refresh()
	scr.getch()
	curses.endwin()
