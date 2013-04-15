import socket

vote = raw_input("Enter your vote: ")	#get vote from user

sock = socket.socket()		#create a socket
host = socket.gethostname()	#get the host name of the socket
port = 12345              	#initialize the port for the socket

sock.connect((host, port))	#connect the socket
sock.send(vote)				#send the user's vote over the socket
print sock.recv(1024)		#print rec'd confirmation msg
sock.close					#close the socket