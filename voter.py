import socket
import hashlib

from Crypto.Cipher import AES	
from Crypto.PublicKey import RSA
from Crypto import Random	
from Crypto.Random.random import getrandbits
import registrar
import sys

def get_vote():
	vote = raw_input("Enter your vote: ")	#get vote from user

	#pad vote
	while (len(vote) < 64):
		vote += " "

	#JEREMY -----------------------------------------
	#ENCRYPT VOTE WITH PAILLER HERE

	return vote


def connect_to_server():
	registrar.Register()
	serv_sock = socket.socket()		#create a socket
	host = socket.gethostname()	#get the host name of the socket
	serv_port = int(sys.argv[1])  	#initialize the port for the socket

	serv_sock.connect((host, serv_port))	#connect the socket

	#generate AES key, iv, encryptor and decryptor
	serv_AES_key = Random.new().read(16)
	serv_AES_iv = Random.new().read(16)
	serv_AES_encryptor = AES.new(serv_AES_key, AES.MODE_CBC, serv_AES_iv)

	#encrypt AES data with server's RSA public key
	f = open("serverpubkey.pem",'r')
	serv_pub_key = RSA.importKey(f.read())
	enc_AES_key = serv_pub_key.encrypt(serv_AES_key,32)
	enc_AES_iv = serv_pub_key.encrypt(serv_AES_iv,32)

	serv_sock.send(enc_AES_key[0])	#send the AES key
	serv_sock.send(enc_AES_iv[0])	#send the AES iv
	
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
	not_AES_encryptor = AES.new(not_AES_key, AES.MODE_CBC, not_AES_iv)
	
	#encrypt AES info with notary's public key
	enc_AES_key = not_pub_key.encrypt(not_AES_key,32)
	enc_AES_iv = not_pub_key.encrypt(not_AES_iv,32)

	#initialize network connection to notary
	not_sock = socket.socket()		#create a socket
	not_port = int(sys.argv[2])   	#initialize the port for the socket
	not_sock.connect((host, not_port))	#connect the socket

	#send encrypted AES data to notary
	not_sock.send(enc_AES_key[0])	#send the AES key
	not_sock.send(enc_AES_iv[0])	#send the AES iv
	
	#get random bits from notary over socket
	not_rand_bits = not_AES_encryptor.decrypt(not_sock.recv(16))

	#get voter's private key	
	f = open("CurrentVoter.pem",'r')
	voter_priv_key = RSA.importKey(f.read())

	#sign random bits from notary with private key
	k = getrandbits(64)
	signed_rand_bits = str(voter_priv_key.sign(not_rand_bits,k)[0])
	
	#get vote from user and blind
	vote = get_vote()
	k = getrandbits(64)
	blinded_vote = str(not_pub_key.blind(vote,k))

	print(blinded_vote)

	#pad length of s_r_b to something divisible by 16 (usually 320)
	while (len(signed_rand_bits) % 16 != 0):
		signed_rand_bits+=" "

	#send signed random bits and blinded vote back to notary
	not_sock.send(not_AES_encryptor.encrypt(signed_rand_bits))
	not_sock.send(not_AES_encryptor.encrypt(blinded_vote))	
	
	#send vote
	serv_sock.send(serv_AES_encryptor.encrypt(vote))

	print serv_sock.recv(1024)		#print rec'd confirmation msg
	serv_sock.close			#close the socket

if __name__ == "__main__":
	if (len(sys.argv) != 3):
		print("Usage: python voter.py server_port notary_port")
		sys.exit(0)
	connect_to_server()	
