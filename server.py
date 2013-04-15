import socket

def listen_for_client():
	s = socket.socket()			#create the socket
	host = socket.gethostname()	#get the host name of the socket
	port = 12345				#initialize the port to connect over
	s.bind((host, port))		#bind the socket to the port

	s.listen(5)					#listen for client connections
	while True:
			c, addr = s.accept()				#accept client connection
			votestring = str(addr) + " voted "	#add client address to string
			vote = c.recv(1024)
			votestring += str(vote)
			print votestring
			c.send("Vote registered.")			#send confirmation msg
			c.close()							#close client connection

if __name__ == "__main__":
    listen_for_client()			