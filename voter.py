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

	#JEREMY -----------------------------------------
	#ENCRYPT VOTE WITH PAILLER HERE
	#WHATEVER THE OUTPUT OF THAT ENCRYPTION IS NEEDS TO BE 
	#ENCRYPTED BY AES BELOW (encryptor.encrypt(vote))
	#JEREMY -----------------------------------------

	#encrypt with AES
	encryptor = AES.new(key,AES.MODE_CBC,iv)
	return encryptor.encrypt(vote)
	
def connect_to_server():
	registrar.Register()
	serv_sock = socket.socket()		#create a socket
	host = socket.gethostname()	#get the host name of the socket
	serv_port = 12345              	#initialize the port for the socket

	serv_sock.connect((host, serv_port))	#connect the socket

	#generate AES key and iv
	serv_AES_key = Random.new().read(16)
	serv_AES_iv = Random.new().read(16)

	#encrypt AES data with server's RSA public key
	f = open("serverpubkey.pem",'r')
	serv_pub_key = RSA.importKey(f.read())
	enc_AES_key = serv_pub_key.encrypt(serv_AES_key,32)
	enc_AES_iv = serv_pub_key.encrypt(serv_AES_iv,32)

	sock.send(enc_AES_key[0])	#send the AES key
	sock.send(enc_AES_iv[0])	#send the AES iv
	
	#get notary public key
	f.close()
	f = open('NotaryKey.pem','r')
	not_pub_key = RSA.importKey(f.read())
	f.close()

	#get voter private key
	f = open('CurrentVoter.pem','r')
	voter_priv_key = RSA.importKey(f.read())
	f.close()

	#generate AES key and iv
	not_AES_key = Random.new().read(16)
	not_AES_iv = Random.new().read(16)

	#encrypt AES info with notary's public key
	enc_AES_key = not_pub_key.encrypt(not_AES_key,32)
	enc_AES_iv = not_pub_key.encrypt(not_AES_iv,32)

	#initialize network connection to notary
	not_sock = socket.socket()		#create a socket
	not_port = 12346              	#initialize the port for the socket
	not_sock.connect((host, not_port))	#connect the socket

	#send encrypted AES data to notary
	sock.send(enc_AES_key[0])	#send the AES key
	sock.send(enc_AES_iv[0])	#send the AES iv
	
	#get random bits from notary over socket
	#k = getrandbits(64)
	#signed_rand_bits = voter_priv_key.sign(randomBits,k)

	#blind vote
	#k = getrandbits(64)
	#vote = get_vote(AES_key,AES_iv)	
	#blinded_vote = not_pub_key.blind(vote,k)

	sock.send(get_vote(AES_key,AES_iv)) #send AES-encrypted vote

	print sock.recv(1024)		#print rec'd confirmation msg
	sock.close			#close the socket

if __name__ == "__main__":
	connect_to_server()	
