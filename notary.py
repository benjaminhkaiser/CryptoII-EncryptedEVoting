#This is the Notary

import Crypto
import Crypto.PublicKey.RSA
from Crypto.Random.random import getrandbits
import os

#Generate random bits, send to voter
randomBits = getrandbits(64)
#Get randombits back signed with vote private key
signedRandomBits

#Set this to true only if you get a valid signature verification
isValidUser = false
# iterate through all public keys to see if one is a valid signature
#length of valid public key after export is always 217
statinfo = os.stat('RegKeys.pem')
filesize = stat_info.st_size
f = open('RegKeys.pem', 'r')
if (filesize%217 == 0):
	for x in range(0, filesize/217):
		tPubKey = RSA.importKey(f.read(271))
		if tPubKey.verify(randomBits, signedRandomBits):
			isValidUser = true
			x = filesize/217#This just terminates the for loop
		
if isValidUser:

	#Genrate a Notary key pair
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


