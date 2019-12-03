"""
TankistOnline - Client > TankClass
Copyright (C) 2019. All Rights Reserved.
"""

import pyglet

class Tank:

	def __init__(self):
		
		"""
		Initialize a new Tank object.
		
		Params:
		  :self: This new Tank object
		"""

		self.sprTank = None
		self.sprExplosion = None
		self.explosion = None
		self.explosionIndex = 0
		self.rotation = 0
		self.realRotation = 0
		self.hp = 10
		self.nick = ''
		self.isMap = False
	
		#Relative xy values.
		self.x = -999
		self.y = -999
	
		#Absolute xy values.
		self.absx = 0 
		self.absy = 0
		
		#Load the explosion
		pyglet.resource.path = ['gfx/sprites']
		pyglet.resource.reindex()
		imgExplode = pyglet.resource.image("explode.png")
		imgExplode = self._centralize(imgExplode)
		self.sprExplosion = pyglet.sprite.Sprite(img=imgExplode, x=self.x, y=self.y)

	def loadImage(self, pathToImage, imageName):

		"""
		Initialize this tank sprite with an image.
		
		Params:
			:self: This Tank object
			:pathToImage: String containing a path to the image
			:imageName: Filename of the image
		"""
		
		pyglet.resource.path = [pathToImage]
		pyglet.resource.reindex()

		imgImage = pyglet.resource.image(imageName)

		imgImage = self._centralize(imgImage)

		self.sprTank = pyglet.sprite.Sprite(img=imgImage, x=self.x, y=self.y)

	def setXY(self):
		
		"""
		Update the X,Y location of the sprites and related objects,
		from our self.x and self.y
		
		Params:
		  :self: This Tank object
		"""

		self.sprTank.x, self.sprTank.y = self.x, self.y
		self.sprExplosion.x, self.sprExplosion.y = self.x, self.y

	def explode(self):

		"""
		Trigger the explosion.
		
		Params:
		  :self: This Tank object
		"""
		
		self.explosion = True
		self.explosionIndex = 0

	def rotate(self):

		"""
		Rotate the tank and related objects.
		
		Params:
			:self: This Tank object
		"""
		
		self.sprTank.rotation = self.rotation
		self.sprExplosion.rotation = self.rotation

	def draw(self):
		
		"""
		Draw the tank and his nickname. If he's exploding, draw that too.
		
		Params:
			:self: This Tank object
		"""
		
		self.sprTank.draw()

		if self.explosion:

			self.explosionIndex += 1

			#The explosion lasts for 10 cycles
			if self.explosionIndex == 10: 
				self.explosion = False
				self.explosionIndex = None
			else:
				self.sprExplosion.draw()
				
		if self.nick != '':
			
			#Display the nickname
			lblNick = pyglet.text.Label(self.nick,
				font_name='Sans',
				font_size=8,
				x=self.x-8,
				y=self.y+50)
			lblNick.color = (0, 255, 0, 255) #RGBA
			lblNick.draw()

	def _centralize(self, image):

		"""
		Internal function to centralize an image before it is used in a sprite,
		that it may rotate evenly upon its axis.
		
		Params:
		  :self: This Tank object
		  :image: The image to centralize
		"""
	
		image.anchor_x = image.width // 2
		image.anchor_y = image.height // 2

		return image
