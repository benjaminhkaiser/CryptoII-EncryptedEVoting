#This is the registrar
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import os


#This is purely a simulation of going to the Registrar in person
def Register(): # Call this function each time a new voter wants to register
	password = raw_input('Please choose a password: ')
	#Should add in more error checking on passwords
	#Pad the password to something of 16x bits for AES
	while len(password) %16 != 0:
		password+='0'	


	
	if os.path.isfile('RegKeys.pem'):
		f = open('RegKeys.pem', 'a')
	else:
		f = open('RegKeys.pem', 'w')

	newKey = RSA.generate(1024)
	f.write(newKey.publickey().exportKey())
	f.close()
	
	#Keys for current voter, only need one voter at a time
	f = open('CurrentVoter.pem', 'w')
	x = newKey.exportKey() 
	while len(x) % 16 != 0:
		x += '0'
	cipher = AES.new( password, AES.MODE_ECB)
	enc_x = cipher.encrypt(x)
	f.write(enc_x)
	f.close()

