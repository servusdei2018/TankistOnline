"""
TankistOnline - Client

The client for TankistOnline
"""

import math
import pyglet
import TankClass

from ListenerClass import Listener
from pyglet.window import key
from time import sleep

#Globals
window = pyglet.window.Window(600, 400)
listener = Listener()
player = None
hpLabel = pyglet.text.Label('HP: '+str(100), font_name='Sans Serif', font_size=36, x=0, y=0)
enemies = []
server = ('127.0.0.1', 2019) #IP and Port
movement = {'mForward': False, 'mBackward': False, 'rLeft': False, 'rRight': False}

#Initialize window
window.set_caption('TankistOnline - Client')
icon1 = pyglet.image.load('gfx/16x16.png')
icon2 = pyglet.image.load('gfx/32x32.png')
window.set_icon(icon1, icon2)
icon1 = None
icon2 = None

#Initialize out player sprite
player = TankClass.Tank()
player.loadImage('gfx/sprites', "blue.png")

def main():

	#Client entrypoint
	
	connectToServer()
	pyglet.clock.schedule(update, 1/15.0) #Update at 30Hz
	pyglet.app.run()
	
def connectToServer():
	
	#Connect to the server
	
	nickn = input('Enter a nickname:')
	print('Connecting to server...')
	send('tko:newplayer %s' % nickn) #Notify the server that we want to join in.
	send('tko:refresh') #Ask for all information.
	print('Connected. Please wait...')
	
def newEnemy(x, y, nick):
	
	#A new enemy.
	
	enemy = TankClass.Tank()
	enemy.loadImage('gfx/sprites', "red.png")
	
	enemy.x = 50 #TODO
	enemy.y = 50 #TODO
	enemy.absx = x
	enemy.absy = y
	enemy.setXY()
	
	return enemy

@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.RIGHT:
		movement['rRight'] = True
	elif symbol == key.LEFT:
		movement['rLeft'] = True
	elif symbol == key.UP:
		movement['mForward'] = True
	elif symbol == key.DOWN:
		movement['mBackward'] = True
	elif symbol == key.SPACE:
		send('tko:shoot')
			
@window.event
def on_key_release(symbol, modifiers):
	if symbol == key.RIGHT:
		movement['rRight'] = False
	elif symbol == key.LEFT:
		movement['rLeft'] = False
	elif symbol == key.UP:
		movement['mForward'] = False
	elif symbol == key.DOWN:
		movement['mBackward'] = False

@window.event
def on_text_motion(motion):
	return
		
@window.event
def on_draw():
	
	#Draw everything.
	
	window.clear()
	player.draw()
	
	for enemy in enemies:
		enemy.draw()
		
def update(dt, overflow):
	
	#Perform check for need to redraw.
	
	# TODO: add interface check and read input from server
	# Note: rotation speed is always 3 (in the future, different speeds could be implemented
	#	for different hulls).
	
	need_draw = False #We don't want to draw more than we have to, so we'll set need_draw
			  #to True if we want on_draw() to be called at the end of our checks.
	
	#First, check if we're moving
	
	if movement['mForward']:
		send('tko:move +')
	elif movement['mBackward']:
		send('tko:move -')
		
	if movement['rRight']:
		send('tko:rotate +')
	elif movement['rLeft']:
		send('tko:rotate -')
		
	#Second, check what the server says
	
	processServer()
	
	#Display the health.
	
	updateLabel() #Update the label to reflect our health, and draw it
		
	if player.explosion:
		need_draw = True
	
	for enemy in enemies:
		if enemy.explosion:
			need_draw = True
			
	if need_draw:
		on_draw()
		
def processServer():
	
	#Check and process what the server sent
	
	messages = listener._read_all()
	
	for message in messages:
		
		
def send(msg):
	
	#Send a message to the server.
	
	print(msg)
	listener._send(msg, server)
	sleep(.2) #Don't spam
		
def updateLabel():
		
	#Update the life display
		
	hpLabel = pyglet.text.Label('HP: '+str(player.hp*10), font_name='Sans Serif', font_size=36, x=0, y=0)
	hpLabel.draw()
	
if __name__ == "__main__":
	main()
