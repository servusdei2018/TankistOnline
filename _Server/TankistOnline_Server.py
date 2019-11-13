"""
TankistOnline - Server

The server has been re-written and is under bugtesting.
"""

import math, socket, sys

from ClientClass import Client
from time import sleep

MAP_WIDTH  = 1800 #The width of the map, in PIXELS.
MAP_HEIGHT = 1200 #The height of the map, in PIXELS.
sock = None #Server socket
players = {} #Player table

def main():
	
	"""
	Entrypoint of the server.
	"""
	
	global sock
	
	print('[TankistOnline - Server]')
	print('         v1.0')
	
	#Create socket
	print('[ ] Creating socket...')
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print('[X] Socket created.')
	
	#Bind socket to localhost
	print('[ ] Binding socket...')
	
	try:
		
		HOST = '127.0.0.1'
		PORT = 2019
		
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Reuse address if in use
		sock.bind((HOST, PORT)) #Bind socket to localhost, port 2019
		sock.setblocking(0) #Make sure socket is not blocking
		
		print('[X] Socket bound.')
	
	except socket.error as e:
		
		print('[!] Bind failed.')
		print('    Error Code: ' + str(e[0]))
		print('    Message ' + str(e[1]))
		exit()
	
	#Entering main loop
	
	print('[i] Entering main loop...')
	
	while True:
		
		sleep(.2)
		cycle() #One cycle of processing
		
def cycle():
	
	global players
	
	packets = read_all()
	
	for packet in packets:
	
		#print('%s, %s' % (packet[0], packet[1]))
		process(packet)
	
def process(packet):
	
	global players
	
	#Process a packet
	
	data = packet[0]
	addr = packet[1]
	
	print(data)
	
	if addr not in players:
		
		#If a player is not in the player map, he has shown no proof that
		#he is a client for the game.
		#All clients, when first connecting to the server,
		#send "tko:connect NICKNAME"
		
		print('addr not in players')
		
		if len(data.split()) > 1:
			data = data.split()
		else:
			return
			
		if data[0] != 'tko:newplayer':
			return
		
		#A new player has connected.
		
		players[addr] = Client(addr) #Add him to the player map
		players[addr].nick = data[1] #Give him a nickname
		
		broadcast('tko:newplayer %s' % players[addr].nick)
		broadcast('tko:xy %s %s %s' % (players[addr].nick, players[addr].absx, players[addr].absy))
		
		return
		
	data = data.split()
	
	if data[0] not in pointers: #Invalid command.
		print('invalid command')
		return
	
	pointers[data[0]](addr, data) #Process it.
		
def read_all():
	
	#Read all packets until none are found -- when none are found, recvfrom() returns error
	
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
	
	#Broadcast a message to all clients
	
	print('sending: '+msg)
	
	for client in players:
		sock.sendto(msg.encode(), client)
		
def move(x, y, speed, angle_in_radians):
	
	#Move a point.
	
    new_x = x + (speed*math.cos(angle_in_radians))
    new_y = y + (speed*math.sin(angle_in_radians))
    
    return new_x, new_y
    
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
		
		conn.rotation -= 3
		conn.realRotation += 3
		
	elif degree == '-':
		
		conn.rotation += 3
		conn.realRotation -= 3
		
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
	broadcast('tko:rotate %s %s %s' % (conn.nick, conn.rotation, conn.realRotation))
	
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
		
		conn.absx, conn.absy = move(conn.absx, conn.absy, 4, angle_rad) #Move forwards
		
	elif degree == '-':
		
		conn.absx, conn.absy = move(conn.absx, conn.absy, -4, angle_rad) #Move backwards
		
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
		
def _tko_refresh(addr, data):
	
	"""
	A tank wants information on everyone's x,y and life.
	"""
	
	conn = players[addr]
	
	for player in players:
		plr = players[player]
		broadcast('tko:refresh %s %s %s %s' % (plr.nick, plr.absx, plr.absy, plr.hp))
		
def _tko_shoot(addr, data):
	
	"""
	A tank shot.
	
	TKO Protocol:
	  "tko:shoot"
	"""
	
	global players
	
	conn = players[addr] #Clone the object, for ease of reference
	
	for client in players:
		
		if client.nick != conn.nick: #Don't let a guy shoot himself!
			
			enx = client.absx #Possible target's X, Y
			eny = client.absy
			
			dist = int(math.hypot(conn.absx-enx, conn.absy-eny)) #Distance to enemy
			
			#Now, we get the X, Y location of a bullet shot from the tank who is shooting,
			#and move it in the direction its turret is facing the distance to the current
			#enemy tank. If it is within a certain radius of the enemy tank, then it is a hit.
			
			bulletX, bulletY = move(conn.absx, conn.absy, dist, rads)
			
			if (abs(bulletX-enx)+abs(bulletY-eny)) < 80: #If the difference between the coordinates
			#is less than 80, it is a hit.
			
				client.hp -= 1
				
				#Instruct clients to project an explosion on him.
				broadcast('tko:hit %s' % client.nick) 
			
				if client.hp <= 0:
					#That tank is dead.
					broadcast('tko:destroy %s' % client.nick)
					
					#Remove him from the player pool.
					del(players[client.address])
			
				return

if __name__ == "__main__":
	
	global pointers
	
	pointers = { #A dictionary of command-function mappings to handle the tko protocol
	'tko:rotate': _tko_rotate,
	'tko:move': _tko_move,
	'tko:shoot': _tko_shoot,
	'tko:refresh': _tko_refresh
	}	
	
	main()
