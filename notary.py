#Notary opens for voters to connect and should never be closed

import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random.random import getrandbits
from Crypto import Random
import os, socket, sys
from os.path import isfile

#initialize network connection to voter
sock = socket.socket()	#create socket
host = socket.gethostname()	#get host name of socket
port = int(sys.argv[1])		#initialize port to connect over
sock.bind((host,port))	#bind socket to port
sock.listen(5)		#listen for client connection


AES_key_size = 512 
AES_iv_size = 512 
blindedVoteSize = 128
signedBlindedVoteSize = 320
signedRandomBitsSize = 320
notaryPublicKeySize=4096
while(1):
	#Generate a Notary key pair
	NotaryKey = RSA.generate(notaryPublicKeySize)
	NotaryPublic = NotaryKey.publickey()
	#publish Notary public key to a file
	f = open('NotaryKey.pem','w')
	f.write(NotaryPublic.exportKey())
	f.close()
	#Create the file to store users who have voted
	f = open('AlreadyVoted.pem','w')
	f.close()
	
	c,addr = sock.accept()	#accept voter connection
	#get AES info and decrypt using RSA private key
	AES_key = NotaryKey.decrypt(c.recv(AES_key_size))
	AES_iv = NotaryKey.decrypt(c.recv(AES_iv_size))
	print AES_iv
	print len(AES_iv)
	AES_encryptor = AES.new(AES_key, AES.MODE_CBC, AES_iv)
	#generate random bits, encrypt, send to voter
	randomBits = str(Random.new().read(16))
	enc_rand_bits = AES_encryptor.encrypt(randomBits)
	c.send(enc_rand_bits)
	
	#receive random bits signed by voter private key
	signedRandomBits = [long(AES_encryptor.decrypt(c.recv(signedRandomBitsSize)).strip()),None]
	blindedVote = AES_encryptor.decrypt(c.recv(blindedVoteSize))
	
	#The registrar must already have published to keys at this point
	# could add redudant (based on our assumptions) error checking that 
	#this file already exists
	statinfo = os.stat('RegKeys.pem')
	filesize_f = statinfo.st_size
	statinfo = os.stat('AlreadyVoted.pem')
	filesize_g = statinfo.st_size
	f = open('RegKeys.pem', 'r')
	g = open('AlreadyVoted.pem','r')
	myFirstTime = True #Make sure no one tries to vote twice

	#271 is standard key size in pem format, it is assumed that these key files
	# are tamper proof but could add extra error checking in the real world
	if (filesize_f%271 == 0):
		for x in range(0, filesize_f/271):
			tPubKey = RSA.importKey(f.read(271))
			for y in range(0, filesize_g/217):
				tAlreadyKey = RSA.importKey( g.read(271) )
				if tAlreadyKey == tPubKey:#Wont check keys already used
					myFirstTime = false
					break;
			g.close()
			g = open('AlreadyVoted.pem','a')
			if myFirstTime:
				if tPubKey.verify(randomBits, signedRandomBits):
					isValidUser = True
					g.write(tPubKey.exportKey())
					break;
	f.close()	
	g.close()
	myFirstTime = True # reset this for the next voter

	#if the user is valid, sign the vote and send it back		
	if isValidUser:
		#sign the vote
		k = getrandbits(64)
		blind_signed_vote = str(NotaryKey.sign(blindedVote,k)[0])
		
		print len(blind_signed_vote)
		#pad the signed vote to len 320 
		while (len(blind_signed_vote) < signedBlindedVoteSize):
			blind_signed_vote += " "
		
		#encrypt with AES and send
		c.send(AES_encryptor.encrypt(blind_signed_vote))
