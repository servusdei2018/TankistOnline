"""
TankistOnline - Client Side Listener
Copyright (C) 2019. All Rights Reserved.

Handles UDP Packets to/from the client.
"""

import socket
from random import randint

class Listener:
	
	def __init__(self):
		
		"""
		Initialize the Listener.
		
		Params:
		  :self: The new Listener object
		"""
		
		bound=False
		while not bound:
			try:
				bound = self._bind()
			except Exception as e:
				continue
		
	def _bind(self):
		
		"""
		Attempt to bind to a random port. An error is raised if
		the port is already in use.
		
		Params:
		  :self: This Listener object
		"""
		
		HOST = '0.0.0.0' #Hostname of this computer (set to 127.0.0.1 for security)
		PORT = 2000 + randint(0, 99) #Port to bind the socket to
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((HOST, PORT))
		self.sock.setblocking(0)
		
		return True
		
	def _send(self, msg, server):
		
		"""
		Send a message message to the server.
		
		Params:
		  :self: This Listener object
		  :msg: A string containing a message
		  :server: A tuple representing the IP Address and port of the server
		"""
		
		try:
			self.sock.sendto(str(msg).encode(), server)
		except Exception as e:
			print('[!] An exception occured when communicating to the host.')
			print(' [info] Most probably, it is because of an invalid IP address.')
			print(' [info] If not, there is a problem with your firewall.')
		
	def _read_all(self):
	
		"""
		Read all packets until none are found, then return them. 
		
		Params:
			:self: This Listener object
		"""
		
		packets = []
	
		stop=False
		while not stop:
			try:
				data, addr = self.sock.recvfrom(1024)
				data = data.decode()
				packets.append((data, addr))
			except Exception as e:
				#When no more are found, recvfrom() raises an error.
				stop=True
		return packets
