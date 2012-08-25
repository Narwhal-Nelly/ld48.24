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
	recurs=3
	for i in range(0,recurs):
		nboxes =  []
		for b in boxes:
			#nboxes.append(b)
			rand = random.random()
			if rand > 0.5:
				if b.width < 8:
					nboxes.append(b)
					break
				ysplit = int(random.uniform(4,b.width-4))
				bA,bB = b.splitV(ysplit)
				if bA:
					nboxes.append(bA)
					nboxes.append(bB)
				else:
					nboxes.append(b)
			else:
				if b.height < 8:
					nboxes.append(b)
					break;
				xsplit = int(random.uniform(4,b.height-4))
				#print xsplit
				bA,bB = b.splitH(xsplit)	
				if bA:
					nboxes.append(bA)
					nboxes.append(bB)
				else:
					nboxes.append(b)
		boxes = nboxes
	print "DIM ",width,height
	for b in boxes:
		b.draw()
		print "box: ",`b.x`,`b.y`,`b.width`,`b.height`
	scr.refresh()
	scr.getch()
	curses.endwin()
