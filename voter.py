import socket
import hashlib

from Crypto.Cipher import AES	#requires pyCrypto installation
from Crypto import Random		#requires pyCrypto installation

iv = Random.new().read(16)

def get_vote(key):
	vote = raw_input("Enter your vote: ")	#get vote from user
	while (len(vote) < 1024):
			vote += " "
	encryptor = AES.new(key,AES.MODE_CBC,iv)
	vote = encryptor.encrypt(vote)
	return vote

def connect_to_server():
	sock = socket.socket()		#create a socket
	host = socket.gethostname()	#get the host name of the socket
	port = 12345              	#initialize the port for the socket

	#key = hashlib.sha256(host).digest()	#generate a key using hostname as seed
	key = '0123456789abcdef'

	vote = get_vote(key)

	sock.connect((host, port))	#connect the socket
	sock.send(vote)				#send the user's vote over the socket
	sock.send(iv)
	print sock.recv(1024)		#print rec'd confirmation msg
	sock.close					#close the socket

if __name__ == "__main__":
	connect_to_server()	