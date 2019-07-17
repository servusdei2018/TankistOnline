import math, select, socket, sys
import ClientClass

from time import sleep

s = None #The socket object
conns = [] #Connections table
playr = [] #Player table

"""
TankistOnline - Server

Currently, the server is fully functional

"""

def main():
	
	global s
	
	print '[TankistOnline - Server]'
	print '         v1.0'
	
	#Create socket
	print '[ ] Creating socket...'
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print '[X] Socket created.'
	
	#Bind socket to localhost
	print '[ ] Binding socket...'
	
	try:
		
		HOST = "0.0.0.0"
		PORT = 1234
		
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((HOST, PORT))
		print '[X] Socket bound.'
	
	except socket.error as msg:
		
		print '[!] Bind failed.'
		print '    Error Code: ' + str(msg[0])
		print '    Message ' + str(msg[1])
		sys.exit()
		
		
	#Start listening
	
	print '[ ] Starting listener...'
	server_socket.listen(10)
	print '[X] Listener started.'
	
	#Entering main loop
	
	print '[i] Entering main loop...'
	
	global conns
	
	#Create a client object for the server socket, thatway we can loop through
	#everything (including our serversocket) using select()
	
	ssock = ClientClass.Client(server_socket, "localhost") 

	ssock.isServerSocket = True
	
	conns.append(ssock)
	
	while True:
		
		read_sockets, write_sockets, error_sockets = select.select(conns,[],[])

		for sock in read_sockets:
			
			if sock == ssock: #Incoming connection
				
				sockfd, addr = sock.connection.accept()
				
				newConn = ClientClass.Client(sockfd, addr)
				greet(newConn) #Initiate the handshake
			
			else:
				
				#Data received from existing player
				
				try:
					
					data = sock.read().splitlines()[0].split(' ')
					
					if sock.status == 0:
						
						#The first line sent from the client is a nickname in response to the handshake
						#request. So the handshake is confirmed, and the client sent his nickname.
						
						sock.nick = str(data[0])
						sock.status = 1
						
						new_player(sock.nick) #Notify each player of the new arrival
						
					else:
						
						#The player has already sent in his nickname, so this must be
						#data.
						
						process(sock, data) 
				
				except:
					
					#If there's an error with the socket, close it. The game must
					#continue.
					
					try:
						
						sock.connection.shutdown()
						sock.connection.close()
						
						notify_all(sock.nick + " has left the battle.")
						
					except:
						
						print '[i] Exception in closing socket.'
					
					finally:
					
						conns.remove(sock)
					
def process(conn, data):
	
	#Process data received from a client.
	
	"""
	index = 0
	
	for con in conns:
		
		if con.nick == nick:
			
			break
			
		index += 1
	"""
	#----^ I forgot why I added that...
	
		
	if data[0] == "tko::request::rotate": #The client requests to be rotated
		
		#Rotate the player's tank.
		
		if data[1] == "+":
			
			raw_comms("tko::rotate "+conn.nick+" +") #Notify each player of the increase in rotation
			
			conn.rotation -= 3 #Increment rotation
			
			#Perform rotation validation
			
			if conn.rotation > 360:
				conn.rotation -= 360
			elif conn.rotation < 0:
				conn.rotation += 360
			
			conn.realRotation += 3
			if conn.realRotation > 360:
				conn.realRotation -= 360
			elif conn.realRotation < 0:
				conn.realRotation += 360
			
		elif data[1] == "-":
			
			raw_comms("tko::rotate "+conn.nick+" -") #Notify each player of the decrease in rotation
			
			conn.rotation += 3 #Increment rotation
			
			#Perform rotation validation
			
			if conn.rotation > 360:
				conn.rotation -= 360
			elif conn.rotation < 0:
				conn.rotation += 360
			
			conn.realRotation -= 3
			if conn.realRotation > 360:
				conn.realRotation -= 360
			elif conn.realRotation < 0:
				conn.realRotation += 360
			
	elif data[0] == "tko::request::move": #The client requests to be moved
		
		if data[1] == "+": #Move forward
			
			angle_rad = math.radians(conn.realRotation)
			
			ax = conn.absx
			ay = conn.absy
			
			conn.absx, conn.absy = move(ax, ay, 4, angle_rad)
			
			raw_comms("tko::updateXY "+conn.nick+" "+conn.absx+" "+conn.absy) #Instruct each client to update
																			  #that player's location.
			
		elif data[1] == "-": #Move backward
			
			angle_rad = math.radians(conn.realRotation)
			
			ax = conn.absx
			ay = conn.absy
			
			conn.absx, conn.absy = move(ax, ay, -4, angle_rad)
			
			raw_comms("tko::updateXY "+conn.nick+" "+conn.absx+" "+conn.absy) #Instruct each client to update
																			  #that player's location.
			
	elif data[0] == "tko::request::shoot": #The client wants to shoot
		
		for pe in conns:
			
				if pe.nick != conn.nick: #We don't want someone to shoot himself :)
					
					enx = pe.absx #Enemy X
					eny = pe.absy #Enemy Y
				
					dist = int(math.hypot(myx - enx, myy - eny)) #Get distance to the enemy
				
					#Now, we get the X and Y location of a bullet shot from the tank who is shooting,
					#moving it in the direction its turret is facing the distance to the current
					#enemy tank.
				
					bulletX, bulletY = move(conn.absx, conn.absy, dist, rads)
				
					if abs(bulletX-enx) + abs(bulletY-eny) < 80: #If the difference between the bulletX and
					#the bullet Y is less than 80, then it is a hit.
					
						explode(pe) #Notify all clients, that they may show an explosion on the hit tank.

		
def move(x, y, speed, angle_in_radians):
	
	#Move a point.
	
    new_x = x + (speed*math.cos(angle_in_radians))
    new_y = y + (speed*math.sin(angle_in_radians))
    
    return new_x, new_y
		
def raw_comms(raw):
	
	#Send raw text to all clients.
	
	for com in conns:
		
		com.send(raw)
					
					
def new_player(nick):
	
	#Notify each client of the new player, that they may add him to their player
	#table.
	
	for con in conns:
		
		con.send("tko::newplayer "+ nick)					


def notify_all(msg):
	
	#Each client should pop up a little notification, notifying the player
	#of the message.
	
	for con in conns:
		
		con.send("tko::msg " + msg)
					
					
def greet(newClient):
	
	#Send a handshake prompt to a client.
	
	newClient.send("tko::handshake")
	

def explode(client):
	
	#Notify everyone that the specified player was hit.
	
	raw_comms("tko::explode "+client.nick)
	

if __name__ == "__main__":
	
	main()
