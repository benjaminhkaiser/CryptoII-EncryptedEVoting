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
from charm.toolbox.conversion import Conversion
from charm.core.math import integer as specialInt
from charm.toolbox.integergroup import integer


from charm.core.engine.util import objectToBytes,bytesToObject

def get_vote():
        vote = raw_input("Enter your vote: ")   #get vote from user
	vote = long(vote)


	group = RSAGroup()
	pai = pkenc_paillier99.Pai99(group)	

	f=open('./pyssss/VotingPublic','rb')
	data = f.read()
	public_key = bytesToObject(data,group)
	
	vote = pai.encode(public_key['n'],vote)
	ciphervote = pai.encrypt(public_key,vote)
	print ciphervote['c']	


	f=open('./pyssss/VotingPrivate','rb')
	data = f.read()
	secret_key = bytesToObject(data,group)

	plaintext=pai.decrypt(public_key, secret_key,ciphervote)
	print plaintext











	ciphervote=42	
        return ciphervote

if __name__ == "__main__":
	get_vote()
