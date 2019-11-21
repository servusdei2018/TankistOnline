"""
TankistOnline - Server > ClientClass
Copyright (C) 2019. All Rights Reserved.
"""

import socket, random, time

class Client:
	
	def __init__(self, addr):
		
		"""
		Initialize client object
		
		Params:
		  :self: This Client object
		  :addr: Tuple containing IP address and port of the client
		"""
		
		self.address = addr
		self.nick = None #String, Nickname of tank
		self.explosion = None #Boolean, whether this tank is exploding
		self.hp = 10 #Amount of hits left until destruction
	
		#Clockwise Pyglet-style rotation in degrees
		self.rotation = 0 
		#Counter-Clockwise rotation in degrees, for calculating movement and shots
		self.realRotation = 0
		
		self.idles = 0
		
		#Set X, Y values
		self._randomXY()
		
	def _randomXY(self):
		
		"""
		Choose a random XY value for this client, but make sure not
		to exceed the map's boundaries.
		
		Params:
		  :self: This Client object
		"""
		
		self.absx = random.randint(0, 600)
		self.absy = random.randint(0, 400)
		
	def send(self, sock, msg):
		
		"""
		Send a UDP message to this client.
		
		Params:
		  :self: This Client object
		  :sock: A socket.socket() object in socket.SOCK_DGRAM mode (UDP)
		  :msg: A string to be sent
		"""
		
		sock.sendto(str(msg).encode(), self.address)
