#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
TankistOnline - Client [Python 3]
Copyright (C) 2019. All Rights Reserved.

The client for TankistOnline.
"""

import math, pyglet, os
import TankClass
import tkinter as tk
import socket
import re

from ListenerClass import Listener
from ViewportClass import Viewport
from pyglet.window import key
from time import sleep
from random import randint

#Globals
window = pyglet.window.Window(600, 400)
listener = Listener()
server = ('127.0.0.1', 2019) #IP and Port of Server
movement = {'mForward': False, 'mBackward': False, 'rLeft': False, 
	'rRight': False}
view = Viewport(0, 0, 600, 400)
enemies = []
player = None
tko_handlers = None
gameOver = False
connected = False
attempts = 0

#Initialize main-game window
window.set_caption('TankistOnline - Client')
window.set_icon(pyglet.image.load('gfx/16x16.png'), 
	pyglet.image.load('gfx/32x32.png'))

#Initialize player sprite
player = TankClass.Tank()
player.loadImage('gfx/sprites', 'blue.png')

#Initialize game-over and connecting sprites
sprGameOver = TankClass.Tank()
sprGameOver.loadImage('gfx/ui', 'game_over.png')
sprGameOver.x, sprGameOver.y = 300, 205
sprGameOver.setXY()

sprConnecting = TankClass.Tank()
sprConnecting.loadImage('gfx/ui', 'connecting.png')
sprConnecting.x, sprConnecting.y = 300, 205
sprConnecting.setXY()

#Initialize our map
sprMap = TankClass.Tank()
sprMap.loadImage('gfx/textures', 'map.png')
sprMap.x, sprMap.y = 0, 0
sprMap.setXY()
sprMap.sprTank.scale = 2
sprMap.isMap = True

def main():

	"""
	Application entrypoint
	"""
	
	print('[---------TankistOnline - Client---------]')
	print('                  v1.2:Alpha')
	print(' Copyright (C) 2019. All Rights Reserved.')
	print()

	selectServer()
	pyglet.clock.schedule(update, 1/15.0) #Update at 30Hz
	connectToServer()
	pyglet.app.run()
	
"""
-----
Client functions
-----
"""

def selectServer():
	
	"""
	Let the user specify the connection details.
	"""
	
	global server
	
	#When public hosts are available, we shall display them here.
	#As there are none as of yet, manual configuration is assumed.
	
	print('[---Host Selection---]')
	print('1) Manual host configuration')
	print('2) Official Public Server')
	userselection = int(input())
	hostSelected=False
	if userselection is 1:
		while not hostSelected:
			hostSelected=selectHost()
	if userselection is 2:
		hostSelected = socket.gethostbyname('tankistonline.skeltonkey.xyz')

	server=(str(hostSelected), 2019)
	
def selectHost():
	
	"""
	Prompt the user to enter a host, and make sure
	it's valid.
	"""
	
	userhost = input("Enter host IP >")
	check = bool(re.search('[a-zA-Z]', userhost))
	print(check)
	if check is True:
		tmpHost = socket.gethostbyname(userhost)
	else:
		tmpHost = userhost

	return tmpHost
	
	
def connectToServer():
	
	"""
	Connect to the server
	"""
	
	global player
	
	nickn = input('Enter a nickname >')
	print('Connecting to server...')
	send('tko:newplayer %s' % nickn) #Notify the server that we want to join in.
	sleep(2)
	player.nick = nickn
	send('tko:refresh') #Ask for all information.

	
def newEnemy(nick):
	
	"""
	Return a new Tank object representing a new enemy
	
	Params:
	  :nick: Nickname of enemy tank
	"""
	
	enemy = TankClass.Tank()
	enemy.loadImage('gfx/sprites', "red.png")
	enemy.nick = nick
	
	return enemy

def game_over():
	
	"""
	Set game-over to true
	"""

	global gameOver
	
	gameOver = True

def processServer():
	
	"""
	Check and process what the server sent	
	"""

	messages = listener._read_all()
	
	for message in messages:
		
		sentFrom = message[1]
		message = message[0]
		
		if sentFrom != server and sentFrom[0] not in ('127.0.0.1', 'localhost'):
			continue #No bogus packets
		
		kwarg = message.split()[0]
		
		if kwarg in tko_handlers:
			
			#Debugging: use "tko_handlers[kwarg](message)"
			#instead of the try statement below, to see all
			#exception details.
			try:
				tko_handlers[kwarg](message)
			except Exception as e:
				print('Exception while handling %s.' % kwarg)
		
def send(msg):
	
	"""
	Send a message to the server.
	
	Params:
	  :msg: A string containing a message to send.
	"""
	
	listener._send(msg, server)
	sleep(.05) #Don't spam
	

def refreshRelativeXY(tank):
	
	"""
	Update the x,y coords of a tank relative to our
	viewport
	
	Params:
	  :tank: The Tank object to adjust 
	"""
	
	tx = tank.absx
	ty = tank.absy
	
	tank.x, tank.y = view.updateXY(tx, ty, tank.isMap)
	tank.setXY()

def findTank(nick):
	
	"""
	Find a tank by nickname. If he's not in the player pool, add him,
	then ask the server for a refresher.
	
	Params:
	  :nick: A string containing the nickname of the tank to find
	"""
	
	global enemies
	
	if nick.lower() == player.nick.lower():
		return player
		
	for en in enemies:
		if en.nick.lower() == nick.lower():
			return en
			
	nt=newEnemy(nick)
	enemies.append(nt)
	
	send('tko:refresh')
	
	return nt

"""
-----
Window event handlers
-----
"""

@window.event
def on_key_press(symbol, modifiers):
	
	"""
	Handle key-presses
	
	Params:
	  :symbol: Pointer to the key pressed
	  :modifiers: A modifier that may change the meaning of the key
	"""
	
	global movement
	
	if symbol == key.RIGHT:
		movement['rLeft'] = True
	elif symbol == key.LEFT:
		movement['rRight'] = True
	elif symbol == key.UP:
		movement['mForward'] = True
	elif symbol == key.DOWN:
		movement['mBackward'] = True
	elif symbol == key.SPACE:
		send('tko:shoot')
			
@window.event
def on_key_release(symbol, modifiers):
	
	"""
	Handle key-releases
	
	Params:
	  :symbol: Pointer to the key pressed
	  :modifiers: A modifier that may change the meaning of the key
	"""
	
	global movement
	
	if symbol == key.RIGHT:
		movement['rLeft'] = False
	elif symbol == key.LEFT:
		movement['rRight'] = False
	elif symbol == key.UP:
		movement['mForward'] = False
	elif symbol == key.DOWN:
		movement['mBackward'] = False
		
@window.event
def on_draw():
	
	"""
	Draw event
	"""
	
	global gameOver
	
	window.clear()
	
	#Draw the map
	
	refreshRelativeXY(sprMap)
	sprMap.draw()
	
	player.draw()
	
	#Draw other tanks
	for enemy in enemies:
		enemy.draw()
		
	#Draw our life
	hpLabel = pyglet.text.Label(hpString(),
		font_name='Sans',
		font_size=12,
		x=150, y=10)
	hpLabel.color = (255, 0, 0, 180) #RGBA
	hpLabel.draw()
		
	#If the game is over, draw the game-over screen
	if gameOver:
		window.clear()
		sprGameOver.draw()
		return
		
	#If we're not connected, draw the connecting screen
	if not connected:		
		
		window.clear()
		sprConnecting.draw()
		sleep(0.2)
		
def hpString():
	
	"""
	Returns a string containing a textual representation of a lifebar
	"""

	lifebar = '████████████████████'
	negbar =  '░░░░░░░░░░░░░░░░░░░░'
		
	pHP = player.hp*2
	
	bar = 'HP: ['+lifebar[0:pHP]+negbar[0:20-pHP]+']'
	
	return bar
		
def update(dt, kwarg):
	
	"""
	Process the server, handle movement/shooting, and redraw if necessary.
	
	Params:
	  :dt: Time since this was last called
	  :kwarg: Un-used message from Pyglet
	"""
	
	global attempts, gameOver
	
	#We don't want to draw more than we have to, so we'll set need_draw
	#to True if we want on_draw() to be called at the end of our checks.
	#need_draw = False 
	
	#Before anything else, check if we were destroyed.
	if gameOver:
		return
	
	#First, check if we're moving
	if movement['mForward']:
		send('tko:move +')
	elif movement['mBackward']:
		send('tko:move -')
		
	if movement['rRight']:
		send('tko:rotate -')
	elif movement['rLeft']:
		send('tko:rotate +')
		
	#Second, check what the server says
	processServer()
	
	if not connected:
	
		attempts+=1
		processServer()
		sleep(.5)
			
		#We've tried to connect for 5 seconds.
		if attempts > 10:
			gameOver = True
			print('[!] Failed to connect to server.')
			print('  [info] Most probably, the specified IP address is\r')
			print('   not running a Tankist Server.')
			print('  [info] It could also be your firewall.')
			return
	
	
"""
-----
TKO PROTOCOL handlers
-----
"""
	
def _tko_newplayer(s):
	
	#Handle the TKO:NEWPLAYER protocol [WORKING]
	#  tko:newplayer playerName
	
	global enemies, connected
	
	ss = s.split()
	
	if len(ss) != 2:
		return
		
	newNick = str(ss[1])
	
	if newNick == player.nick: #We don't want to add ourselves to enemy list!
		connected=True
		print('Connected.')
		return
	
	newTank = newEnemy(newNick)
	newTank.x, newTank.y = -999, -999 #Don't let him be seen
	enemies.append(newTank)
	
def _tko_destroy(s):
	
	#Handle the TKO:DESTROY protocol [WORKING]
	#  tko:destroy <nick>
	
	global enemies
	
	ss = s.split()
	
	if len(ss) != 2:
		return
		
	nick = str(ss[1])
	
	tank = findTank(nick)
	
	if nick == player.nick:
		game_over()
		
	#Find and remove the destroyed player
		
	cnt=0
	for tnk in enemies:
		if enemies[cnt].nick == nick:
			del(enemies[cnt])
		cnt+=1
	
def _tko_hit(s):
	
	#Handle the TKO:HIT protocol [WORKING]
	#  tko:hit <nick> <hitsLeft>
	
	ss = s.split()
	
	if len(ss) != 3:
		return
		
	nick = str(ss[1])
	
	tank = findTank(nick)
	tank.explode()
	
	#If it's us that was hit, then update our life thatway
	#we can display the proper lifebar.
	if nick == player.nick:
		
		hpLeft = int(ss[2])
		player.hp = hpLeft
	
def _tko_xy(s):
	
	#Handle the TKO:XY protocol [WORKING]
	#  tko:xy <nick> <absx> <absy>
	
	params=s.split()
	
	if len(params) != 4:
		return
		
	nick=str(params[1])
	absx=int(params[2])
	absy=int(params[3])
	
	tank=findTank(nick)
	
	tank.absx=absx
	tank.absy=absy
	
	if tank.nick == player.nick:
		
		#Update the viewport, to follow our tank
		
		global view

		view.topLeftX = tank.absx - 300
		view.topLeftY = tank.absy + 200

		refreshRelativeXY(player)
		
		for en in enemies:
			refreshRelativeXY(en)
			
		on_draw()
			
		return
	
	refreshRelativeXY(tank) #Just move that tank
	on_draw()
	
def _tko_rotate(s):
	
	#Handle the TKO:ROTATE protocol [WORKING]
	#  tko:rotate <nick> <rotation> <realRotation>
	
	params=s.split()
	
	if len(params) != 4:
		return
		
	nick=str(params[1])
	rotation=int(params[2])
	realRotation=int(params[3])
	
	tank=findTank(nick)
	
	tank.rotation=rotation
	tank.realRotation=realRotation
	tank.rotate()
	
if __name__ == "__main__":
	
	"""
	Set up a dictionary to handle the TKO:PROTOCOL by mapping
	statements to their handlers.
	"""
	
	tko_handlers = {
	'tko:rotate': _tko_rotate,
	'tko:newplayer': _tko_newplayer,
	'tko:xy': _tko_xy,
	'tko:hit': _tko_hit,
	'tko:destroy': _tko_destroy
	}
	
	main()
