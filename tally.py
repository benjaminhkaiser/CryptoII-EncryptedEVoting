#!/usr/bin/python
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
from charm.schemes.pkenc.pkenc_paillier99 import Ciphertext
from charm.toolbox.conversion import Conversion
from charm.core.math import integer as specialInt
from charm.toolbox.integergroup import integer


from charm.core.engine.util import objectToBytes,bytesToObject

def tally_vote():

	#initialization
	group = RSAGroup()
	pai = pkenc_paillier99.Pai99(group)	


	#get voting public key	
	f=open('./pyssss/VotingPublic','rb')
	data = f.read()
	public_key = bytesToObject(data,group)
	n=public_key['n']
	
	#get voting private key
	f=open('./pyssss/VotingPrivate','rb')
	data = f.read()
	secret_key = bytesToObject(data,group)

	
	#get ciphervotes file
	f=open('./CipherVotes','r')
	data=f.readlines()
	count = 0
	
	#go through all recorded ciphervotes
	for vote in data:
		serializedVote = vote.strip()
		ciphervote = specialInt.deserialize(serializedVote)
		ciphervote = Ciphertext({'c':ciphervote},public_key,'c')	
		if count == 0:
			ciphertotal = ciphervote
		else:
			ciphertotal=ciphertotal+ciphervote


		#ciphertotal=ciphertotal+((pai.L(ciphervote**specialInt.toInt(secret_key['lamda']), n) % n) * secret_key['u']) % n
		count = count +1		

	print 'Our calculated total:', pai.decrypt(public_key,secret_key,ciphertotal)
	#get ciphervotes file
	f=open('./CipherVotesTotal','r')
	data=f.read()
	data=data.strip()
	ciphervotetotal = specialInt.deserialize(data)
	ciphervotetotal = Ciphertext({'c':ciphervotetotal},public_key,'c')
	ciphervotetotal = pai.decrypt(public_key,secret_key,ciphervotetotal)
	
	print 'Their calculated total:',ciphervotetotal

	return


if __name__ == "__main__":
	tally_vote()
