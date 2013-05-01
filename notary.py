#Notary opens for voters to connect and should never be closed

import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random.random import getrandbits
from Crypto import Random
import os, socket, sys

#initialize network connection to voter
sock = socket.socket()	#create socket
host = socket.gethostname()	#get host name of socket
port = int(sys.argv[1])		#initialize port to connect over
sock.bind((host,port))	#bind socket to port
sock.listen(5)		#listen for client connection


AES_key_size = 128
AES_iv_size = 128
blindedVoteSize = 128
signedBlindedVoteSize = 320
signedRandomBitsSize = 320
notaryPublicKeySize=1024
while(1):
	#Generate a Notary key pair
	NotaryKey = RSA.generate(notaryPublicKeySize)
	NotaryPublic = NotaryKey.publickey()
	#publish Notary public key to a file
	f = open('NotaryKey.pem','w')
	f.write(NotaryPublic.exportKey())
	f.close()
	
	c,addr = sock.accept()	#accept voter connection
	#get AES info and decrypt using RSA private key
	AES_key = NotaryKey.decrypt(c.recv(AES_key_size))
	AES_iv = NotaryKey.decrypt(c.recv(AES_iv_size))
	AES_encryptor = AES.new(AES_key, AES.MODE_CBC, AES_iv)
	#generate random bits, encrypt, send to voter
	randomBits = str(Random.new().read(16))
	enc_rand_bits = AES_encryptor.encrypt(randomBits)
	c.send(enc_rand_bits)
	
	#receive random bits signed by voter private key
	signedRandomBits = [long(AES_encryptor.decrypt(c.recv(signedRandomBitsSize)).strip()),None]
	blindedVote = AES_encryptor.decrypt(c.recv(blindedVoteSize))
	
	statinfo = os.stat('RegKeys.pem')
	filesize = statinfo.st_size
	f = open('RegKeys.pem', 'r')
	if (filesize%271 == 0):
		for x in range(0, filesize/271):
			tPubKey = RSA.importKey(f.read(271))
			if tPubKey.verify(randomBits, signedRandomBits):
				isValidUser = True
				break;

	#if the user is valid, sign the vote and send it back		
	if isValidUser:
		#sign the vote
		k = getrandbits(64)
		blind_signed_vote = str(NotaryKey.sign(blindedVote,k)[0])

		#pad the signed vote to len 320 
		while (len(blind_signed_vote) < signedBlindedVoteSize):
			blind_signed_vote += " "
		
		#encrypt with AES and send
		c.send(AES_encryptor.encrypt(blind_signed_vote))
