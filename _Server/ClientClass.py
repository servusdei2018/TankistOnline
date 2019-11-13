"""
TankistOnline - Server > ClientClass
"""

import socket, random, time

class Client:
	
	def __init__(self, addr):
		
		#Initialize client object
		
		self.address = addr
		self.nick = None #String, Nickname of tank
		self.explosion = None #Boolean, whether this tank is exploding
		self.hp = 10 #Amount of hits left until destruction
	
		#Clockwise Pyglet-style rotation in degrees
		self.rotation = 0 
		#Counter-Clockwise rotation in degrees, for calculating movement and shots
		self.realRotation = 0 
		
		#Set X, Y values
		self._randomXY()
		
	def _randomXY(self):
		
		#Choose a random XY value for this client
		
		self.absx = random.randint(0, 750)
		self.absy = random.randint(0, 750)
		
	def send(self, sock, msg):
		
		#Send a UDP message to this client.
		#Params:
		#  @self: This Client object
		#  @sock: A socket.socket() object in socket.SOCK_DGRAM (UDP) mode
		#  @msg: A string to be sent
		
		sock.sendto(str(msg).encode(), self.address)
