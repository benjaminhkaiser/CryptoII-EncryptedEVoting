#This is the registrar
import Crypto
import os


#This is purely a simulation of going to the Registrar in person
def Register(): # Call this function each time a new voter wants to register
	password = input('Please enter a password (numbers only):')
	#Should add in more error checking on passwords
	
	if os.path.isfile('RegKeys.pem'):
		f = open('RegKeys.pem', 'a')
	else:
		f = open('RegKeys.pem', 'w')

	newKey = RSA.generate(1024)
	f.write(newKey.publickey().exportkey())
	f.close()
	
	#Keys for current voter, only need one voter at a time
	f = open('CurrentVoter.pem', 'w')
	f.write(newKey.expotkey( )
	f.close()
