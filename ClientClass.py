import random
import socket

class Client:
	
	isServerSocket = False
	state = 0 #0 = Handshake, 1=In-Battle
	
	address = None #IP Address of the client
	connection = None #Connection object
	nick = None #Nickname
	
	explosion = None #Whether this tank is exploding
	explosionIndex = None #If this tank is exploding, this contains the stage
						  #the explosion.
	
	rotation = 0 #Clockwise Pyglet-style rotation
	realRotation = 0 #Counter-Clockwise rotation, for calculating movement and shots
	
	absx = 0 #Absolute xy values.
	absy = 0
	
	def __init__(self, conn, addr): #Initialize client object
		
		self.address = addr
		self.connection = conn
		
		self._randomXY()
		
	def _randomXY(self): #Choose a random XY value for this client
		
		self.absx = random.randint(0, 750)
		self.absy = random.randint(0, 750)

	def fileno(self):
		
		return self.connection.fileno()

	def send(self, message): #Send plaintext to a client
		
		self.connection.send(str(message))

	def read(self): #Read plaintext from a client
		
		return self.connection.recv(1024)
