import socket
import hashlib

from Crypto.Cipher import AES	#requires pyCrypto installation
from Crypto.PublicKey import RSA	#requires pyCrypto installation
from Crypto import Random		#requires pyCrypto installation

def get_vote():
	vote = raw_input("Enter your vote: ")	#get vote from user
	while (len(vote) < 64):
		vote += " "
	f = open("serverpubkey.pem",'r')
	key = RSA.importKey(f.read()) 
	enc_data = key.encrypt(vote,32)
	print(len(enc_data[0]))	
	return enc_data[0]

def connect_to_server():
	sock = socket.socket()		#create a socket
	host = socket.gethostname()	#get the host name of the socket
	port = 12345              	#initialize the port for the socket

	vote = get_vote()

	sock.connect((host, port))	#connect the socket
	sock.send(vote)			#send the user's vote over the socket

	print sock.recv(1024)		#print rec'd confirmation msg
	sock.close			#close the socket

if __name__ == "__main__":
	connect_to_server()	
