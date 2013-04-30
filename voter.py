import socket
import hashlib

from Crypto.Cipher import AES	
from Crypto.PublicKey import RSA
from Crypto import Random	
from Crypto.Random.random import getrandbits
import registrar
import sys


from charm.toolbox.integergroup import RSAGroup
from charm.schemes.pkenc import pkenc_paillier99
from charm.core.math import integer as specialInt
from charm.core.engine.util import objectToBytes,bytesToObject

def get_vote():
	vote = raw_input("Enter your vote: ")	#get vote from user
	vote = long(vote)	
	

	#Initial setup for Paillier
	group = RSAGroup()
	pai = pkenc_paillier99.Pai99(group)

	#Get public voting public key	
	f=open("./pyssss/VotingPublic")
	data = f.read()
	public_key = bytesToObject(data,group)
	
	#Encryption with Paillier
	vote = pai.encode(public_key['n'],vote)
	ciphervote = pai.encrypt(public_key,vote)

#	ciphervotestr = str(str(ciphervote['c']).split('mod')[0])


#	print ciphervote['c']
	ciphervote = specialInt.serialize(ciphervote['c'])

	
	#pad vote
	while (len(ciphervote) < 128):
		ciphervote += " "

	print ciphervote
        return ciphervote

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
	#Could add more input verification
	password = raw_input('Please enter your password: ')
	while len(password) %16 != 0:
		password += '0'

	f = open('CurrentVoter.pem','r')
	enc_x = f.read()
	f.close()
	cipher = AES.new(password, AES.MODE_ECB)
	x = cipher.decrypt(enc_x)
	x = x.rstrip('0')
	voter_priv_key = RSA.importKey(x)

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

	#sign random bits from notary with private key
	k = getrandbits(64)
	signed_rand_bits = str(voter_priv_key.sign(not_rand_bits,k)[0])
	
	#get vote from user and blind
	vote = get_vote()
	k = getrandbits(64)
	blinded_vote = str(not_pub_key.blind(vote,k))

	#pad length of s_r_b to 320
	while (len(signed_rand_bits) < 320):
		signed_rand_bits+=" "

	#send signed random bits and blinded vote back to notary
	not_sock.send(not_AES_encryptor.encrypt(signed_rand_bits))
	not_sock.send(not_AES_encryptor.encrypt(blinded_vote))	

	#receive blind signed vote from notary and unblind
	blinded_signed_vote = not_AES_encryptor.decrypt(not_sock.recv(320))
	blinded_signed_vote = blinded_signed_vote.strip()
	signed_vote = str(not_pub_key.unblind(long(blinded_signed_vote),k))
	
	#send vote to server
	serv_sock.send(serv_AES_encryptor.encrypt(vote))

	#pad signed vote to 320
	while (len(signed_vote) < 320):
		signed_vote += " "
	
	#send signed vote
	serv_sock.send(serv_AES_encryptor.encrypt(signed_vote))
	
	#print rec'd confirmation message
	print serv_sock.recv(1024)
	serv_sock.close			#close the socket

if __name__ == "__main__":
	if (len(sys.argv) != 3):
		print("Usage: python voter.py server_port notary_port")
		sys.exit(0)
	connect_to_server()	
