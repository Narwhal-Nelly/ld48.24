#!/usr/bin/python
# -*- coding: latin-1 -*-
import curses

class point:
	x = 0
	y = 0
	def __init__(self,x=0,y=0):
		self.x = x
		self.y = y

def clampPoint(p,min,max):
	if p.x < min.x:
		p.x = min.x
	if p.x > max.x:
		p.x = max.x
	if p.y < min.y: 
		p.y = min.y
	if p.y > max.y:
		p.y = max.y

scr = curses.initscr()
curses.curs_set(0)
curses.meta(True)
m = scr.getmaxyx()
ScreenMax = point(m[1],m[0])
m = scr.getbegyx()
ScreenMin = point(m[1],m[0])

width = ScreenMax.x - ScreenMin.x
height = ScreenMax.y - ScreenMax.y

right = 261
left = 260
up = 259
down = 258

pos = point(10,10)

scr.nodelay(True)
curses.noecho()
scr.keypad(True)
loop = True
debug = []

scr.hline(1,1,'-',20)
scr.hline(20,1,'-',20)

while loop is True:
	opos = point(pos.x,pos.y)
	mykey = scr.getch() 
	if mykey > 0:
		if mykey == ord('d') or mykey == right:
			pos.x+=1
		if mykey == ord('a') or mykey == left:
			pos.x-=1
		if mykey == ord('w') or mykey == up:
			pos.y-=1
		if mykey == ord('s') or mykey == down:
			pos.y+=1
		if mykey == 27:
			loop = False
		#if mykey == 27:
		#	loop = False
		clampPoint(pos,ScreenMin,ScreenMax)
		scr.addch(opos.y,opos.x,' ')
		n = scr.inch(pos.y,pos.x)
		if n != ord(' '): 
			debug.append(n)
			pos.y = opos.y
			pos.x = opos.x
	scr.addch(pos.y,pos.x,'@')
	scr.refresh()
	#
	#if mykey is chr(27):
	#	loop = False
	#curses.napms(60)
	



curses.endwin()

print (debug)