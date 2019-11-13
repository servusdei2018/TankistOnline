"""
TankistOnline - Client > TankClass
"""

import pyglet

class Tank:

	def __init__(self):

		self.sprTank = None
		self.sprExplosion = None
		self.explosion = None
		self.explosionIndex = 0
		self.removeable = False
		self.rotation = 0
		self.realRotation = 0
		self.hp = 10
	
		self.rotateLeftRequested = False
		self.rotateRightRequested = False
	
		self.x = 0
		self.y = 0
	
		self.absx = 0 #Absolute xy values.
		self.absy = 0
		
		#Load the explosion
		pyglet.resource.path = ['gfx/sprites']
		pyglet.resource.reindex()
		imgExplode = pyglet.resource.image("explode.png")
		imgExplode = self.centralize(imgExplode)
		self.sprExplosion = pyglet.sprite.Sprite(img=imgExplode, x=self.x, y=self.y)

	def loadImage(self, pathToImage, imageName):

		#Initialize this tank sprite with an image.

		pyglet.resource.path = [pathToImage]
		pyglet.resource.reindex()

		imgImage = pyglet.resource.image(imageName)

		imgImage = self.centralize(imgImage)

		self.sprTank = pyglet.sprite.Sprite(img=imgImage, x=self.x, y=self.y)

	def setXY(self):
		
		#Set the X,Y location of this tank.

		self.sprTank.x = self.x
		self.sprTank.y = self.y
		self.sprExplosion.x = self.x
		self.sprExplosion.y = self.y

	def explode(self):

		#Trigger the explosion.
		
		self.explosion = True
		self.explosionIndex = 0

	def rotate(self):

		#Rotate both the tank and the explosion.

		self.sprTank.rotation = self.rotation
		self.sprExplosion.rotation = self.rotation

	def draw(self):
		
		#Draw the tank.
		
		self.sprTank.draw()

		if self.explosion:

			self.explosionIndex += 1

			if self.explosionIndex == 10: #The explosion lasts for 10 cycles

				self.explosion = False
				self.explosionIndex = None

			else:

				self.sprExplosion.draw()

	def centralize(self, image):

		#Internal function to centralize an image before it is used in a sprite,
		#that it may rotate evenly upon its axis.

		image.anchor_x = image.width // 2
		image.anchor_y = image.height // 2

		return image

	def move(self):

		#Internal function to change the tank's x and y.

		self.sprTank.x = self.x
		self.sprTank.y = self.y
		self.sprExplosion.x = self.x
		self.sprExplosion.y = self.y
