#This is the Notary

import Crypto
import Crypto.PublicKey.RSA
from Crypto.Random.random import getrandbits

#Generate random bits, send to voter

#Get randombits back signed with vote private key

# iterate through all public keys to see if one is a valid signature



#Genrate a Notary key pair
NotaryKey = RSA.generate(1024)
NotaryPublic = NotaryKey.publickey()

#publish Notary public key to a file
f = open('NotaryKey.pem','w')
f.write(NotaryPublic.exportKey())
f.close()

#Recieve blinded, encrypted vote from voter
#blindedC





k = getrandbits(64) #Change this to something random
#blind sign c'
blindsigned = NotaryKey.sign( blindedC, k)


#sent blindsigned back to the voter




