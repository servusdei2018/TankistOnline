"""
TankistOnline - Client Side Listener

Handles UDP Packets to the client.
"""

import socket

class Listener:
	
	def __init__(self):
		
		#Initialize the Listener.
		
		HOST = '127.0.0.1'
		PORT = 2002
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((HOST, PORT)) #Bind socket to localhost, port 2019
		self.sock.setblocking(0) #Make sure socket is not blocking
		
	def _send(self, msg, server):
		
		#Send message @msg to @server.
		
		self.sock.sendto(str(msg).encode(), server)
		
	def _read_all(self):
	
		#Read all packets until none are found -- when none are found, recvfrom() returns error
	
		packets = []
	
		stop=False
		while not stop:
			try:
				data, addr = self.sock.recvfrom(1024)
				data = data.decode()
				packets.append((data, addr))
			except Exception as e:
				stop=True
		return packets
