
## Simple Examples of how to use pycrypto blind signs  ###
##########################################################
import Crypto
import Crypto.PublicKey.RSA
from Crypto.Random.random import getrandbits
#	key = RSA.generate(1024)
#	key2 = RSA.generate(1024)
#
#
#
#
#	#Syntax for verification
#	key.verify(plaintext,key.sign(plaintext, 123L))
#
#
#	#This gives original message back, "Hello"
#	key.decrypt(key.encrypt( "Hello", 123L))
#
#	NKey = RSA.generate(1024)
#
#	#Blind with Notary, Sign by Notary, Unblind with notary (Sign with encrypt and decrypt)
#	r = 3L
#	blinded = NKey.blind(plaintext, r)
#	k = 2L
#	blindsigned = NKey.sign( blinded, k)
#	signed = NKey.unblind( blindsigned[0], r)
#	# NotaryKey.sign( plaintext, k) == signed
######### END OF EXAMPLES CODE##########################


#############################################################
###### This part of the code is for the voter communication## 
###### 	with the Notary   ###################################
#############################################################

#encrypt the vote with Paillier here
#PaillierEncryptedVote

#Load Notary public key from file
f = open('NotaryKey.pem','r')
NotaryPublic = RSA.importKey(f.read())
f.close()


f = open('CurrentVoter.pem', 'r')
VoterPrivate = RSA.importKey(f.read())#Add prompt for user passcode
f.close()
#Sign the randomBits
k = getrandbits(64)
x = VoterPrivate.sign(randomBits, k)


r = getrandbits(64) #make this more random/secure?
#blind the PaillierVote with Notary key
blinded = NotaryPublic.blind(PaillierEncryptedVote,r)


#Recieve the blind signed vote back
blindsigned

#Get PaillierVote with a signature on it
signed = NotaryPublic.unblind( blindsigned[0]. r)

#Now this can be sent to the server






