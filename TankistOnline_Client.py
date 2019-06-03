import math
import pyglet
import TankClass

from pyglet.window import key

window = pyglet.window.Window()

player_sprite = None #Player sprite
enemies = []

playSound = False #Requires vlc media player, as well as the vlc python library to be
				  #installed.

theme = None

if playSound:
	import vlc

def main():

	global player_sprite
	
	player_sprite = TankClass.Tank()
	
	player_sprite.loadImage('gfx/sprites', "blue.png")
	
	player_sprite.x = 100
	player_sprite.y = 100
	player_sprite.setXY()
	
	tempEnemies()
	
	if playSound:
		
		global theme
		
		theme = vlc.MediaPlayer("sfx/theme.mp3")
		theme.play()
	
	pyglet.app.run()
	
def newEnemy():
	
	enemy = TankClass.Tank()
	
	enemy.loadImage('gfx/sprites', "red.png")
	
	enemy.x = 50
	enemy.y = 50
	enemy.setXY()
	
	return enemy
	
def tempEnemies():
	
	global enemies
	
	enemies.append(newEnemy())
	
	"""
	pyglet.resource.path = ['gfx/sprites']
	pyglet.resource.reindex()
	
	enemy_image = pyglet.resource.image("red.png")
	
	enemy_image = centralize(enemy_image)
	
	newEnemy = pyglet.sprite.Sprite(img=enemy_image, x=200, y=100)

	enemy_image = None
	
	enemies.append(newEnemy)
	enemyRotations.append(0)

	newEnemy = None
	"""

@window.event
def on_key_press(symbol, modifiers):
	
	if symbol == key.SPACE:

		if playSound:
			boom = vlc.MediaPlayer("sfx/boom.mp3")
			boom.play()
		
		myx = player_sprite.x
		myy = player_sprite.y
		
		rads = math.radians(player_sprite.realRotation)
		
		#The process of whether he hit or not shall be determined by the server.
		#However, a skectch of the procedure is implemented here.
		
		for enemy in enemies:
			
				enx = enemy.x
				eny = enemy.y
				
				dist = int(math.hypot(myx - enx, myy - eny))
				
				print("Distance to target: "+str(dist))
				
				bulletX, bulletY = move(myx, myy, dist, rads)
				
				print(str(bulletX)+","+str(bulletY))
				print(str(enx)+","+str(eny))
				
				if abs(bulletX-enx) + abs(bulletY-eny) < 80:
					enemy.explode()
			

@window.event
def on_text_motion(motion):
	
	global player_sprite, realRotation
	
	if motion == key.MOTION_RIGHT:
		
		#The client shall not perform rotation, it shall instead communicate its rotation
		#to the server which shall return its new rotation.
		
		player_sprite.rotation += 3
		player_sprite.rotate()
		player_sprite.realRotation -= 3
		
		if player_sprite.rotation > 359:
			player_sprite.rotation = 0
	
		if player_sprite.realRotation < 0:
			player_sprite.realRotation = 359
			
		player_sprite.rotate()
			
		return
			
	elif motion == key.MOTION_LEFT:
		
		#As above.
		
		player_sprite.rotation -= 3
		player_sprite.realRotation += 3
		
		if player_sprite.rotation < 0:
			player_sprite.rotation = 359
	
		if player_sprite.realRotation > 360:
			player_sprite.realRotation = 1

		player_sprite.rotate()

		return
	
	else:
		
		if motion == key.MOTION_UP:
			
			#The client shall communicate that it wants to move up to the server,
			#which shall then make it move up.
			
			angle_rad = math.radians(player_sprite.realRotation)
			x = player_sprite.x
			y = player_sprite.y
			
			player_sprite.x, player_sprite.y = move(x, y, 4, angle_rad)
			
			player_sprite.move()
			
			return
			
		elif motion == key.MOTION_DOWN:
			
			#As above.
		
			angle_rad = math.radians(player_sprite.realRotation)
			x = player_sprite.x
			y = player_sprite.y
			
			player_sprite.x, player_sprite.y = move(x, y, 4, angle_rad)
			
			player_sprite.move()
		
def move(x, y, speed, angle_in_radians):
    new_x = x + (speed*math.cos(angle_in_radians))
    new_y = y + (speed*math.sin(angle_in_radians))
    return new_x, new_y
		
@window.event
def on_draw():
	window.clear()
	
	player_sprite.draw()
	
	for enemy in enemies:
		
		enemy.draw()

	if playSound == True:
		if bool(theme.is_playing()) == False:
		
			theme.play()
	
if __name__ == "__main__":
	
	main()
	
	
