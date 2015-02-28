#!/usr/bin/python
# -*- coding: latin-1 -*-
import curses
import random

def sign(value):
	if value < 0:
		return -1
	if value > 0:
		return 1

class box:
	x = 0
	y = 0
	width = 0
	height = 0
	passages = []
	def __init__(self,x=0,y=0,w=1,h=1):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.passages = []
	def getMaxY(self):
		return self.y + self.height - 1
	def getMaxX(self):
		return self.x + self.width - 1 #-1 for width of side
	def getMinY(self):
		return self.y
	def getMinX(self):
		return self.x
	#
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
	def adjacentTo(self,other):
		Ax1 = self.x
		Ax2 = self.getMaxX()
		Bx1 = other.x
		Bx2 = other.getMaxX()
		overlap = 0
		start = -1
		#
		delta21 = Ax2 - Bx1
		delta22 = Ax2 - Bx2
		overlapsR = sign(delta21) != sign(delta22)
		if overlapsR:
			start = Bx1
			overlap = delta21
			if overlap > other.width:
				overlap = other.width
			if overlap > self.width:
				start = Ax1
				overlap = self.width
		delta21 = Bx2 - Ax1
		delta22 = Bx2 - Ax2
		overlapsL = sign(delta21) != sign(delta22)
		if overlapsL:
			start = Ax1
			overlap = delta21
			if overlap > other.width:
				start = Bx1
				overlap = other.width
			if overlap > self.width:
				overlap = self.width
		# top-edge
		if self.y - other.getMaxY() is 1:
			if overlap !=0:
				return ('top',start,overlap)
			return None
		# bottom-edge
		if  other.y - self.getMaxY() is 1:
			if overlap !=0:
				return ('bottom',start,overlap)
			return None
		Ay1 = self.y
		Ay2 = self.getMaxY()
		By1 = other.y
		By2 = self.getMaxY()
		start = -1
		overlap = 0
		delta21 = Ay2 - By1
		delta22 = Ay2 - By2
		overlapsR = sign(delta21) != sign(delta22)
		if overlapsR:
			start = By1
			overlap = delta21
			if overlap > other.height:
				overlap = other.height
			if overlap > self.height:
				overlap = self.height
				start = Ay1
		delta21 = By2 - Ay1
		delta22 = By2 - Ay2
		overlapsL = sign(delta21) != sign(delta22)
		if overlapsL:
			start = Ay1
			overlap = delta21
			if overlap > other.height:
				overlap = other.height
				start = By1
			if overlap > self.height:
				overlap = self.height	
		# left-edge
		if self.x - other.getMaxX() is 1:
			if overlap > 0:
				return ('left',start,overlap)
			return None
		# right-edge
		if other.x - self.getMaxX() is 1:
			if overlap > 0:
				return ('right',start,overlap)
			return None
		return None
	def join(self,where):
		start = where[1]
		length = where[2]
		if where[0] is 'top':
			coords = (start,self.y)
			self.passages.append( ('top',coords,length) )
			return
		if where[0] is 'bottom':
			coords = (start,self.getMaxY())
			self.passages.append( ('bottom',coords,length) )
			return
		if where[0] is 'left':
			coords = (self.x,start)
			self.passages.append( ('left',coords,length) )
			return
		if where[0] is 'right':
			coords = (self.getMaxX(),start)
			self.passages.append( ('right',coords,length) )
			return
		return 
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
		# passages
		for p in self.passages:
			length = p[2]
			coords = p[1]
			if length > 2:
				if p[0] is 'left':
					scr.vline(coords[1],coords[0],' ',length-1)
					scr.addch(coords[1],coords[0],curses.ACS_LRCORNER)
					scr.addch(coords[1]+length-1,coords[0],curses.ACS_URCORNER)
				if p[0] is 'right':
					scr.vline(coords[1],coords[0],' ',length-1)
					scr.addch(coords[1],coords[0],curses.ACS_LLCORNER)
					scr.addch(coords[1]+length-1,coords[0],curses.ACS_ULCORNER)
				if p[0] is 'top':
					scr.hline(coords[1],coords[0],' ',length-1)
					scr.addch(coords[1],coords[0],curses.ACS_LRCORNER)
					scr.addch(coords[1],coords[0]+length-1,curses.ACS_LLCORNER)
				if p[0] is 'bottom':
					scr.hline(coords[1],coords[0],' ',length-1)
					scr.addch(coords[1],coords[0],curses.ACS_URCORNER)
					scr.addch(coords[1],coords[0]+length-1,curses.ACS_ULCORNER)
	def __str__(self):
		x = self.x
		y = self.y
		width = self.width
		height = self.height
		return "box["+ x +','+ y +','+ str(int(x+width))+','+str(int(y+height))+"]"

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
		L=split(subBoxes[0], minSize, depth - 1)
		R=split(subBoxes[1], minSize, depth - 1)
		# maybe make this more 'random' in the future
		hasjoined = False
		for boxL in L:
			for boxR in R:
				adjR = boxR.adjacentTo(boxL)
				if adjR:
					adjL = boxL.adjacentTo(boxR)
					#
					start = adjR[1]
					length = adjR[2]
					portalSize = 4
					if length > (portalSize+1):
						newStart = random.randint(start+1,start+length-(portalSize+1))
						#
						boxR.join( (adjR[0],newStart,portalSize) )
						boxL.join( (adjL[0],newStart,portalSize) )
						hasjoined = True
						break
			if hasjoined:
				break;
		return L + R



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
	#print "DIM ",width,height
	boxes = split(boxes[0],8,4)
	for b in boxes:
		b.draw()
		#print "box: ",`b.x`,`b.y`,`b.width`,`b.height`
	scr.refresh()
	scr.getch()
	curses.endwin()
