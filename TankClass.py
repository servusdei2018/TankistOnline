import pyglet
class Tank:

	sprTank = None
	sprExplosion = None
	health = 100
	explosion = None
	explosionIndex = None
	removeable = False
	rotation = 0
	realRotation = 0

	rotateLeftRequested = False
	rotateRightRequested = False

	x = 0
	y = 0

	absx = 0 #Absolute xy values.
	absy = 0

	def loadImage(self, pathToImage, imageName):

		#Initialize this tank sprite with an image.

		pyglet.resource.path = [pathToImage]
		pyglet.resource.reindex()

		imgImage = pyglet.resource.image(imageName)

		imgImage = self.centralize(imgImage)

		self.sprTank = pyglet.sprite.Sprite(img=imgImage, x=self.x, y=self.y)

	def setXY(self):

		self.sprTank.x = self.x
		self.sprTank.y = self.y
		self.sprExplosion.x = self.x
		self.sprExplosion.y = self.y

	def explode(self):

		#Trigger the explosion.
		#and adjust health
		self.explosion = True
		self.explosionIndex = 0
		self.health -= 10
		if self.health <1:
			self.removeable=True


	def rotate(self):

		#Rotate both the tank and the explosion.

		self.sprTank.rotation = self.rotation
		self.sprExplosion.rotation = self.rotation


	def draw(self):
		#Show the health only for the player tank
		if self.player:
			#Draw the tank. If an explosion is present, explode that, too.
			self.updateLabel()# adjusts the drawn value

			self.label.draw()
		self.sprTank.draw()

		if self.explosion:

			self.explosionIndex += 1

			if self.explosionIndex == 10:

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

	def updateLabel(self):
		self.label = pyglet.text.Label(str(self.health),
				                          font_name='Times New Roman',
				                          font_size=36,
				                          x=0, y=0)



	def __init__(self,isPlayer=False):

		#We preload the explosion, as no tank shall go unscathed.
		#difference between player Tanks and other tanks. Health is only showen for player tanks
		self.player=isPlayer
		pyglet.resource.path = ['gfx/sprites']
		pyglet.resource.reindex()

		imgExplode = pyglet.resource.image("explode.png")
		imgExplode = self.centralize(imgExplode)

		self.sprExplosion = pyglet.sprite.Sprite(img=imgExplode, x=self.x, y=self.y)

		imgExplode = None
