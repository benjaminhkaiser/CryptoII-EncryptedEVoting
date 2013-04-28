#This is the Notary
#Notary opens for voters to connect and should never be closed

import Crypto
import Crypto.PublicKey.RSA
from Crypto.Random.random import getrandbits
import os, socket

#initialize network connection to voter
sock = socket.socket()	#create socket
host = socket.gethostname()	#get host name of socket
port = 12346		#initialize port to connect over
sock.bind(host,port)	#bind socket to port
sock.listen(5)		#listen for client connection

while(1):
	c,addr = s.accept()	#accept voter connection

	#MOVE KEY GENERATION HERE

	#get AES info and decrypt using RSA private key
	AES_key = key.decrypt(c.recv(128))
	AES_iv = key.decrypt(c.recv(128))

	#generate random bits, encrypt, send to voter
	randomBits = getrandbits(64)
	AES_encryptor = AES.new(AES_key, AES.MODE_CBC, AES_iv)
	enc_rand_bits = encryptor.encrypt(enc_rand_bits)
	sock.send(enc_rand_bits[0])

	#receive random bits signed by voter private key
	
signedRandomBits

#Set this to true only if you get a valid signature verification
isValidUser = false
# iterate through all public keys to see if one is a valid signature
#length of valid public key after export is always 217
statinfo = os.stat('RegKeys.pem')
filesize = statinfo.st_size
f = open('RegKeys.pem', 'r')
if (filesize%271 == 0):
	for x in range(0, filesize/271):
		tPubKey = RSA.importKey(f.read(271))
		if tPubKey.verify(randomBits, signedRandomBits):
			isValidUser = true
			x = filesize/271#This just terminates the for loop
		
if isValidUser:

	#Generate a Notary key pair
	if os.path.isfile('NotaryKey.pem'):
		NotaryKey = RSA.generate(1024)
		NotaryPublic = NotaryKey.publickey()
		#publish Notary public key to a file
		f = open('NotaryKey.pem','w')
		f.write(NotaryPublic.exportKey())
		f.close()
	
		

	#Recieve blinded, encrypted vote from voter
	blindedC



	k = getrandbits(64) #Change this to something random
	#blind sign c'
	blindsigned = NotaryKey.sign( blindedC, k)


	#send blindsigned back to the voter


#Optional behaviour when user is not valid, scolding etc...


