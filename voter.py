import socket
import hashlib

from Crypto.Cipher import AES		#requires pyCrypto installation
from Crypto.PublicKey import RSA	#requires pyCrypto installation
from Crypto import Random		#requires pyCrypto installation
import registrar

def get_vote(key,iv):
	vote = raw_input("Enter your vote: ")	#get vote from user

	#pad vote
	while (len(vote) < 64):
		vote += " "

	#encrypt with AES
	encryptor = AES.new(key,AES.MODE_CBC,iv)
	return encryptor.encrypt(vote)
	
def connect_to_server():
	registrar.Register()
	sock = socket.socket()		#create a socket
	host = socket.gethostname()	#get the host name of the socket
	port = 12345              	#initialize the port for the socket

	sock.connect((host, port))	#connect the socket

	#generate AES key and iv
	AES_key = Random.new().read(16)
	AES_iv = Random.new().read(16)

	#encrypt AES data with server's RSA public key
	f = open("serverpubkey.pem",'r')
	RSA_key = RSA.importKey(f.read())
	enc_AES_key = RSA_key.encrypt(AES_key,32)
	enc_AES_iv = RSA_key.encrypt(AES_iv,32)

	sock.send(enc_AES_key[0])	#send the AES key
	sock.send(enc_AES_iv[0])	#send the AES iv
	sock.send(get_vote(AES_key,AES_iv)) #send AES-encrypted vote

	print sock.recv(1024)		#print rec'd confirmation msg
	sock.close			#close the socket

if __name__ == "__main__":
	connect_to_server()	
