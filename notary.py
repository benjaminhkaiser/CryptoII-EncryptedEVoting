#This is the Notary

import Crypto
import Crypto.PublicKey.RSA

#Genrate a Notary key pair
NotaryKey = RSA.generate(1024)

#publish Notary public key to a file


#Recieve blinded, encrypted vote from voter
#blindedC


#authenticate with token


k = 123L #Change this to something random
#blind sign c'
NotaryKey.sign( blindedC, k)




