"""
TankistOnline - Server [Python 2.7+/3]
Copyright (C) 2019. All Rights Reserved.

--Running

The Server has no dependencies besides the standard library, and
can work with Python 2.7+, Python 3.x, and PyPy (reccomended).

For the most optimized experience, PyPy is reccomended, although
there is little performance difference between PyPy and Python 3.x

--About

This server utilizes UDP packets. UDP is pretty secure: it isn't
detected by a port scan as there is no formal listener. None of
the UDP packets are encrypted or compressed.
"""

import math, socket, sys

from ClientClass import Client
from time import sleep

MAP_WIDTH  = 600 #The width of the map, in PIXELS.
MAP_HEIGHT = 400 #The height of the map, in PIXELS.
sock = None #Server socket
players = {} #Player table

def main():
	
	"""
	Entrypoint of the server.
	"""
	
	global sock
	
	print('[---------TankistOnline - Server---------]')
	print('                    v1.0')
	print(' Copyright (C) 2019. All Rights Reserved.')
	
	#Create socket
	print('[ ] Creating socket...')
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print('[X] Socket created.')
	
	#Bind socket to localhost
	print('[ ] Binding socket...')
	
	try:
		
		"""
		Host options:
		
		'127.0.0.1' - Allows connections only from this computer
		'0.0.0.0'   - Allows connections from anywhere?
		'localhost' - Same as above?
		'' - Bind to all available interfaces
		"""
		
		HOST = '' # '' binds to all available interfaces. Can be '127.0.0.1', '0.0.0.0', 'localhost'
		PORT = 2019 #Port on which to run the server
		
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Reuse address if in use
		sock.bind((HOST, PORT)) #Bind socket to localhost, port 2019
		sock.setblocking(0) #Make sure socket is not blocking
		
		print('[X] Socket bound.')
	
	except socket.error as e:
		
		print('[!] Bind failed.')
		print('    Error Code: ' + str(e[0]))
		print('    Message ' + str(e[1]))
		exit()
	
	print('[i] You may now connect to the server by running the client')
	print('  and specifying "localhost" as the host IP. If you want to')
	print('  connect from another computer, use the IP address of this')
	print('  computer.')
	
	#Entering main loop
	print('[i] Entering main loop...')
	
	while True:
		
		sleep(.05)
		cycle() #One cycle of processing
		
def cycle():
	
	"""
	Cycle through packets, processing them.
	"""
	
	global players
	
	packets = read_all()
	
	updateIdles(packets)
	
	for packet in packets:
	
		process(packet)
	
def updateIdles(packets):
	
	"""
	Keep track of how long each player is idle, and if he's idle for
	one minute or longer, boot him out.
	"""
	
	addrs = []
	for pk in packets:
		addrs.append(pk[1])
		
	connsToDelete = []
		
	for con in players:
		if con not in addrs:
			players[con].idles += 1
			
			if players[con].idles >= 1200: #1 minute of idle and you're out
				#That tank idled out.
				broadcast('tko:destroy %s' % players[con].nick)
				
				#Add him to the list to be removed from the player list.
				connsToDelete.append(con)
		else:
			players[con].idles = 0
			
	for con in connsToDelete:
		del(players[players[con].address])
	
def process(packet):
	
	"""
	Process a packet's contents.
	"""
	
	global players
	
	data = packet[0]
	addr = packet[1]
	
	print('%s sent: %s' % (data, addr))
	
	if addr not in players:
		
		"""
		If a player is not in the player map, he has shown no proof that he is a client for the game.
		All clients, when first connecting to the server, send "tko:connect NICKNAME"
		"""
		
		if len(data.split()) > 1:
			data = data.split()
		else:
			return
			
		if data[0] != 'tko:newplayer':
			return
			
		if len(data) != 2:
			return
		
		#A new player has connected.
		nick = data[1]
		
		if isTaken(nick):
			return
		
		players[addr] = Client(addr) #Add him to the player map
		players[addr].nick = nick #Give him a nickname
		
		broadcast('tko:newplayer %s' % players[addr].nick)
		broadcast('tko:xy %s %s %s' % (players[addr].nick, players[addr].absx, players[addr].absy))
		
		return
		
	data = data.split()
	
	if data[0] not in pointers: #Invalid command.
		print('invalid command')
		return
	
	pointers[data[0]](addr, data) #Process it.
		
def read_all():
	
	"""
	Read all packets until none are found - when none are found, recvfrom() returns error
	"""
	
	packets = []
	
	stop=False
	while not stop:
		try:
			data, addr = sock.recvfrom(1024)
			data = data.decode()
			packets.append((data, addr))
		except Exception as e:
			stop=True
	
	return packets
	
def broadcast(msg):
	
	"""
	Broadcast a message to all clients
	"""
	
	print('sending: '+msg)
	
	for client in players:
		sock.sendto(msg.encode(), client)
		
def move(x, y, speed, angle_in_radians):
	
	"""
	Move a point in direction :angle_in_radians: with speed :speed: from :x:, :y:
	"""
	
	new_x = x + (speed*math.cos(angle_in_radians))
	new_y = y + (speed*math.sin(angle_in_radians))
	
	return int(new_x), int(new_y)
	
def isTaken(nick):
	
	"""
	Returns a boolean value whether a nickname is already registered in the
	player pool.
	"""
	
	for plr in players:
		player = players[plr]
		if nick.lower() == player.nick.lower():
			return True
			
	return False
    
"""
-------BEGIN TKO PROTOCOL HANDLERS--------
"""
		
def _tko_rotate(addr, data):
	
	"""
	Rotate a tank.
	
	TKO Protocol:
	  "tko:rotate +" or "tko:rotate -"
	"""
	
	global players
	
	#First, data validation.	
	if len(data)<2:
		return
	degree = data[1]
	if degree not in ('+', '-'):
		return
		
	#Then, processing.
		
	conn = players[addr] #Clone the object, for ease of reference
		
	if degree == '+':
		
		conn.rotation -= 12
		conn.realRotation += 12
		
	elif degree == '-':
		
		conn.rotation += 12
		conn.realRotation -= 12
		
	#Make sure there are no superlative degrees.
		
	if conn.rotation > 360:
		conn.rotation -= 360
	elif conn.rotation < 0:
		conn.rotation += 360
		
	if conn.realRotation > 360:
		conn.realRotation -= 360
	elif conn.realRotation < 0:
		conn.realRotation += 360
		
	players[addr] = conn #Reflect changes from the clone to the base object
		
	#Instruct clients to rotate him.
	broadcast('tko:rotate %s %s %s' % (conn.nick, conn.realRotation, conn.rotation))
	
def _tko_move(addr, data):
	
	"""
	Move a tank.
	
	TKO Protocol:
		"tko:move +" or "tko:move -"
	"""
	
	global players

	print(data)

	#First, data validation.	
	if len(data)<2:
		print('too short')
		return
	degree = data[1]
	if degree not in ('+', '-'):
		print('invalid degree')
		return
		
	#Then, processing.
		
	conn = players[addr] #Clone the object, for ease of reference
	
	angle_rad = math.radians(conn.realRotation)
		
	#Move the tank.
		
	if degree == '+':
		
		conn.absx, conn.absy = move(conn.absx, conn.absy, 16, angle_rad) #Move forwards
		
	elif degree == '-':
		
		conn.absx, conn.absy = move(conn.absx, conn.absy, -16, angle_rad) #Move backwards
		
	#Validate positions, to make sure nobody moves off the map's edges.
		
	if conn.absx < 0:
		conn.absx = 0
	if conn.absx > MAP_WIDTH:
		conn.absx = MAP_WIDTH
	if conn.absy < 0:
		conn.absy = 0
	if conn.absy > MAP_HEIGHT:
		conn.absy = MAP_HEIGHT
		
	players[addr] = conn #Reflect changes from the clone to the base object
		
	#Instruct clients to move the client.
	broadcast('tko:xy %s %s %s' % (conn.nick, conn.absx, conn.absy))
		
def _tko_newplayer(addr, data):
	
	"""
	A player has reconnected from the same IP and Port.
	"""

	global players
	
	print('Re-connection from: %s port %s' % (addr[0], addr[1]))

	#Delete the old data
	broadcast('tko:destroy %s' % players[addr].nick)
	del(players[addr])
	
	if len(data) != 2:
		return
		
	#Create a new player
	nick = data[1]
		
	if isTaken(nick):
		return
		
	players[addr] = Client(addr) #Add him to the player map
	players[addr].nick = nick #Give him a nickname
	
	broadcast('tko:newplayer %s' % players[addr].nick)
	broadcast('tko:xy %s %s %s' % (players[addr].nick, players[addr].absx, players[addr].absy))
	
def _tko_refresh(addr, data):
	
	"""
	A tank wants information on everyone's x,y and life.
	"""
	
	conn = players[addr]
	
	for player in players:
		plr = players[player]
		broadcast('tko:xy %s %s %s' % (plr.nick, plr.absx, plr.absy))
		broadcast('tko:rotate %s %s %s' % (plr.nick, plr.realRotation, plr.rotation))
		
def _tko_shoot(addr, data):
	
	"""
	A tank shot.
	
	TKO Protocol:
	  "tko:shoot"
	"""
	
	global players
	
	conn = players[addr] #Clone the object, for ease of reference
	
	for client in players:
		
		"""
		Go through all players, for each one could be a possible
		target because each one could be hit by the player's bullet.
		"""
		
		client = players[client]
		
		if client.nick == conn.nick: #Don't let a guy shoot himself!
			continue 
		
		enx = client.absx #Possible target's X, Y
		eny = client.absy
		
		dist = int(math.hypot(conn.absx-enx, conn.absy-eny)) #Distance to enemy
		rads = math.radians(conn.realRotation)
		
		print('distance=%s' % dist)
		
		"""
		We get the X, Y location of a bullet shot from the tank who is shooting,
		and move it in the direction its turret is facing the distance to the current
		enemy tank. If it is within a certain radius of the enemy tank, then it is a hit.
		"""
		
		bulletX, bulletY = move(conn.absx, conn.absy, dist, rads)
		
		#If the difference between the coordinates
		#is less than 80, it is a hit.
		if (abs(bulletX-enx)+abs(bulletY-eny)) < 80:
		
			client.hp -= 1
			
			#Instruct clients to project an explosion on him.
			broadcast('tko:hit %s %s' % (client.nick, client.hp)) 
		
			if client.hp <= 0:
				#That tank is dead.
				broadcast('tko:destroy %s' % client.nick)
				
				#Remove him from the player pool.
				del(players[client.address])
		
			return

if __name__ == "__main__":
	
	global pointers
	
	#Initialize a dictionary of command->function mappings, to handle the TKO Protocol
	pointers = {
	'tko:rotate': _tko_rotate,
	'tko:move': _tko_move,
	'tko:shoot': _tko_shoot,
	'tko:refresh': _tko_refresh,
	'tko:newplayer': _tko_newplayer
	}	
	
	main()
