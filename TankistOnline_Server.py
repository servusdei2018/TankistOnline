import math, select, socket, sys
import ClientClass

from time import sleep

s = None #The socket object
conns = [] #Connections table
playr = [] #Player table

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
	
	print '[i] Intering main loop...'
	
	global conns
	
	ssock = ClientClass.Client(server_socket, "localhost") #Create a client object for the server socket, thatway we can loop through
								#everything using select()
	ssock.isServerSocket = True
	
	conns.append(sclient)
	
	while True:
		
		read_sockets,write_sockets,error_sockets = select.select(conns,[],[])

		for sock in read_sockets:
			
			if sock == ssock: #Incoming connection
				
				sockfd, addr = sock.connection.accept()
				
				newConn = ClientClass.Client(sockfd, addr)
				newConn.send("tko::handshake")
			
			else:
				
				#Data received from existing player
				try:
					
					data = sock.read().splitlines()[0].split(' ')
					
					if sock.status == 0:
						
						#The handshake is confirmed, the client sent the nickname
						
						sock.nick = str(data[0])
						sock.status = 1
						
						new_player(sock.nick)
						
					else:
						
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
	
	index = 0
	
	for con in conns:
		
		if con.nick == nick:
			
			break
			
		index += 1
		
	if data[0] == "tko::request::rotate":
		
		if data[1] == "+":
			
			raw_comms("tko::rotate "+conn.nick+" +")
			
			conn.rotation -= 3
			
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
			
			raw_comms("tko::rotate "+conn.nick+" -")
			
			conn.rotation += 3
			
			if conn.rotation > 360:
				conn.rotation -= 360
			elif conn.rotation < 0:
				conn.rotation += 360
			
			conn.realRotation -= 3
			if conn.realRotation > 360:
				conn.realRotation -= 360
			elif conn.realRotation < 0:
				conn.realRotation += 360
			
	elif data[0] == "tko::request::move":
		
		if data[1] == "+": #Move forward
			
			angle_rad = math.radians(conn.realRotation)
			
			ax = conn.absx
			ay = conn.absy
			
			conn.absx, conn.absy = move(ax, ay, 4, angle_rad)
			
			raw_comms("tko::updateXY "+conn.nick+" "+conn.absx+" "+conn.absy)
			
		elif data[1] == "-": #Move backward
			
			angle_rad = math.radians(conn.realRotation)
			
			ax = conn.absx
			ay = conn.absy
			
			conn.absx, conn.absy = move(ax, ay, -4, angle_rad)
			
			raw_comms("tko::updateXY "+conn.nick+" "+conn.absx+" "+conn.absy)	
			
	elif data[0] == "tko::request::shoot":
		
		#Todo: Implement shoot code

			
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
	
	newClient.send("tko::handshake")

if __name__ == "__main__":
	
	main()
